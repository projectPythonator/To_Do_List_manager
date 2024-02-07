import mvc_exceptions as mvc_exc
from typing import Dict, Tuple, List


TaskItem = Tuple[str, str]
ToDoTasks = Dict[str, str] | None  # for now, we shall keep this basic like this
ListOfTasks = Dict[str, str]
to_do_tasks: ToDoTasks | None = {}
users: Dict[str, to_do_tasks] | None = {}

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


def create_user_by_user_name(self, user_name: str) -> None:
    global users
    if user_name not in users:
        users[user_name] = {}
    else:
        raise mvc_exc.UserNameOnCreationAlreadyExists(
            "User name {} already exists during creation".format(user_name))


def delete_user_by_user_name(self, user_name: str) -> None:
    global users
    if user_name in users:
        del users[user_name]
    else:
        raise mvc_exc.UserNameOnDeleteDoesNotExist(
            "User name {} does not exist during deletion".format(user_name))

