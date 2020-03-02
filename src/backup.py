# Fast backup
# Copyright Artem Botnev  2019-2020
# MIT License

# Requires python version 3.5 or higher
# Copies all new and updated source directory files to destination directory
# (checks if each file already exist in destination directory and copy only if
# doesn't or has been updated)
# Copies full directories tree
# Exclude empty folders

import constants as c
from mparser import Parser
from runner import TaskRunner
from logger import Logger
from utils import Timer


def verbose_action(s):
    print(s)
    if settings[c.LOGGING]:
        logger.writeLog(s)


def do_nothing(s):
    pass


def print_report(r):
    rep = \
        r[c.HEAD] + '\n' + r[c.DURATION] + '\n\n' \
        + r[c.SOURCE_DIR_COUNT] + '\n' + r[c.SOURCE_FILES_COUNT] + '\n' \
        + r[c.COPIED_FILES_COUNT] + '\n' + r[c.UPDATED_FILES_COUNT] + '\n' + r[c.DATA_SIZE] + '\n\n'

    print(rep)

    if settings[c.LOGGING]:
        logger.writeLog(rep)


parser = Parser().parse_tasks(c.DIRECTORIES).parse_settings(c.SETTINGS)
tasks = parser.tasks
logger = Logger(Timer.get_time_stamp())
settings = parser.settings

start_log = '\nSTARTED at %s\n' % Timer.get_current_time()
print(start_log)
if settings[c.LOGGING]:
    logger.writeLog(start_log)

for t in tasks:
    try:
        a = do_nothing
        if settings[c.VERBOSE]:
            a = verbose_action

        report = TaskRunner(settings).execute(t, a)
        print_report(report)
    except FileNotFoundError:
        print('Source directory %s doesn\'t exist' % t.source)

finish_log = 'FINISHED at %s' % Timer.get_current_time()
print(finish_log)
if settings[c.LOGGING]:
    logger.writeLog(finish_log)

logger.close()
