from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QHBoxLayout, QLineEdit, QPushButton, QListWidget)
import to_do_app_backend as backend_file
import mvc_exceptions as mvc_exc


class Model(object):
    def __init__(self, user_name: str, tasks):
        self._user_name = user_name
        self._connection = backend_file.connect_to_data_base(backend_file.data_base_name)
        backend_file.create_table(self.connection, self._user_name)
        self.create_tasks(tasks)

    @property
    def connection(self):
        return self._connection

    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, new_user):
        self._user_name = new_user

    def create_task(self, name, description):
        backend_file.insert_one(self.connection, name, description, user_name=self.user_name)

    def create_tasks(self, tasks):
        backend_file.insert_many(self.connection, tasks, user_name=self.user_name)

    def read_task(self, task):
        return backend_file.select_one(self.connection, task, user_name=self.user_name)

    def read_tasks(self):
        return backend_file.select_all(self.connection, user_name=self.user_name)

    def update_task(self, name, description):
        backend_file.update_one(self.connection, name, description, user_name=self.user_name)

    def delete_task(self, task):
        backend_file.delete_one(self.connection, task, user_name=self.user_name)


class View(object):
    def __init__(self):
        pass


class Controller(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view
