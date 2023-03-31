import sys
from http_log_monitoring import Dispatcher

if __name__ == '__main__':
    Dispatcher(sys.argv[1]).run()