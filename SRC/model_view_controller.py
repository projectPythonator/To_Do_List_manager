import to_do_app_backend as backend_file
import mvc_exceptions as mvc_exc


class Model(object):
    def __init__(self, user_info):
        backend_file.create_tasks(user_info)  # load up the info for a user
        pass

    def load_user(self, user_key):
        backend_file.load_user_by_user_name(user_key)

    def add_new_user(self, user_key):
        backend_file.create_user_by_user_name(user_key)

    def delete_user(self, user_key):
        backend_file.delete_user_by_user_name(user_key)

    def create_task(self, task_key_name, task_description):
        backend_file.create_task_by_name_and_description(task_key_name, task_description)

    def create_tasks(self, list_of_tasks):
        backend_file.create_tasks(list_of_tasks)

    def read_task(self, task_key):
        return backend_file.read_task_by_named_key(task_key)

    def read_tasks(self):
        return backend_file.read_all_tasks()

    def update_task(self, task_key, task_description):
        backend_file.update_task_given_keyed_name(task_key, task_description)

    def delete_task(self, task_key):
        backend_file.delete_task_given_keyed_name(task_key)

class View(object):
    def __init__(self):
        pass


class Controller(object):
    def __init__(self):
        pass
