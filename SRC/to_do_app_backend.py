from sqlite3 import OperationalError, IntegrityError, ProgrammingError
import sqlite3
import mvc_exceptions as mvc_exc


DB_name = ''


def scrub(input_string):
    """Clean an input string (to prevent SQL injection)."""
    return ''.join(k for k in input_string if k.isalnum())


def connect_to_db(db=None):
    """Connect to a db. creates db if there isn't one yet."""
    if db is None:
        current_db = ':memory:'
        print("connected to local data base")
    else:
        current_db = '{}.db'.format(db)
        print("connected to {} data base.".format(db))
    connection = sqlite3.connect(current_db)
    return connection


def connect(func):
    """Connect to a db. creates db if there isn't one yet."""
    def inner_func(conn, *args, **kwargs):
        try:
            conn.execute(
                'SELECT name FROM sqlite_temp_master WHERE type="table";')
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
def create_table(conn, table_name):
    name_of_user = scrub(table_name)
    sql = ('CREATE TABLE {} (rowid INTEGER PRIMARY KEY AUTOINCREMENT, '
           'name TEXT UNIQUE, '
           'description TEXT UNIQUE)').format(table_name)
    try:
        conn.execute(sql)
    except OperationalError as e:
        print(e)


@connect
def insert_one(conn, task_name, task_description, user_name):
    user_name = scrub(user_name)
    sql_command = "INSERT INTO {} ('name', 'description') VALUES (?, ?)".format(user_name)
    try:
        conn.execute(sql_command, (task_name, task_description))
        conn.commit()
    except IntegrityError as e:
        mvc_exc.TaskNameOnCreationAlreadyExists(
            "{} '{}' already stored in user {} tasks".format(e, task_name, user_name))


@connect
def insert_many(conn, tasks, user_name):
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
def select_one(conn, task_name, user_name):
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
def select_all(conn, user_name):
    user_name = scrub(user_name)
    sql_command = "SELECT * FROM {}".format(user_name)
    connect_obj = conn.execute(sql_command)
    result = connect_obj.fetchall()
    return result


@connect
def update_one(conn, task_name, task_description, user_name):
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
def delete_one(conn, task_name, user_name):
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


def main():
    table_name = 'agis'
    conn = connect_to_db()  # in-memory database
    # conn = connect_to_db(DB_name)  # physical database (i.e. a .db file)

    create_table(conn, table_name)





if __name__ == "__main__":
    main()