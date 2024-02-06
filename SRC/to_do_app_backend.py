from typing import Dict

ToDoTasks = Dict[str, str] | None  # for now, we shall keep this basic like this
ListOfTasks = Dict[str, str]

to_do_tasks: ToDoTasks | None = None


def create_tasks(new_tasks: ListOfTasks) -> None:
    """Sets the current list of task to a new list of tasks."""
    global to_do_tasks
    to_do_tasks = new_tasks


def create_task(task_name: str, task_description: str) -> None:
    """Creates a new task to be done."""
    global to_do_tasks
    to_do_tasks[task_name] = task_description
