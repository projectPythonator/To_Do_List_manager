import mvc_exceptions as mvc_exc
from typing import Dict, Tuple, List


TaskItem = Tuple[str, str]
ToDoTasks = Dict[str, str] | None  # for now, we shall keep this basic like this
ListOfTasks = Dict[str, str]

to_do_tasks: ToDoTasks | None = None


def create_tasks(new_tasks: ListOfTasks) -> None:
    """Sets the current list of task to a new list of tasks."""
    global to_do_tasks
    to_do_tasks = new_tasks


def create_task_by_name_and_description(task_name: str, task_description: str) -> None:
    """Creates a new task to be done."""
    global to_do_tasks
    if task_name in to_do_tasks:
        raise mvc_exc.TaskByNameAlreadyExistsOnCreation(
            "task {}, with description {} already exists".format(task_name, task_description))
    else:
        to_do_tasks[task_name] = task_description


def read_task_by_named_key(task_key_name: str):
    """Grabs task by keyed name."""
    global to_do_tasks
    if task_key_name not in to_do_tasks:
        raise mvc_exc.TaskNameOnReadDoesNotExist(
            "Task with name {} was not found in list of tasks".format(task_key_name))
    else:
        return to_do_tasks[task_key_name]


def read_all_tasks() -> List[TaskItem]:
    """Grabs all tasks that currently exist."""
    global to_do_tasks
    return [(task_name, task_description) for task_name, task_description in to_do_tasks.items()]
