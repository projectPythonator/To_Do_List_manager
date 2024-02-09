from tkinter import *
from tkinter import messagebox
import to_do_app_backend as backend_file


class Model(object):
    def __init__(self, db_name: str, user_name: str):
        self._user_name = user_name
        self._connection: backend_file.Connection = backend_file.connect_to_db(db_name)
        self.load_user()

    @property
    def connection(self):
        return self._connection

    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, new_user: str):
        self._user_name = new_user

    def load_user(self):
        backend_file.create_table(self._connection, self._user_name)

    def add_new_user(self, new_user_name):
        self._user_name = new_user_name
        self.load_user()

    def create_task(self, task_name: str, task_description: str):
        backend_file.insert_one(self.connection, task_name, task_description,
                                user_name=self.user_name)

    def read_tasks(self):
        return backend_file.select_all(self.connection, user_name=self.user_name)

    def delete_task(self, task_name: str):
        backend_file.delete_one(self.connection, task_name, user_name=self.user_name)


class View(object):
    def update_user_name_window(self, gui, user_name: str):
        task_label_widget = Label(gui,
                                  text='List of Tasks for {}'.format(user_name),
                                  background="light green")
        task_label_widget.grid(row=0, column=1)

    def update_tasks_window(self, task_list_widget, list_of_tasks):
        """Method clears tasks then writes the new updated tasks to window. Can be optimized."""
        task_list_widget.delete(1.0, END)
        for key, num, task in list_of_tasks:
            task_list_widget.insert('end -1 chars', "[{}]: '{}'\n".format(num, task))


class Controller(object):
    def __init__(self, mod: Model, viw: View):
        self.model: Model = mod
        self.view: View = viw
        user_name_prompt_string = 'enter user name here'
        task_name_prompt_string = 'enter task name here'
        task_description_prompt_string = 'enter task description here'
        task_info_label_string = 'List of Tasks for {}'.format(model.user_name)
        self.gui = Tk()
        self.gui.configure(background="light green")
        self.gui.title("to do app")
        self.gui.geometry("640x400")

        self.user_name_prompt_label = Label(self.gui, text=user_name_prompt_string,
                                            background="light green")
        self.user_name_text_field = Entry(self.gui)

        self.load_user_btn = Button(self.gui, text="Load User", fg="Black", bg="Red",
                                    command=self.load_user)
        self.add_user_btn = Button(self.gui, text="Add User", fg="Black", bg="Red",
                                   command=self.add_user)
        self.delete_user_btn = Button(self.gui, text="Delete User", fg="Black", bg="Red",
                                      command=self.delete_user)

        self.task_info_prompt_label = Label(self.gui, text=task_description_prompt_string,
                                            background="light green")
        self.task_info_text_field = Entry(self.gui)
        self.task_name_prompt_label = Label(self.gui, text=task_name_prompt_string,
                                            background="light green")
        self.task_name_text_field = Entry(self.gui)
        self.text_info_label = Label(self.gui, text=task_info_label_string,
                                     background="light green")
        self.task_info_text_area = Text(self.gui, height=20, width=50)

        self.add_task_btn = Button(self.gui, text="Add task", fg="Black", bg="Red",
                                   command=self.add_task)
        self.update_task_btn = Button(self.gui, text="Update task", fg="Black", bg="Red",
                                      command=self.update_task)
        self.delete_task_btn = Button(self.gui, text="Delete Task", fg="Black", bg="Red",
                                      command=self.delete_task)

        self.exit_btn = Button(self.gui, text="Exit", fg="Black", bg="Red", command=exit)

        self.user_name_prompt_label.grid(row=0, column=0)
        self.user_name_text_field.grid(row=1, column=0)
        self.load_user_btn.grid(row=2, column=0)
        self.add_user_btn.grid(row=3, column=0)
        self.delete_user_btn.grid(row=4, column=0)

        self.task_name_prompt_label.grid(row=5, column=0)
        self.task_name_text_field.grid(row=6, column=0)
        self.task_info_prompt_label.grid(row=7, column=0)
        self.task_info_text_field.grid(row=8, column=0)
        self.add_task_btn.grid(row=9, column=0)

        self.update_task_btn.grid(row=10, column=0)
        self.delete_task_btn.grid(row=11, column=0)
        self.text_info_label.grid(row=0, column=1)
        self.task_info_text_area.grid(row=1, column=1, rowspan=12)
        self.exit_btn.grid(row=16, column=0)
        self.view.update_tasks_window(self.task_info_text_area, self.model.read_tasks())
        self.gui.mainloop()

    def clear_text_entries(self):
        self.user_name_text_field.delete(0, END)
        self.task_info_text_field.delete(0, END)
        self.task_name_text_field.delete(0, END)

    def check_user_name_field(self) -> bool:
        return self.user_name_text_field.get() == ''

    def check_task_name_field(self) -> bool:
        return self.task_name_text_field.get() == ''

    def check_task_info_field(self) -> bool:
        return self.task_info_text_field.get() == ''

    def is_valid_user_name(self) -> bool:
        """Checks on validity of a username entered."""
        if self.check_user_name_field():
            messagebox.showerror("Invalid user name",
                                 message="User name must not be blank.")
            return False
        return True

    def is_valid_task_name(self) -> bool:
        if self.check_task_name_field():
            messagebox.showerror("Invalid Task Name",
                                 message="Task name must not be blank.")
            return False
        return True

    def is_valid_task_description(self) -> bool:
        if self.check_task_info_field():
            messagebox.showerror("Invalid Task Description",
                                 message="Task name must not be blank.")
            return False
        return True

    def load_user(self):
        if self.is_valid_user_name():
            self.model.add_new_user(self.user_name_text_field.get())
            self.view.update_user_name_window(self.gui,
                                              self.user_name_text_field.get())
            self.update_window_and_text_clear()

    def add_user(self):
        if self.is_valid_user_name():
            self.load_user()

    def delete_user(self):
        pass

    def update_window_and_text_clear(self):
        self.view.update_tasks_window(self.task_info_text_area, self.model.read_tasks())
        self.clear_text_entries()

    def add_task(self):
        if self.is_valid_task_name() and self.is_valid_task_description():
            self.model.create_task(self.task_name_text_field.get(), self.task_info_text_field.get())
            self.update_window_and_text_clear()

    def update_task(self):
        if self.is_valid_task_name() and self.is_valid_task_description():
            self.model.delete_task(self.task_name_text_field.get())
            self.add_task()

    def delete_task(self):
        if self.is_valid_task_name():
            self.model.delete_task(self.task_name_text_field.get())
            self.update_window_and_text_clear()


if __name__ == '__main__':
    model = Model('new_data_base', 'Kate')
    view = View()
    Controller(model, view)
