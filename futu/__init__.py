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

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'VERSION.txt'), 'rb') as f:
    __version__ = f.read().decode('ascii').strip()


def set_futu_debug_model(on_off=True):
    common.set_debug_model(on_off)
