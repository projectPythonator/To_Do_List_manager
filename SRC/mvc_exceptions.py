
class TaskByNameAlreadyExistsOnCreation(Exception):
    pass


class TaskRemovedDoesNotExist(Exception):
    pass


class TaskNameOnUpdateDoesNotExist(Exception):
    pass


class TaskNameOnReadDoesNotExist(Exception):
    pass
