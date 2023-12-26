# __main__.py
print('in main')
print('main name: ', __name__)

from tracker.app.main import *

if __name__ == '__main__':
    print('in main main block')
    main()
else:
    print('in main else block')
