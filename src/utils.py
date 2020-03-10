# Fast backup
# Copyright Artem Botnev 2019-2020
# MIT License

import time
from datetime import datetime
import constants as c


class Timer:
    _start_time = 0
    _finish_time = 0

    @staticmethod
    def get_current_time_str():
        return datetime.now().strftime(c.TIME_PATTERN)

    @staticmethod
    def get_time_stamp():
        return datetime.now().strftime(c.TIME_STAMP_PATTERN)

    @staticmethod
    def show_time(seconds):
        sec = float(seconds) % 60
        sec_string = format('%.2f seconds' % sec)
        minutes = int(seconds) // 60
        minutes_string = ''
        hours_string = ''
        if minutes > 0:
            hours = minutes // 60
            minutes %= 60
            minutes_string = format('%d minutes ' % minutes)
            if hours > 0:
                hours_string = format('%d hours ' % hours)

        return 'It has taken ' + hours_string + minutes_string + sec_string

    def get_task_duration(self):
        return self._finish_time - self._start_time

    def start(self):
        self._start_time = time.time()
        return self

    def stop(self):
        self._finish_time = time.time()
        return self


class DataMeasure:

    @staticmethod
    def show_data_size(count):
        m = ['bytes', 'kB', 'mB', 'gB']

        for s in m:
            result = count / 1024
            if result < 1:
                if s == 'bytes':
                    return format('%.0f %s' % (count, s))
                else:
                    return format('%.3f %s' % (count, s))
            else:
                count = result

        return format('%.3f tB' % count)