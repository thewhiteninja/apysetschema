import csv
import glob
import os
import sys

from modules import logger
from modules.apisetschema import ApiSetSchema
from modules.logger import set_log_level, LogLevel
from modules.utils import welcome

OPTIONS = { }


def usage():
    print("Usage: " + os.path.basename(sys.argv[0]) + ' [options]')
    print()
    print("Options:")
    print("      -h, --help      : Show help")
    print("      -f, --file      : Input file (apisetschema.dll)")
    print("      --test          : Dump all DLL files from /data")
    print()
    sys.exit(0)


def parse_args():
    global OPTIONS
    i = 1
    while i < len(sys.argv):
        try:
            if sys.argv[i] in ["-h", "--help"]:
                usage()
            elif sys.argv[i] in ["-f", "--file"]:
                OPTIONS["file"] = sys.argv[i + 1]
                i += 1
            elif sys.argv[i] in ["--test"]:
                OPTIONS["test"] = True
        except IndexError:
            usage()
        i += 1


def main():
    welcome()
    set_log_level(LogLevel.DEBUG)
    parse_args()
    if OPTIONS.setdefault("test", False):
        test()
    elif OPTIONS.setdefault("file", None) is not None:
        api = ApiSetSchema(OPTIONS["file"])
        logger.log_info("Version: %d" % api.version)
        logger.log_info("Count: %d" % api.count)
        for entry in api.entries:
            for value in entry.values:
                logger.log_info("%s -> %s" % (entry.name, value.value))
    else:
        usage()


def test():
    welcome()
    set_log_level(LogLevel.DEBUG)

    for sample in glob.glob("data/*.dll"):
        api = ApiSetSchema(sample)
        logger.log_info("Version: %d" % api.version)
        logger.log_info("Count: %d" % api.count)
        logger.log_info("Writing entries to " + sample + ".txt")

        with open(sample + ".csv", "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['Name', 'Value'], delimiter=';')
            writer.writeheader()
            for entry in api.entries:
                for value in entry.values:
                    writer.writerow({ "Name": entry.name, "Value": value.value })


if __name__ == '__main__':
    main()
