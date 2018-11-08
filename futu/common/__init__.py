# -*- coding: utf-8 -*-

import sys
IS_PY2 = sys.version_info[0] == 2


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


class RspHandlerBase(object):
    """callback function base class"""

    def __init__(self):
        pass

    def on_recv_rsp(self, rsp_pb):
        """receive response callback function"""
        return 0, None


