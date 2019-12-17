# Fast backup
# Copyright Artem Botnev 2019
# MIT License

class CopyTask:

    def __init__(self, source, destination, excluded_list):
        self._source = source
        self._destination = destination
        self._excluded_list = excluded_list

    @property
    def source(self):
        return self._source

    @property
    def destination(self):
        return self._destination

    @property
    def excluded_list(self):
        return self._excluded_list
