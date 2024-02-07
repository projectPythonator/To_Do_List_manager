from sqlite3 import OperationalError, IntegrityError, ProgrammingError, connect
import mvc_exceptions as mvc_exc


data_base_name: str = ''


def connect_to_data_base(name_of_db=None):
    global data_base_name
    """Connect to a db. creates db if there isn't one yet."""
    if name_of_db is None:
        data_base_name = 'local_data_base'
        print("connected to local data base")
    else:
        data_base_name = '{}.db'.format(name_of_db)
        print("connected to {} data base.".format(data_base_name))
    connection = connect(data_base_name)
    return connection


def connect_attempt(func):
    """Connect to a db. creates db if there isn't one yet."""

    def inner_func(conn, *args, **kwargs):
        try:
            conn.execture('SELECT name FROM sqlite_temp_master WHERE type="table";')
        except (AttributeError, ProgrammingError):
            conn = connect_to_data_base(data_base_name)
        return func(conn, *args, **kwargs)

    return inner_func


def disconnect_from_db(db_name=None, conn=None):
    if db_name is not data_base_name:
        print("trying to disconnect from the wrong db!!")
    if conn is not None:
        conn.close()


@connect
def create_table(conn, name_of_user: str):
    name_of_user = scrub(name_of_user)
    sql_cmd = ('CREATE TABLE {} (rowid INTEGER PRIMARY KEY AUTOINCREMENT, '
               'name TEXT UNIQUE, '
               'description TEXT)').format(name_of_user)
    try:
        conn.execute(sql_cmd)
    except OperationalError as e:
        print(e)


def scrub(input_string):
    """Clean an input string (to prevent SQL injection).

    Parameters
    ----------
    input_string : str

    Returns
    -------
    str
    """
    return ''.join(k for k in input_string if k.isalnum())


@connect
def insert_task(conn, task_name: str, task_description: str, user_name):
    user_name = scrub(user_name)
    sql_command = "INSERT INTO {} ('name', 'description') VALUES (?, ?)".format(user_name)
    try:
        conn.execute(sql_command, (task_name, task_description))
        conn.commit()
    except IntegrityError as e:
        mvc_exc.TaskNameOnCreationAlreadyExists(
            "{} '{}' already stored in user {} tasks".format(e, task_name, user_name))


@connect
def insert_tasks(conn, tasks, user_name):
    user_name = scrub(user_name)
    sql_command = "INSERT INTO {} ('name', 'description') VALUES (?, ?)".format(user_name)
    entries = [(task, description) for task, description in tasks]
    try:
        conn.executemany(sql_command, entries)
        conn.commit()
    except IntegrityError as e:
        print("{}: at least one task in {} already exists for user {}".format(e,
                                                                              [el[0] for el in tasks],
                                                                              user_name))


@connect
def read_task(conn, task_name, user_name):
    user_name = scrub(user_name)
    task_name = scrub(task_name)
    sql_command = "SELECT * FROM {} WHERE name='{}'".format(user_name, task_name)
    connect_obj = conn.execute(sql_command)
    result = connect_obj.fetchone()
    if result is not None:
        return result
    else:
        mvc_exc.TaskNameOnReadDoesNotExist(
            "cant read '{}' because it does not exist for user {}".format(task_name, user_name))


@connect
def read_tasks(conn, user_name):
    user_name = scrub(user_name)
    sql_command = "SELECT * FROM {}".format(user_name)
    connect_obj = conn.execute(sql_command)
    result = connect_obj.fetchall()
    return result


@connect
def update_task(conn, task_name, task_description, user_name):
    user_name = scrub(user_name)
    sql_check_command = 'SELECT EXISTS(SELECT 1 FROM {} WHERE name=? LIMIT 1'.format(user_name)
    sql_update_command = 'UPDATE {} SET description=? WHERE name=?'.format(user_name)
    connect_obj = conn.execute(sql_check_command, (task_name,))
    result = connect_obj.fetchone()
    if result[0]:
        connect_obj.execute(sql_update_command, (task_description, task_name))
        conn.commit()
    else:
        mvc_exc.TaskNameOnUpdateDoesNotExist(
            "cant update '{}' because it does not exist for user {}".format(task_name, user_name))


@connect
def delete_task(conn, task_name, user_name):
    user_name = scrub(user_name)
    sql_check_command = 'SELECT EXISTS(SELECT 1 FROM {} WHERE name=? LIMIT 1'.format(user_name)
    user_name = scrub(user_name)
    sql_delete_command = 'DELETE FROM {} WHERE name=?'.format(user_name)
    connect_obj = conn.execute(sql_check_command, (task_name,))
    result = connect_obj.fetchone()
    if result[0]:
        connect_obj.execute(sql_delete_command, (task_name,))
        conn.commit()
    else:
        mvc_exc.UserNameOnDeleteDoesNotExist(
            "cant delete '{}' because it does not exist for user {}".format(task_name, user_name))

