# -*- coding: utf-8 -*-

import sys
import io
import time
import json
from .ft_logger import *

IS_PY2 = sys.version_info[0] == 2
debug_model = False

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

def set_debug_model(on_off):
    global debug_model
    debug_model = (on_off is True)
    logger.debug_model = (on_off is True)


class RspHandlerBase(object):
    """callback function base class"""

    def __init__(self):
        self._file = None
        self._current_day = 0

    def __del__(self):
        self._close_file()

    def _close_file(self):
        if self._file is not None:
            self._file.close()
            self._file = None

    def _open_file(self):
        self._close_file()

        time_str = time.strftime('%Y_%m_%d', time.localtime(time.time()))
        millis = int(round(time.time() * 1000))
        type_name = self.__class__.__name__
        log_file_name = os.path.join("Track_{}_{}_{}.log".format(time_str, millis, type_name))
        file_path = os.path.join(logger.log_path, log_file_name)
        self._file = open(file_path, 'w')
        self._current_day = time.localtime().tm_mday

    def on_recv_log(self, content):
    #用于记录推送信息，性能不高，如果需要提升性能的时候，记得把set_futu_debug_model关掉
        if not debug_model:
            return
        current_day = time.localtime().tm_mday

        if (self._file is None) or (current_day != self._current_day):
            self._open_file()

        if self._file:
            try:
                log_contents = dict()
                log_contents["content"] = content
                log_contents["time"] = time.strftime('%H:%M:%S', time.localtime(time.time()))
                log_contents["millis"] = int(round(time.time() * 1000))
                self._file.write(json.dumps(log_contents, indent=4).replace('\n', '').replace('\t', '').replace(' ', '') + "\n")
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


