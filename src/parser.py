import xml.etree.ElementTree as p
import constants as c


class Parser:

    def __init__(self, file_name):
        file_full_path = c.FILE_PATH + '/' + file_name + c.XML_POSTFIX
        self._root = p.parse(file_full_path).getroot()
