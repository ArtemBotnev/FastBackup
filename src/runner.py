# Fast backup
# Copyright Artem Botnev 2019-2020
# MIT License

import errno
import os
import constants as c
from pathlib import *
from shutil import copy
from utils import *


class TaskRunner:
    _task = None
    _action = None
    _excluded_paths = set
    _settings = {}

    _source_dir_count = 0
    _source_files_count = 0
    _copied_files_count = 0
    _updated_files_count = 0
    _data_size = 0

    _root_is_file = False

    def __init__(self, settings):
        self._settings = settings

    def execute(self, task, action):
        self._task = task
        self._action = action

        source_path = Path(task.source).expanduser()
        self._excluded_paths = set(map(lambda e: source_path.joinpath(e), self._task.excluded_list))

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

        return Report(
            timer.get_task_duration(),
            self._source_dir_count,
            self._source_files_count,
            self._copied_files_count,
            self._updated_files_count,
            self._data_size
        )

    def _create_dir(self, p):
        try:
            p.mkdir(parents=True, exist_ok=True)
        except OSError:
            print('Creation of the directory %s failed, check path name and try again' % self._task.destination)

    def _check_path(self, p):
        if not p.exists():
            if self._root_is_file:
                p = p.parent
            self._create_dir(p)

    def _copy_tree(self, source, destination):
        if self._is_path_excluded(source):
            return

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
            if self._settings[c.CHECK_ONLY_BY_NAME]:
                self._action(format('Skipped: file: %s in directory %s already exist.' % (file.name, destination)))
            elif destination.stat().st_mtime < file.stat().st_mtime:
                self._copy_and_increment(file, destination, False)
            else:
                self._action(format(
                    'Skipped: file %s in directory %s is newer than one from source directory.'
                    % (file.name, destination)
                ))
        else:
            destination = destination.parent
            self._create_dir(destination)
            self._copy_and_increment(file, destination, True)

    def _copy_and_increment(self, sour, des, is_new):
        copy(sour.absolute(), des)
        if is_new:
            self._copied_files_count += 1
            self._action(format('Copied: file %s to -> %s' % (sour, des.parent)))
        else:
            self._updated_files_count += 1
            self._action(format('Updated: file %s in %s' % (sour, des.parent)))
        self._data_size += sour.stat().st_size

    def _is_path_excluded(self, path):
        if self._excluded_paths.__contains__(path):
            if path.is_dir():
                p = 'directory'
            else:
                p = 'file'
            self._action(format('Skipped: %s %s is excluded.' % (p, path)))
            return True
        else:
            return False


class Report:
    time_sec = .0
    source_dir_count = 0
    source_files_count = 0
    copied_files_count = 0
    updated_files_count = 0
    data_size = 0

    def __init__(
            self,
            time_sec,
            source_dir_count,
            source_files_count,
            copied_files_count,
            updated_files_count,
            data_size
    ):
        self.time_sec = time_sec
        self.source_dir_count = source_dir_count
        self.source_files_count = source_files_count
        self.copied_files_count = copied_files_count
        self.updated_files_count = updated_files_count
        self.data_size = data_size


class Receiver:
    _total_time_sec = .0
    _total_source_dir_count = 0
    _total_source_files_count = 0
    _total_copied_files_count = 0
    _total_updated_files_count = 0
    _total_data_size = 0

    def append(self, report):
        self._total_time_sec += report.time_sec
        self._total_source_dir_count += report.source_dir_count
        self._total_source_files_count += report.source_files_count
        self._total_copied_files_count += report.copied_files_count
        self._total_updated_files_count += report.updated_files_count
        self._total_data_size += report.data_size

    def release(self):
        return Report(
            self._total_time_sec,
            self._total_source_dir_count,
            self._total_source_files_count,
            self._total_copied_files_count,
            self._total_updated_files_count,
            self._total_data_size
        )
