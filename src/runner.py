# Fast backup
# Copyright Artem Botnev 2019
# MIT License

from sys import argv
from pathlib import Path
from shutil import copy
from entities import CopyTask


class TaskRunner:
    _task = None

    _source_dir_count = 0
    _source_files_count = 0
    _copied_files_count = 0
    _updated_files_count = 0
    _data_size = 0

    def execute(self, task):
        self._task = task

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
                self._create_dir(p)
            elif answer == 'n' or answer == 'N':
                print('Destination directory doesn\'t exist')
                exit(0)
            else:
                self._check_path(p)

    def _copy_file(self, file, destination):
        self._source_files_count += 1

        dist_file_path = destination.joinpath(file.relative_to(self._task.source))

        if dist_file_path.exists():
            if dist_file_path.stat().st_mtime < file.stat().st_mtime:
                copy(file.absolute(), dist_file_path)
                self._updated_files_count += 1
                self._data_size += file.stat().st_size
        else:
            dist_dir = dist_file_path.parent
            self._create_dir(dist_dir)
            copy(file.absolute(), dist_dir)
            self._copied_files_count += 1
            self._data_size += file.stat().st_size

    def _copy_tree(self, source, destination):
        if source.is_dir():
            self._source_dir_count += 1
            for path in source.iterdir():
                self._copy_tree(path, destination)
        else:
            self._copy_file(source, destination)