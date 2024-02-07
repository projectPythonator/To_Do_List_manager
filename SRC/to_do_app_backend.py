from sqlite3 import OperationalError, IntegrityError, ProgrammingError
import sqlite3
import mvc_exceptions as mvc_exc


DB_name = ''


def scrub(input_string: str) -> str:
    """Clean an input string (to prevent SQL injection). only take chars and nums."""
    return ''.join(k for k in input_string if k.isalnum())


def connect_to_db(new_data_base=None):
    """Connect to a db. creates db if there isn't one yet."""
    global DB_name
    if new_data_base is None:
        DB_name = ':memory:'
        print("connected to local data base")
    else:
        DB_name = '{}.db'.format(new_data_base)
        print("connected to {} data base.".format(new_data_base))
    connection = sqlite3.connect(DB_name)
    return connection


def connect(func):
    """Function will open the database if it is not already open on the try."""
    def inner_func(conn, *args, **kwargs):
        try:
            conn.execute('SELECT name FROM sqlite_temp_master WHERE type="table";')
        except (AttributeError, ProgrammingError):
            conn = connect_to_db(DB_name)
        return func(conn, *args, **kwargs)
    return inner_func


def disconnect_from_db(db=None, conn=None):
    if db is not DB_name:
        print("You are trying to disconnect from a wrong DB")
    if conn is not None:
        conn.close()


@connect
def create_table(conn, table_name: str):
    """Create a user profile in the form of a table."""
    table_name = scrub(table_name)
    sql = ('CREATE TABLE {} (rowid INTEGER PRIMARY KEY AUTOINCREMENT, '
           'name TEXT UNIQUE, '
           'description TEXT UNIQUE)').format(table_name)
    try:
        conn.execute(sql)
    except OperationalError as e:
        print(e)


@connect
def insert_one(conn, task_name: str, task_description: str, user_name: str):
    """For given username adds a new task to their list."""
    user_name = scrub(user_name)
    sql_command = "INSERT INTO {} ('name', 'description') VALUES (?, ?)".format(user_name)
    try:
        conn.execute(sql_command, (task_name, task_description))
        conn.commit()
    except IntegrityError as e:
        mvc_exc.TaskNameOnCreationAlreadyExists(
            "{} task name '{}' already stored in user {} tasks".format(e, task_name, user_name))


@connect
def select_all(conn, user_name: str):
    user_name = scrub(user_name)
    sql_command = "SELECT * FROM {}".format(user_name)
    connect_obj = conn.execute(sql_command)
    return connect_obj.fetchall()


@connect
def delete_one(conn, task_name: str, user_name: str):
    user_name = scrub(user_name)
    sql_check_command = 'SELECT EXISTS(SELECT 1 FROM {} WHERE name=? LIMIT 1)'.format(user_name)
    sql_delete_command = 'DELETE FROM {} WHERE name=?'.format(user_name)
    connect_obj = conn.execute(sql_check_command, (task_name,))  # tuple is needed so we append ,
    result = connect_obj.fetchone()
    if result[0]:
        connect_obj.execute(sql_delete_command, (task_name,))  # tuple is needed so we append ,
        conn.commit()
    else:
        mvc_exc.UserNameOnDeleteDoesNotExist(
            "cant delete '{}' because it does not exist for user {}".format(task_name, user_name))
