class DirectoryItem:

    def __init__(self, directory, excluded_list):
        self._directory = directory
        self._excluded_list = excluded_list

    @property
    def directory(self):
        return self._directory

    @property
    def excluded_list(self):
        return self._excluded_list
