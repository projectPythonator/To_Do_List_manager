from tkinter import *
from tkinter import messagebox
import to_do_app_backend as backend_file


class Model(object):
    def __init__(self, name: str):
        self._user_name = name
        self._connection = backend_file.connect_to_db(name)
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

    def update_tasks_window(self, obj, tasks):
        obj.delete(1.0, END)
        for key, num, task in tasks:
            obj.insert('end -1 chars', "[{}] {}\n".format(num, task))


class Controller(object):
    def __init__(self, mod, viw):
        self.counter = 0
        self.model: Model = mod
        self.view: View = viw
        gui = Tk()
        gui.configure(background="light green")
        gui.title("to do app")
        gui.geometry("640x400")

        self.user_name_prompt_label = Label(gui, text='enter user name here',
                                            background="light green")
        self.user_name_text_field = Entry(gui)

        self.load_user_btn = Button(gui, text="Load User", fg="Black", bg="Red",
                                    command=self.load_user)
        self.add_user_btn = Button(gui, text="Add User", fg="Black", bg="Red",
                                   command=self.add_user)
        self.delete_user_btn = Button(gui, text="Delete User", fg="Black", bg="Red",
                                      command=self.delete_user)

        self.task_info_prompt_label = Label(gui, text='enter task to add here',
                                            background="light green")
        self.task_info_text_field = Entry(gui)
        self.task_name_prompt_label = Label(gui, text='enter task name', background="light green")
        self.task_name_text_field = Entry(gui)
        self.task_info_text_area = Text(gui, height=20, width=50)

        self.task_num_prompt_label = Label(gui, text='enter task number here to delete or update',
                                           background="light green")
        self.task_update_prompt_label = Label(gui, text='enter updated content here',
                                              background="light green")
        self.task_num_text_field = Entry(gui)
        self.task_update_text_field = Entry(gui)

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

        self.task_num_prompt_label.grid(row=10, column=0)
        self.task_num_text_field.grid(row=11, column=0)

        self.task_update_prompt_label.grid(row=12, column=0)
        self.task_update_text_field.grid(row=13, column=0)

        self.update_task_btn.grid(row=14, column=0)
        self.delete_task_btn.grid(row=15, column=0)
        self.task_info_text_area.grid(row=0, column=1, rowspan=14)
        self.exit_btn.grid(row=16, column=0)
        self.view.update_tasks_window(self.task_info_text_area, self.model.read_tasks())
        gui.mainloop()

    def input_error(self):
        if self.task_info_text_field.get() == '' or self.task_name_text_field == '':
            messagebox.showerror("Empty error")
            return True
        return False

    def load_user(self):
        user_name = self.user_name_text_field.get()
        if len(user_name) == 0:
            messagebox.showerror("empty user name")
            return
        self.model = Model(user_name)
        self.view.update_tasks_window(self.task_info_text_area, self.model.read_tasks())

    def add_user(self):
        user_name = self.user_name_text_field.get()
        if len(user_name) == 0:
            messagebox.showerror("empty user name")
            return
        self.model = Model(user_name)
        self.view.update_tasks_window(self.task_info_text_area, self.model.read_tasks())

    def delete_user(self):
        pass

    def add_task(self):
        if self.input_error():
            return
        name = self.task_name_text_field.get()
        content = self.task_info_text_field.get()
        self.model.create_task(name, content)
        self.view.update_tasks_window(self.task_info_text_area,
                                      self.model.read_tasks())
        self.task_info_text_field.delete(0, END)
        self.task_name_text_field.delete(0, END)

    def update_task(self):
        name = self.task_update_text_field.get()
        content = self.task_num_text_field.get()
        if len(content) == 0 or len(name) == 0:
            messagebox.showerror("empty key")
            return
        self.model.update_task(name, content)
        self.view.update_tasks_window(self.task_info_text_area,
                                      self.model.read_tasks())
        self.task_update_text_field.delete(0, END)
        self.task_num_text_field.delete(0, END)

    def delete_task(self):
        tasks = self.model.read_tasks()
        if len(tasks) == 0:
            messagebox.showerror("No task")
            return
        content = self.task_num_text_field.get()
        if len(content) == 0:
            messagebox.showerror("empty key")
            return
        self.task_num_text_field.delete(0, END)
        self.model.delete_task(content)
        self.view.update_tasks_window(self.task_info_text_area,
                                      self.model.read_tasks())


if __name__ == '__main__':
    model = Model('Agis')
    view = View()
    Controller(model, view)
