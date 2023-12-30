import inspect
import snoop

def log_call():
    snoop.pp(inspect.stack()[1][3])
