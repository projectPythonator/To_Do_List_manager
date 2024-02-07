from sqlite3 import OperationalError, IntegrityError, ProgrammingError, connect
import mvc_exceptions as mvc_exc
from typing import Dict, Tuple, List

TaskItem = Tuple[str, str]
ToDoTasks = Dict[str, str] | None  # for now, we shall keep this basic like this
ListOfTasks = Dict[str, str]
to_do_tasks: ToDoTasks | None = {}
users: Dict[str, Tuple[str, str]] | None = {}
current_user: str = ''

data_base_name: str = ''


def connect_to_data_base(name_of_db=None):
    global data_base_name
    """Connect to a db. creates db if there isn't one yet."""
    if name_of_db is None:
        data_base_name = 'local_data_base'
        print("connected to local data base")
    else:
        data_base_name = name_of_db
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
def create_table(conn, name_of_user):
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






def create_tasks(new_tasks: ListOfTasks) -> None:
    """Sets the current list of task to a new list of tasks."""
    global to_do_tasks
    to_do_tasks = new_tasks


def create_task_by_name_and_description(task_name: str, task_description: str) -> None:
    """Creates a new task to be done."""
    global to_do_tasks
    if task_name not in to_do_tasks:
        to_do_tasks[task_name] = task_description
    else:
        raise mvc_exc.TaskNameOnCreationAlreadyExists(
            "task {}, with description {} already exists".format(task_name, task_description))


def read_task_by_named_key(task_key_name: str):
    """Grabs task by keyed name."""
    global to_do_tasks
    if task_key_name in to_do_tasks:
        return to_do_tasks[task_key_name]
    else:
        raise mvc_exc.TaskNameOnReadDoesNotExist(
            "Task with name {} was not found in list of tasks".format(task_key_name))


def read_all_tasks() -> List[TaskItem]:
    """Grabs all tasks that currently exist."""
    global to_do_tasks
    return [(task_name, task_description) for task_name, task_description in to_do_tasks.items()]


def update_task_given_keyed_name(task_key_name: str, new_description: str) -> None:
    """Takes task key and new description and tries to update the task."""
    global to_do_tasks
    if task_key_name in to_do_tasks:
        to_do_tasks[task_key_name] = new_description
    else:
        raise mvc_exc.TaskNameOnUpdateDoesNotExist(
            "Task name {} and description {} was not found".format(task_key_name, new_description))


def delete_task_given_keyed_name(task_key_name: str) -> None:
    """Delete given task if it exists"""
    global to_do_tasks
    if task_key_name in to_do_tasks:
        to_do_tasks.pop(task_key_name)
    else:
        raise mvc_exc.TaskNameOnDeleteDoesNotExist(
            "Task name {} not found when deletion attempted".format(task_key_name))


def create_user_by_user_name(user_name: str) -> None:
    global users
    if user_name not in users:
        users[user_name] = {}
    else:
        raise mvc_exc.UserNameOnCreationAlreadyExists(
            "User name {} already exists during creation".format(user_name))


def delete_user_by_user_name(user_name: str) -> None:
    global users
    if user_name in users:
        del users[user_name]
    else:
        raise mvc_exc.UserNameOnDeleteDoesNotExist(
            "User name {} does not exist during deletion".format(user_name))


def load_user_by_user_name(user_name: str) -> None:
    global users, current_user
    if user_name in users:
        current_user = user_name
        create_tasks(users[user_name])
    else:
        raise mvc_exc.UserNameOnDeleteDoesNotExist(
            "User name {} does not exist during deletion".format(user_name))
