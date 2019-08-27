# -*- coding: utf-8 -*-

import logging
from datetime import datetime
import os
import platform
import sys

# logger = logging.getLogger('FT')
# log_level = logging.INFO
# is_file_log = True
#
# # 设置logger的level为DEBUG
# logger.setLevel(log_level)
#
# # 创建一个输出日志到控制台的StreamHandler
# hdr = logging.StreamHandler()
# formatter = logging.Formatter(
#     '%(asctime)s [%(filename)s] %(funcName)s:%(lineno)d: %(message)s')
# hdr.setFormatter(formatter)
#
# # 给logger添加上handler
# logger.addHandler(hdr)
#
# # 添加文件handle
# if is_file_log:
#     filename = 'ft_' + datetime.now().strftime('%Y%m%d') + '.log'
#     tempPath = os.path.join(os.getcwd(), 'log')
#     if not os.path.exists(tempPath):
#         os.makedirs(tempPath)
#     filepath = os.path.join(tempPath, filename)
#     fileHandler = logging.FileHandler(filepath)
#     fileHandler.setFormatter(formatter)
#     logger.addHandler(fileHandler)
#
#
# def make_log_msg(title, **kwargs):
#     msg = ''
#     if len(kwargs) > 0:
#         msg = ':'
#         for k, v in kwargs.items():
#             msg += ' {0}={1};'.format(k, v)
#     return title + msg


#从logger库里扣出来的
if hasattr(sys, '_getframe'):
    currentframe = lambda: sys._getframe(3)
else:  # pragma: no cover
    def currentframe():
        """Return the frame object for the caller's stack frame."""
        try:
            raise Exception
        except Exception:
            return sys.exc_info()[2].tb_frame.f_back

__LogPathName__ = "com.futunn.FutuOpenD//Log"


