# -*- coding: utf-8 -*-

import threading
import time
from collections import namedtuple
from .utils import IS_PY2
from . import sys_config
from .ft_logger import logger

if IS_PY2:
    import Queue as queue
else:
    import queue

CallbackItem = namedtuple('CallbackItem', ['ctx', 'proto_id', 'serial_no', 'rsp_pb'])


class CallbackExecutor:
    def __init__(self):
        self._quit = False
        self._queue = queue.Queue()
        self._thread = threading.Thread(target=self.run)
        self._thread.daemon = sys_config.SysConfig.get_all_thread_daemon()
        self._thread.start()

    @property
    def queue(self):
        return self._queue

    def run(self):
        last_size_warn_time = time.time()
        while True:
            w = self._queue.get()
            if self._quit:
                break
            if w is None:
                break

            w.ctx.packet_callback(w.proto_id, serial_no=w.serial_no, rsp_pb=w.rsp_pb)

            size = self._queue.qsize()
            if size > 1000:
                now = time.time()
                if now - last_size_warn_time >= 60:
                    logger.warning(f'Callback queue size large: conn={w.ctx.conn_str()} size={size}')
                    last_size_warn_time = now

    def close(self):
        self._quit = True
        self._queue.put(None)