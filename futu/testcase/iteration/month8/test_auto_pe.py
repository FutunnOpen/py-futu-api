# 8月迭代2--正股增加动态PE

# -*- coding:utf-8 -*-
from futu import *
import pandas


def test_get_market_snapshot():
    pandas.set_option('max_columns', 100)
    pandas.set_option('display.width', 1000)
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    code_list = ['HK.00700', 'HK.00066', 'US.AAPL', 'SZ.000700']  # 港股正股、美股正股、A股
    # code_list = ['HK.999010', 'HK.22170']  # 期权、涡轮
    print(quote_ctx.get_market_snapshot(code_list))


if __name__ == '__main__':
    test_get_market_snapshot()
