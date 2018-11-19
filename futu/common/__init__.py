# -*- coding: utf-8 -*-

import sys
import io
import time
import json
from .ft_logger import *

IS_PY2 = sys.version_info[0] == 2
debug_model = True

def bytes_utf8(data):
    if IS_PY2:
        return bytes(data)
    else:
        return bytes(data, encoding='utf-8')


def str_utf8(data):
    if IS_PY2:
        return str(data)
    else:
        return str(data, encoding='utf-8')

def set_debug_model(value):
    global debug_model
    debug_model = (value is True)
    logger.debug_model = (value is True)


class RspHandlerBase(object):
    """callback function base class"""

    def __init__(self):
        self._file = None

    def __del__(self):
        self.close_file()

    def close_file(self):
        if self._file is not None:
            self._file.close()
            self._file = None

    def open_file(self, file_name):
        self.close_file()
        file_path = os.path.join(logger.log_path, file_name)
        self._file = open(file_path, 'w')

    def on_recv_log(self, content):
        if not debug_model:
            return
        if self._file is None:
            time_str = time.strftime('%Y_%m_%d', time.localtime(time.time()))
            millis = int(round(time.time() * 1000))
            type_name = self.__class__.__name__
            log_name = os.path.join("{}_{}_{}.log".format(time_str, millis, type_name))
            self.open_file(log_name)
        if self._file:
            try:
                self._file.write(json.dumps(content, indent=4).replace('\n', '').replace('\t', '').replace(' ', '') + "\n")
                self._file.flush()
            except TypeError:
                type_name = self.__class__.__name__
                self._file.write("{} can not dump json\n".format(type_name))
                self._file.flush()
            except IOError:
                self.close_file()
            except Exception as e:
                logger.error(str(e).replace('\n', '').replace('\t', ''))

    def on_recv_rsp(self, rsp_pb):
        """receive response callback function"""
        return 0, None


