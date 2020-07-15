import os
import platform
import sys
import time


def read_string(data, start, length):
    return data[start:start + length].decode("utf-16-le")


def welcome():
    print("Starting %s at %s (%s version)\n" % (
        os.path.basename(sys.argv[0]), time.asctime(time.localtime(time.time())), platform.architecture()[0]))
