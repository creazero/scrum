import enum


class TaskState(enum.Enum):
    todo = 'todo'
    in_process = 'in_process'
    testing = 'testing'
    done = 'done'
