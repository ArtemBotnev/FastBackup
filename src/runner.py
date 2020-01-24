# Fast backup
# Copyright Artem Botnev 2019
# MIT License

import errno
import os
import constants as c
from pathlib import *
from shutil import copy
from utils import *


class TaskRunner:
    _task = None
    _report = {}

    _source_dir_count = 0
    _source_files_count = 0
    _copied_files_count = 0
    _updated_files_count = 0
    _data_size = 0

    _root_is_file = False

    def execute(self, task):
        self._task = task

        self._report[c.HEAD] = '\n' + 'Copy data from %s to %s' % (task.source, task.destination) + '\n'
        source_path = Path(task.source).expanduser()

        if not source_path.exists():
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), source_path)

        dist_path = Path(task.destination).expanduser()

        if source_path.is_file():
            self._root_is_file = True

        dist_path = dist_path.joinpath(PurePath(source_path).name)

        self._check_path(dist_path)

        timer = Timer().start()
        self._copy_tree(source_path, dist_path)
        timer.stop()

        self._report[c.DURATION] = timer.show_time()
        self._report[c.SOURCE_DIR_COUNT] = format('Total count of source packages:  %d' % self._source_dir_count)
        self._report[c.SOURCE_FILES_COUNT] = format('Total count of source files:     %d' % self._source_files_count)
        self._report[c.COPIED_FILES_COUNT] = format('Total count of copied files:     %d' % self._copied_files_count)
        self._report[c.UPDATED_FILES_COUNT] = format('Total count of updated files:    %d' % self._updated_files_count)
        self._report[c.DATA_SIZE] = format(
            'Total copied data:               %s' % DataMeasure.show_data_size(self._data_size)
        )

        return self._report

    def _create_dir(self, p):
        try:
            p.mkdir(parents=True, exist_ok=True)
        except OSError:
            print('Creation of the directory %s failed, check path name and try again' % self._task.destination)

    def _check_path(self, p):
        first_word = 'directory'
        if self._root_is_file:
            first_word = 'file'

        if not p.exists():
            message = format(
                '%s %s doesn\'t exist, would you like to create it? press y(yes), n(no)' % (first_word, p)
            )
            answer = input(message)
            if answer == 'y' or answer == 'Y':
                if self._root_is_file:
                    p = p.parent
                self._create_dir(p)
            elif answer == 'n' or answer == 'N':
                print('Destination directory doesn\'t exist')
            else:
                self._check_path(p)

    def _copy_tree(self, source, destination):
        if source.is_dir():
            self._source_dir_count += 1
            for path in source.iterdir():
                pure_path = PurePath(path).name
                self._copy_tree(path, destination.joinpath(pure_path))
        else:
            self._copy_file(source, destination)

    def _copy_file(self, file, destination):
        self._source_files_count += 1

        if destination.exists():
            if destination.stat().st_mtime < file.stat().st_mtime:
                self._copy_and_increment(file, destination, False)
        else:
            destination = destination.parent
            self._create_dir(destination)
            self._copy_and_increment(file, destination, True)

    def _copy_and_increment(self, sour, des, is_new):
        copy(sour.absolute(), des)
        if is_new:
            self._copied_files_count += 1
        else:
            self._updated_files_count += 1
        self._data_size += sour.stat().st_size
