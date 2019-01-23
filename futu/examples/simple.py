# -*- coding: utf-8 -*-
from futu import *


quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
print(quote_ctx.get_trading_days(Market.HK, start='2018-02-01', end='2018-02-05'))


from futu.quote.quote_get_warrant import Request

req = Request()
req.sort_field = SortField.CODE
req.ascend = True
req.type_list = [WrtType.BEAR, WrtType.BUY]
req .issuer_list = [Issuer.CS, Issuer.CT, Issuer.EA]

print(quote_ctx.get_warrant("HK.00700", req))
quote_ctx.close()


