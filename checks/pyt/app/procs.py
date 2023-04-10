def stand_proc():
    log_call()
    return __name__

def par_proc():
    log_call()

    def child_proc():
        log_call()
        return __name__

    def test_child_procx():
        assert 1 == 'child_proc'

    child_proc()
    return __name__


def test_child_proc():
    assert 1 == 'child_proc'

def g_par_proc():
    log_call()

    def in_par_proc():
        log_call()
        def g_child():
            log_call()
            return __name__

        g_child()
        return __name__

    in_par_proc()
    return __name__


stand_proc()
print()
par_proc()
print()
g_par_proc()