from lambda_test_core import *

print('beat=beat2')
print('BegC')
pprint.pprint(inspect.getmembers(lam))
print('EndC')
beat=beat1
beat = beat2
print('BegD')
pprint.pprint(inspect.getmembers(lam))
print('EndD')
print('beat', beat)
beat()
print('lam', lam)
lam()

print('lam = lambda:beat()')
lam  = lambda : beat()
print('beat', beat)
beat()
print('lam', lam)
lam()