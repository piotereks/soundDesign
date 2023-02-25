
from checks.pyt.app.procs import *


def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 5

def test_answerx():
    assert inc(4) == 5

def test_xxx():
    assert stand_proc() == "stand_proc"