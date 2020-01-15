# Fast backup
# Copyright Artem Botnev 2019
# MIT License

from sys import argv
import errno
import os
import constants as c
from pathlib import *
from shutil import copy
from src.utils import *
from entities import CopyTask


class TaskRunner:
    _task = None
    _report = {}

    _source_dir_count = 0
    _source_files_count = 0
    _copied_files_count = 0
    _updated_files_count = 0
    _data_size = 0

    _is_new_dir = False

    def execute(self, task):
        self._task = task

        self._report[c.HEAD] = '\n' + 'Copy data from %s to %s' % (task.source, task.destination) + '\n'
        source_path = Path(task.source).expanduser()

        if not source_path.exists():
            # print('Source directory doesn\'t exist')
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), source_path)

        dist_path = Path(task.destination).expanduser()
        if source_path.is_dir():
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
        if not p.exists():
            message = format(
                'directory %s doesn\'t exist, would you like to create it? press y(yes), n(no)' % self._task.destination
            )
            answer = input(message)
            if answer == 'y' or answer == 'Y':
                self._is_new_dir = True
                self._create_dir(p)
            elif answer == 'n' or answer == 'N':
                print('Destination directory doesn\'t exist')
                exit(0)
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
        dist_file_path = destination

        if dist_file_path.exists():
            if self._is_new_dir or dist_file_path.stat().st_mtime < file.stat().st_mtime:
                copy(file.absolute(), dist_file_path)
                self._updated_files_count += 1
                self._data_size += file.stat().st_size
        else:
            dist_dir = dist_file_path.parent
            self._create_dir(dist_dir)
            copy(file.absolute(), dist_dir)
            self._copied_files_count += 1
            self._data_size += file.stat().st_size
