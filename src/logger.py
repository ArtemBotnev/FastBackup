# Fast backup
# Copyright Artem Botnev 2019-2020
# MIT License

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import constants as c


class Logger:
    _executor = ThreadPoolExecutor(max_workers=1)
    _dir = Path(c.LOGS_DIR)
    _timestamp = None
    _file_path = None
    _file = None

    def __init__(self, timestamp):
        self._timestamp = timestamp
        if not self._dir.exists():
            self._dir.mkdir()

    def writeLog(self, string):
        self._executor.submit(self._write, string)

    def close(self):
        self._executor.submit(self._close)

    def _write(self, string):
        if self._file_path is None:
            self._file_path = self._dir.joinpath(self._timestamp + c.LOG_POSTFIX)
            self._file = self._file_path.open("w", encoding="utf-8")
        self._file.write(string.strip() + '\n')

    def _close(self):
        self._file.close()
