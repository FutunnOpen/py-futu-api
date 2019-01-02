# -*- coding: utf-8 -*-

import threading
from collections import namedtuple
from futu.common.utils import IS_PY2

if IS_PY2:
    import Queue as queue
else:
    import queue

CallbackItem = namedtuple('CallbackItem', ['ctx', 'proto_id', 'rsp_pb'])


class CallbackExecutor:
    def __init__(self):
        self._queue = queue.Queue()
        self._thread = threading.Thread(target=self.run)
        self._thread.daemon = True
        self._thread.start()

    @property
    def queue(self):
        return self._queue

    def run(self):
        while True:
            w = self._queue.get()
            if w is None:
                break

            ctx, proto_id, rsp_pb = w
            ctx.packet_callback(proto_id, rsp_pb)

    def close(self):
        self._queue.put(None)