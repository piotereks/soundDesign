import inspect


def log_call():
    print(inspect.stack()[1][3])
