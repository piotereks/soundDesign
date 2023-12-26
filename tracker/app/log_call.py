import inspect


def log_call():
    print(inspect.stack()[1][3])
    # for xxx in inspect.stack():
    #     print(xxx[1],xxx[2],xxx[3])
