# -*- coding: utf-8 -*-
from futu import *
from futu.quote.quote_stockfilter_info import SimpleFilter

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

field = SimpleFilter()
field.filter_min = 100
field.filter_max = 1000
field.stock_field = StockField.CUR_PRICE
field.is_no_filter = False
field.sort = SortDir.ASCEND

# field2 = SimpleFilter()
# field2.filter_min = 100
# field2.filter_max = 1000
# field2.stock_field = StockField.VOLUME_RATIO
# field2.sort = SortDir.ASCEND
# field2.is_no_filter = False
#
# field3 = SimpleFilter()
# field3.stock_field = StockField.CUR_PRICE_TO_HIGHEST52_WEEKS_RATIO
# field3.is_no_filter = True

code, ret = quote_ctx.get_stock_filter(Market.HK, [field])
if code == RET_OK:
    last_page, all_count, ret_list = ret
    print(ret_list)
else:
    print(ret)

quote_ctx.close()


