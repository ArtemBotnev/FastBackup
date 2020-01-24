# Fast backup
# Copyright Artem Botnev 2019
# MIT License

# Requires python version 3.5 or higher
# Copies all new and updated source directory files to destination directory
# (checks if each file already exist in destination directory and copy only if
# doesn't or has been updated)
# Copies full directories tree
# Exclude empty folders

import constants as c
from parser import Parser
from runner import TaskRunner


def print_report(r):
    print()
    print(r[c.HEAD])
    print(r[c.DURATION])
    print()
    print(r[c.SOURCE_DIR_COUNT])
    print(r[c.SOURCE_FILES_COUNT])
    print(r[c.COPIED_FILES_COUNT])
    print(r[c.UPDATED_FILES_COUNT])
    print(r[c.DATA_SIZE])
    print()


print()
print('STARTED')

tasks = Parser(c.DIRECTORIES).directories
for t in tasks:
    try:
        report = TaskRunner().execute(t)
        print_report(report)
    except FileNotFoundError:
        print('Source directory %s doesn\'t exist' % t.source)

print('FINISHED')
