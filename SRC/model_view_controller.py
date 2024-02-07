from tkinter import *
from tkinter import messagebox
import to_do_app_backend as backend_file


class Model(object):
    def __init__(self, name: str):
        self._user_name: str = name
        self._connection: str = backend_file.connect_to_db(name)
        backend_file.create_table(self._connection, self._user_name)

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

    def read_tasks(self):
        return backend_file.select_all(self.connection, user_name=self.user_name)

    def delete_task(self, task):
        backend_file.delete_one(self.connection, task, user_name=self.user_name)


class View(object):

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
        task_info_label_string = 'List of Tasks'
        gui = Tk()
        gui.configure(background="light green")
        gui.title("to do app")
        gui.geometry("640x400")

        self.user_name_prompt_label = Label(gui, text=user_name_prompt_string,
                                            background="light green")
        self.user_name_text_field = Entry(gui)

        self.load_user_btn = Button(gui, text="Load User", fg="Black", bg="Red",
                                    command=self.load_user)
        self.add_user_btn = Button(gui, text="Add User", fg="Black", bg="Red",
                                   command=self.add_user)
        self.delete_user_btn = Button(gui, text="Delete User", fg="Black", bg="Red",
                                      command=self.delete_user)

        self.task_info_prompt_label = Label(gui, text=task_description_prompt_string,
                                            background="light green")
        self.task_info_text_field = Entry(gui)
        self.task_name_prompt_label = Label(gui, text=task_name_prompt_string,
                                            background="light green")
        self.task_name_text_field = Entry(gui)
        self.text_info_label = Label(gui, text=task_info_label_string, background="light green")
        self.task_info_text_area = Text(gui, height=20, width=50)

        self.add_task_btn = Button(gui, text="Add task", fg="Black", bg="Red",
                                   command=self.add_task)
        self.update_task_btn = Button(gui, text="Update task", fg="Black", bg="Red",
                                      command=self.update_task)
        self.delete_task_btn = Button(gui, text="Delete Task", fg="Black", bg="Red",
                                      command=self.delete_task)

        self.exit_btn = Button(gui, text="Exit", fg="Black", bg="Red", command=exit)

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
        gui.mainloop()

    def input_error(self):
        if self.task_info_text_field.get() == '' or self.task_name_text_field.get() == '':
            messagebox.showerror("Empty error",
                                 message="task name and description can not be blank")
            return True
        return False

    def load_user(self):
        user_name = self.user_name_text_field.get()
        if len(user_name) == 0:
            messagebox.showerror("empty user name", message="user name field must not be blank")
            return
        self.model = Model(user_name)
        self.view.update_tasks_window(self.task_info_text_area, self.model.read_tasks())

    def add_user(self):
        user_name = self.user_name_text_field.get()
        if len(user_name) == 0:
            messagebox.showerror("empty user name", message="user name field must not be blank")
            return
        self.model = Model(user_name)
        self.view.update_tasks_window(self.task_info_text_area, self.model.read_tasks())

    def delete_user(self):
        pass

    def add_task(self):
        if self.input_error():
            return
        task_name = self.task_name_text_field.get()
        task_description = self.task_info_text_field.get()
        self.model.create_task(task_name, task_description)
        self.view.update_tasks_window(self.task_info_text_area,
                                      self.model.read_tasks())
        self.task_info_text_field.delete(0, END)
        self.task_name_text_field.delete(0, END)

    def update_task(self):
        task_description: str = self.task_info_text_field.get()
        task_name = self.task_name_text_field.get()
        if len(task_description) == 0 or len(task_name) == 0:
            messagebox.showerror("empty text box",
                                 message="both task name and description must not be blank")
            return
        self.model.delete_task(task_name)
        self.model.create_task(task_name, task_description)
        self.view.update_tasks_window(self.task_info_text_area,
                                      self.model.read_tasks())
        self.task_name_text_field.delete(0, END)
        self.task_info_text_field.delete(0, END)

    def delete_task(self):
        content: str = self.task_name_text_field.get()
        if len(content) == 0:
            messagebox.showerror("task name error", message="task name must not be blank")
            return
        if len(self.model.read_tasks()) == 0:
            messagebox.showerror("No task", message="task list was empty")
            return
        self.task_name_text_field.delete(0, END)
        self.model.delete_task(content)
        self.view.update_tasks_window(self.task_info_text_area,
                                      self.model.read_tasks())


if __name__ == '__main__':
    model = Model('to_do_data_base')
    view = View()
    Controller(model, view)
