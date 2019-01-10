import sys
import os
import os.path
import platform
import futu
import multiprocessing as mp

if futu.IS_PY2:
    import Queue as queue
else:
    import queue


def print_sys_info(opend_ip=None, opend_port=None):
    if futu.IS_PY2:
        mp.freeze_support()
    opend_version = get_opend_version(opend_ip, opend_port)
    futu_path = os.path.abspath(os.path.realpath(futu.__file__))
    log_dir = _get_log_dir()

    print('Futu path: ',  futu_path)
    print('Futu version: ', futu.__version__)
    print('OpenD version:', opend_version)
    print('Python path: ', sys.executable)
    print('Python version: ', platform.python_version())
    print('OS: ', sys.platform)
    print('Platform: ', platform.platform())
    print('Arch: ', platform.architecture())
    print('Module search path: ', sys.path)
    print('Log dir: ', log_dir)


def get_opend_version(opend_ip, opend_port):
    q = mp.Queue()
    proc = mp.Process(target=_opend_proc, args=(q, opend_ip, opend_port))
    try:
        proc.start()
        opend_version = q.get(timeout=5)
        return opend_version
    except queue.Empty:
        proc.terminate()
        return 'Unknown'


def _opend_proc(q, ip=None, port=None):
    arg = {}
    if ip is not None:
        arg['host'] = ip
    if port is not None:
        arg['port'] = port

    quote_ctx = futu.OpenQuoteContext(**arg)
    ret, data = quote_ctx.get_global_state()
    if ret == futu.RET_OK:
        q.put(data['server_ver'])
    quote_ctx.close()


def _get_log_dir():
    if sys.platform.startswith('win'):
        return os.path.join(os.getenv("appdata"), 'com.futunn.FutuOpenD/Log')
    else:
        return os.path.join(os.environ['HOME'], '.com.futunn.FutuOpenD/Log')
