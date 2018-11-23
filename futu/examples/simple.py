# -*- coding: utf-8 -*-
from futu import *

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
ret, data, page_req_key = quote_ctx.request_history_kline('HK.00700', start='2018-01-20', end='2018-06-22', ktype=KLType.K_QUARTER) #请求开头50个数据
print(ret, data)
# ret, data, page_req_key = quote_ctx.request_history_kline('HK.00700', start='2018-06-20', end='2018-06-22', max_count=50, page_req_key=page_req_key) #请求下50个数据
# print(ret, data)
quote_ctx.close()


