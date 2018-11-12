# -*- coding: utf-8 -*-


import logging
import datetime


class SimpleLogger:
    def __init__(self, log_path):
        self._log_path = log_path
        self._log_fo = open(log_path, 'w', encoding='utf-8')
        self._log_level = logging.INFO
        self.use_cache = False
        self._cache = ['' for i in range(700000)]
        self._idx = 0

    def __del__(self):
        self.close()

    def close(self):
        if self._log_fo:
            self._log_fo.close()
            self._log_fo = None

    @property
    def log_level(self):
        return self._log_level

    @log_level.setter
    def log_level(self, val):
        self._log_level = val

    def _log_head(self, log_level):
        now = datetime.datetime.now()
        time_part = now.strftime('%Y-%m-%d %H:%M:%S.%f')
        level_part = logging.getLevelName(log_level)
        return ' | '.join((time_part, level_part)) + ' | '

    def _write_log_head(self, log_level):
        self._log_fo.write(self._log_head(log_level))

    def _write_log_line(self, log_level, msg=''):
        assert self._log_fo

        if log_level < self._log_level:
            return

        line = ''.join((self._log_head(log_level), msg, '\n'))
        # line = str(datetime.datetime.now().timestamp()) + ' ' + msg + '\n'
        if self.use_cache:
            self._cache[self._idx] = line
            self._idx += 1
        else:
            self._log_fo.write(line)
            # self.flush()

    def flush(self):
        if self.use_cache:
            for line in self._cache:
                self._log_fo.write(line)
            self._cache.clear()
        self._log_fo.flush()

    def info(self, msg=''):
        self._write_log_line(logging.INFO, msg)

    def debug(self, msg=''):
        self._write_log_line(logging.DEBUG, msg)

    def warning(self, msg=''):
        self._write_log_line(logging.WARNING, msg)

    def error(self, msg=''):
        self._write_log_line(logging.ERROR, msg)

    def write_raw(self, msg=''):
        self._log_fo.write(msg)
        if not msg.endswith('\n'):
            self._log_fo.write('\n')