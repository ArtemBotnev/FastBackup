# Fast backup
# Copyright Artem Botnev 2019
# MIT License

import xml.etree.ElementTree as p
import constants as c
from entities import CopyTask


class Parser:
    _directories = []

    def __init__(self, file_name):
        file_full_path = c.FILE_PATH + '/' + file_name + c.XML_POSTFIX
        root = p.parse(file_full_path).getroot()

        for task in root.findall('./copytask'):
            task = CopyTask(task.attrib['source'], task.attrib['destination'], [])
            self._directories.append(task)

    @property
    def directories(self):
        return self._directories
