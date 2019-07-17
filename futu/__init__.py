# -*- coding: utf-8 -*-
#
# Copyright 2017 Futu, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os.path
import signal
import sys
import threading

def _check_module(mod_name, package_name=None, version=None, version_getter=None, py_version=None):
    import importlib

    if package_name is None:
        package_name = mod_name

    if py_version is not None:
        if sys.version_info[0] != py_version:
            return

    try:
        mod = importlib.import_module(mod_name)
    except Exception:
        if version is None:
            print("Missing required package {}".format(package_name))
        else:
            print("Missing required package {} v{}".format(package_name, version))
        sys.exit(1)

    if version is not None:
        mod_version = version_getter(mod)
        if version != mod_version:
            print("Package {} version is {}, better be {}.".format(package_name, mod_version, version))


def _pip_get_package_version(package_name):
    import subprocess
    proc = subprocess.Popen([sys.executable, '-m', 'pip', 'show', package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outdata, errdata = proc.communicate()

    if isinstance(outdata, bytes):
        eol = b'\n'
        version_key = b'Version:'
    else:
        eol = '\n'
        version_key = 'Version:'

    lines = outdata.split(eol)
    for line in lines:
        line = line.strip()
        if line.startswith(version_key):
            version = line.lstrip(version_key).strip()
            if isinstance(version, bytes):
                return version.decode('utf-8')
    return None


def _check_package(package_name, version=None):
    try:
        import pip
    except ImportError:
        return

    mod_version = _pip_get_package_version(package_name)
    if mod_version == '':
        if version is None:
            print("Missing required package {}".format(package_name))
        else:
            print("Missing required package {} v{}".format(package_name, version))
        sys.exit(1)
    elif version is not None and mod_version != version:
        print("Package {} version is {}, better be {}.".format(package_name, mod_version, version))


_check_module('pandas')
_check_module('simplejson')
_check_module('Crypto', 'pycryptodome')
_check_module('google.protobuf', package_name='protobuf', version='3.5.1', version_getter=lambda mod: mod.__version__)
_check_module('selectors2', py_version=2)
_check_package('pycryptodome')


#import data querying APIs and response handle base class
from futu.quote.open_quote_context import OpenQuoteContext
from futu.quote.quote_response_handler import *
from futu.trade.trade_response_handler import *

#import HK and US trade context
from futu.trade.open_trade_context import OpenHKTradeContext
from futu.trade.open_trade_context import OpenUSTradeContext
from futu.trade.open_trade_context import OpenHKCCTradeContext
from futu.trade.open_trade_context import OpenCNTradeContext

#import constant values
from futu.common import *
from futu.common.constant import *
from futu.common.sys_config import SysConfig
from futu.common.diag import print_sys_info
from futu.common.err import Err

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'VERSION.txt'), 'rb') as f:
    __version__ = f.read().decode('ascii').strip()

def set_futu_debug_model(on_off=True):
    common.set_debug_model(on_off)


def quit_handler(sig, frame):
    os._exit(0)


if not IS_PY2:
    if threading.current_thread() is threading.main_thread():
        signal.signal(signal.SIGINT, quit_handler)
