import sys
from dispatcher import Dispatcher

if __name__ == '__main__':
    if len(sys.argv) > 1:
        Dispatcher(sys.argv[1]).run()
    else:
        Dispatcher().run()