class FTLog(object):

    BOTH_FILE_CONSOLE = 3
    ONLY_FILE = 1
    ONLY_CONSOLE = 2

    def __init__(self, **args):
        sys_str = platform.system()
        if sys_str == "Windows":
            self.log_path = os.path.join(os.getenv("appdata"), __LogPathName__)
        else:
            self.log_path = os.path.join(os.environ['HOME'], ("." + __LogPathName__))

        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)

        self._file_level = logging.DEBUG
        self._console_level = logging.INFO

        if "file_level" in args:
            self._file_level = args["file_level"]
        if "console_level" in args:
            self._console_level = args["console_level"]

        self.file_logger = logging.getLogger('FTFileLog')
        self.file_logger.setLevel(self._file_level)
        self.file_logger.propagate = False
        self.console_logger = logging.getLogger('FTConsoleLog')
        self.console_logger.setLevel(self._console_level)
        self.console_logger.propagate = False
        
        self.formatter = logging.Formatter('%(asctime)s %(message)s')

        if not hasattr(self, 'fileHandler'):
            file_name = 'py_' + datetime.now().strftime('%Y_%m_%d') + '.log'
            file_path = os.path.join(self.log_path, file_name)
            self.fileHandler = logging.FileHandler(file_path)
            self.fileHandler.setLevel(self._file_level)
            self.fileHandler.setFormatter(self.formatter)
            self.file_logger.addHandler(self.fileHandler)

        if not hasattr(self, 'consoleHandler'):
            self.consoleHandler = logging.StreamHandler()
            self.consoleHandler.setLevel(self._console_level)
            self.consoleHandler.setFormatter(self.formatter)
            self.console_logger.addHandler(self.consoleHandler)

    def __new__(cls):
        # 关键在于这，每一次实例化的时候，我们都只会返回这同一个instance对象
        if not hasattr(cls, 'instance'):
            cls.instance = super(FTLog, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def make_log_msg(title, **kwargs):
        msg = ''
        if len(kwargs) > 0:
            msg = ':'
            for k, v in kwargs.items():
                msg += ' {0}={1};'.format(k, v)
        return title + msg

    def format_msg(self, msg):
        rv = self.findCaller()
        if (rv is not None) and (len(rv) > 0):
            filepath = rv[0]
            [_, filename] = os.path.split(filepath)
            return "[{}] {}:{}: ".format(filename, rv[2], rv[1]) + msg
        else:
            return msg

    def warning2(self, flag, msg, *args, **kwargs):
        if self._file_level <= logging.WARNING or self._console_level <= logging.WARNING:
            msg = self.format_msg(msg)
        if (self._file_level <= logging.WARNING) and ((flag & self.ONLY_FILE) != 0):
            self.file_logger.warning(msg, *args, **kwargs)
        if (self._console_level <= logging.WARNING) and ((flag & self.ONLY_CONSOLE) != 0):
            self.console_logger.warning(msg, *args, **kwargs)

    def error2(self, flag, msg, *args, **kwargs):
        if self._file_level <= logging.ERROR or self._console_level <= logging.ERROR:
            msg = self.format_msg(msg)
        if (self._file_level <= logging.ERROR) and ((flag & self.ONLY_FILE) != 0):
            self.file_logger.error(msg, *args, **kwargs)
        if (self._console_level <= logging.ERROR) and ((flag & self.ONLY_CONSOLE) != 0):
            self.console_logger.error(msg, *args, **kwargs)

    def debug2(self, flag, msg, *args, **kwargs):
        if self._file_level <= logging.DEBUG or self._console_level <= logging.DEBUG:
            msg = self.format_msg(msg)
        if (self._file_level <= logging.DEBUG) and ((flag & self.ONLY_FILE) != 0):
            self.file_logger.debug(msg, *args, **kwargs)
        if (self._console_level <= logging.DEBUG) and ((flag & self.ONLY_CONSOLE) != 0):
            self.console_logger.debug(msg, *args, **kwargs)

    def info2(self, flag, msg, *args, **kwargs):
        if self._file_level <= logging.INFO or self._console_level <= logging.INFO:
            msg = self.format_msg(msg)
        if (self._file_level <= logging.INFO) and ((flag & self.ONLY_FILE) != 0):
            self.file_logger.info(msg, *args, **kwargs)
        if (self._console_level <= logging.INFO) and ((flag & self.ONLY_CONSOLE) != 0):
            self.console_logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.warning2(self.BOTH_FILE_CONSOLE, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.error2(self.BOTH_FILE_CONSOLE, msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.debug2(self.BOTH_FILE_CONSOLE, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.info2(self.BOTH_FILE_CONSOLE, msg, *args, **kwargs)

    @property
    def file_level(self):
        return self._file_level

    @file_level.setter
    def file_level(self, value):
        self._file_level = value
        self.file_logger.setLevel(self._file_level)
        self.fileHandler.setLevel(self._file_level)

    @property
    def console_level(self):
        return self._console_level

    @console_level.setter
    def console_level(self, value):
        self._console_level = value
        self.console_logger.setLevel(self._console_level)
        self.consoleHandler.setLevel(self._console_level)

    @property
    def debug_model(self):
        """
        这个接口可以方便的让用户设置当前log的级别，一般在生产环境中，尽量关闭冗余的log以提升性能
        """
        if self._console_level <= logging.INFO and self._file_level <= logging.DEBUG:
            return True
        else:
            return False

    @console_level.setter
    def debug_model(self, on_off):
        if on_off is True:
            self._console_level = logging.INFO
            self._file_level = logging.DEBUG
        else:
            self._console_level = logging.WARNING
            self._file_level = logging.WARNING

        self.console_logger.setLevel(self._console_level)
        self.consoleHandler.setLevel(self._console_level)
        self.file_logger.setLevel(self._file_level)
        self.fileHandler.setLevel(self._file_level)


    def findCaller(self):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = currentframe()
        #On some versions of IronPython, currentframe() returns None if
        #IronPython isn't run with -X:Frames.
        if f is not None:
            f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)", None
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                continue
            rv = (co.co_filename, f.f_lineno, co.co_name)
            break
        return rv


logger = FTLog()
_srcfile = os.path.normcase(logger.error2.__code__.co_filename)


if __name__ == '__main__':
    _srcfile = ""
    logger.error2(FTLog.BOTH_FILE_CONSOLE, "1111111111")
    logger.error2(FTLog.ONLY_FILE, "222222222")
    logger.error2(FTLog.ONLY_CONSOLE, "33333333")
    logger.debug('444444444 %s' % datetime.now())
    logger.info('5555555555 %s' % datetime.now())
    logger.error('666666666 %s' % datetime.now())

