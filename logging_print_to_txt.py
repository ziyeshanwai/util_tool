import sys
import time

class Logger(object):
    def __init__(self, filename='default.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


if __name__ == '__main__':
    t1 = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    sys.stdout = Logger('./log/a-{}.log'.format(t1), sys.stdout)
    sys.stderr = Logger('./log/a-{}.log'.format(t1), sys.stderr)  # redirect std err, if necessary

    while True:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        c = 5/0
        print("hello ...")