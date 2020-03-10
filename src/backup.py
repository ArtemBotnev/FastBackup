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
from runner import *
from logger import Logger
from utils import *


def create_header(rep, is_total_report):
    if is_total_report:
        report_prefix = 'Total count'
    else:
        report_prefix = 'Count'

    time = Timer.show_time(rep.time_sec)
    source_dir_count = format('%s of source packages:  %d' % (report_prefix, rep.source_dir_count))
    source_files_count = format('%s of source files:     %d' % (report_prefix, rep.source_files_count))
    copied_files_count = format('%s of copied files:     %d' % (report_prefix, rep.copied_files_count))
    updated_files_count = format('%s of updated files:    %d' % (report_prefix, rep.updated_files_count))
    data_size = format(
        '%s of copied data:      %s' % (report_prefix, DataMeasure.show_data_size(rep.data_size))
    )

    return Report(
        time,
        source_dir_count,
        source_files_count,
        copied_files_count,
        updated_files_count,
        data_size
    )


def verbose_action(s):
    print(s)
    if settings[c.LOGGING]:
        logger.writeLog(s)


def do_nothing(s):
    pass


def print_report(r):
    rep = '\n' + \
          r.time_sec + '\n\n' \
          + r.source_dir_count + '\n' + r.source_files_count + '\n' \
          + r.copied_files_count + '\n' + r.updated_files_count + '\n' + r.data_size + '\n\n'

    print(rep)

    if settings[c.LOGGING]:
        logger.writeLog(rep)


parser = Parser().parse_tasks(c.DIRECTORIES).parse_settings(c.SETTINGS)
tasks = parser.tasks
report_receiver = Receiver()
logger = Logger(Timer.get_time_stamp())
settings = parser.settings

start_log = '\nSTARTED at %s\n' % Timer.get_current_time_str()
print(start_log)
if settings[c.LOGGING]:
    logger.writeLog(start_log)

for t in tasks:
    try:
        a = do_nothing
        if settings[c.VERBOSE]:
            a = verbose_action

        head_message = '\n' + 'Copied data from %s to %s' % (t.source, t.destination) + '\n'
        verbose_action(head_message)
        report = TaskRunner(settings).execute(t, a)
        report_receiver.append(report)
        str_report = create_header(report, False)
        print_report(str_report)
    except FileNotFoundError:
        print('Source directory %s doesn\'t exist' % t.source)

finish_log = 'FINISHED at %s' % Timer.get_current_time_str()
finish_rep = report_receiver.release()
finish_rep = create_header(finish_rep, True)

print(finish_log)
if settings[c.LOGGING]:
    logger.writeLog(finish_log)

print_report(finish_rep)

logger.close()
