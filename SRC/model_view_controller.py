from tkinter import *
import tkinter.messagebox
import to_do_app_backend as backend_file
import mvc_exceptions as mvc_exc


class Model(object):
    def __init__(self, name: str, tasks):
        self._user_name = name
        self._connection = backend_file.connect_to_db(name)
        backend_file.create_table(self._connection, self._user_name)
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

    @staticmethod
    def show_tasks(display, user, tasks):
        pass

    def show_tasks(self, user, task):
        pass

    def display_missing_task(self, task, err):
        pass


class Controller(object):
    def __init__(self, mod, viw):
        self.model: Model = mod
        self.view: View = viw
        gui = Tk()
        gui.configure(background="light green")
        gui.title("to do app")
        gui.geometry("640x400")

        user_name_prompt_label = Label(gui, text='enter user name here', background="light green")
        user_name_text_field = Entry(gui)

        load_user_btn = Button(gui, text="Load User", fg="Black", bg="Red", command=self.load_user)
        add_user_btn = Button(gui, text="Add User", fg="Black", bg="Red", command=self.add_user)
        delete_user_btn = Button(gui, text="Delete User", fg="Black", bg="Red",
                                 command=self.delete_user)

        task_inf_prompt_label = Label(gui, text='enter task to add here', background="light green")
        task_inf_text_field = Entry(gui)
        task_info_text_area = Text(gui, height=20, width=50)

        task_num_prompt_label = Label(gui, text='enter task number here to delete or update',
                                      background="light green")
        task_update_prompt_label = Label(gui, text='enter updated content here',
                                         background="light green")
        task_num_text_field = Entry(gui)
        task_update_text_field = Entry(gui)

        add_task_btn = Button(gui, text="Add task", fg="Black", bg="Red", command=self.add_task)
        update_task_btn = Button(gui, text="Update task", fg="Black", bg="Red",
                                 command=self.update_task)
        delete_task_btn = Button(gui, text="Delete Task", fg="Black", bg="Red",
                                 command=self.delete_task)

        exit_btn = Button(gui, text="Exit", fg="Black", bg="Red", command=exit)

        user_name_prompt_label.grid(row=0, column=0)
        user_name_text_field.grid(row=1, column=0)
        load_user_btn.grid(row=2, column=0)
        add_user_btn.grid(row=3, column=0)
        delete_user_btn.grid(row=4, column=0)

        task_inf_prompt_label.grid(row=5, column=0)
        task_inf_text_field.grid(row=6, column=0)
        add_task_btn.grid(row=7, column=0)

        task_num_prompt_label.grid(row=8, column=0)
        task_num_text_field.grid(row=9, column=0)

        task_update_prompt_label.grid(row=10, column=0)
        task_update_text_field.grid(row=11, column=0)

        update_task_btn.grid(row=12, column=0)
        delete_task_btn.grid(row=13, column=0)
        task_info_text_area.grid(row=0, column=1, rowspan=14)
        exit_btn.grid(row=14, column=0)
        gui.mainloop()

    def load_user(self):
        pass

    def add_user(self):
        pass

    def delete_user(self):
        pass

    def add_task(self):
        pass

    def update_task(self):
        pass

    def delete_task(self):
        pass


if __name__ == '__main__':
    model = Model('Agis', {})
    view = View()
    Controller(model, view)
