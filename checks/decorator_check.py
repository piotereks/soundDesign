def logging(func):
    def inner():
        print("Before func")
        func()
        print('xxxx: ', func.__name__)
        print("after func")
    return inner

@logging
def test1():
    print("test1x")
    print("uhm: ",test1.__name__)
    print("dir: ",dir(test1))
    print("xxxxx1: ",test1.__class__)

@logging
def test2():
    print("test2x")
    print("buu: ", __name__)

def blah():
    print(__name__)


test1()
# test2()
print("something")
blah()