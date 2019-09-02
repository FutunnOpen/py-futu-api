# -*- coding: utf-8 -*-
from futu import *


quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

req = Request()
req.sort_field = SortField.CODE
req.ascend = True
req.type_list = [WrtType.BEAR, WrtType.CALL]
req .issuer_list = [Issuer.CS, Issuer.CT, Issuer.EA]
print(quote_ctx.get_warrant("HK.00700", req))

quote_ctx.close()


