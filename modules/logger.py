import sys
from enum import Enum


class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    NONE = 4


__log_level = LogLevel.DEBUG
__log_fd = sys.stdout


def set_log_level(level):
    global __log_level
    __log_level = level


def set_log_file(filename):
    global __log_fd
    try:
        __log_fd = open(filename, "wb")
    except IOError:
        __log_fd = sys.stdout
        log_warn("Unable to create %s, using standard ouput")


def log_debug(s):
    global __log_level
    if __log_level.value < LogLevel.INFO.value:
        __log_fd.write('{:<7}'.format("[Dbg]") + s + "\n")
        sys.stdout.flush()


def log_info(s):
    global __log_level
    if __log_level.value <= LogLevel.WARNING.value:
        __log_fd.write('{:<7}'.format("[Info]") + s + "\n")
        sys.stdout.flush()


def log_warn(s):
    global __log_level
    if __log_level.value <= LogLevel.ERROR.value:
        __log_fd.write('{:<7}'.format("[Warn]") + s + "\n")
        sys.stdout.flush()


def log_err(s):
    global __log_level
    if __log_level.value <= LogLevel.NONE.value:
        __log_fd.write('{:<7}'.format("[Err]") + s + "\n")
        sys.stdout.flush()
