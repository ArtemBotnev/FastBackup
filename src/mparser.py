# Fast backup
# Copyright Artem Botnev 2019-2020
# MIT License

import xml.etree.ElementTree as p
import constants as c
from entities import CopyTask


class Parser:
    _tasks = []
    _settings = {}

    def __init__(self):
        pass

    def parse_tasks(self, file_name):
        for task in self._get_items(file_name, './copytask'):
            excluded = task.find('excluded')
            if excluded is not None:
                excluded = task.find('excluded').findall('item')
                excluded = list(map(lambda e: e.text, excluded))
            else:
                excluded = []
            task = CopyTask(task.attrib['source'], task.attrib['destination'], excluded)
            self._tasks.append(task)
        return self

    def parse_settings(self, file_name):
        for prop in self._get_items(file_name, './property'):
            self._settings[prop.attrib['key']] = prop.attrib['value'] == c.TRUE
        return self

    def _get_items(self, file_name, item_name):
        file_full_path = file_name + c.XML_POSTFIX
        return p.parse(file_full_path).getroot().findall(item_name)

    @property
    def tasks(self):
        return self._tasks

    @property
    def settings(self):
        return self._settings
