class MaxClass():
    par1 = 5
    par2 ='abc'

    def meth_signle(self):
        log_call()
        return __name__

    def meth_par(self):
        log_call()
        def meth_kid():
            log_call()
            return __name__

        meth_kid()
        return __name__


clasy = MaxClass()

clasy.meth_signle()
print()
clasy.meth_par()


