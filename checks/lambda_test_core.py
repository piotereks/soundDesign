import inspect
import pprint
global xxx
xxx = inspect.stack()
def xwhoami_print():
    print('proc:' + inspect.stack()[1][3])



def whoami_print():
    print("hello, I'm %s, daddy is %s" % (whoami(), whosdaddy()))
    # pprint.pprint(inspect.stack()[2])


def whoami():
    return inspect.stack()[2][3]


def whosdaddy():
    return inspect.stack()[3][3]



def beat1():
    whoami_print()

def beat2():
    whoami_print()


def beat_none():
    whoami_print()


beat = beat_none
# def lam():
#     return lambda : beat()
lam = lambda: beat()

print('beat1', beat1)
beat1()

print('beat2', beat2)
beat2()

print('beat_none', beat_none)
beat_none()
print('beat', beat)
beat()
print('lam', lam)
lam()
print('beat=beat1')
print('BegA')
pprint.pprint(inspect.getmembers(lam))
print('EndA')
beat=beat1
print('BegB')
pprint.pprint(inspect.getmembers(lam))
print('EndB')
print('beat', beat1)
beat()
print('lam', lam)
lam()
print('lam = lambda:beat()')
# lam  = lambda : beat()

print('beat', beat)
beat()
print('lam', lam)
lam()


print('---')


