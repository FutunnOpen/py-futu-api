# -*- coding: utf-8 -*-
from futu import *

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
print(quote_ctx.get_trading_days(Market.HK, start='2018-01-01', end='2018-01-05'))
print(quote_ctx.get_warrant())
quote_ctx.close()


