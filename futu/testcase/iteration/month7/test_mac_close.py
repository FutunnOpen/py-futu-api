# -*- coding:utf-8 -*-
from futuquant import *
import time
import pandas


def test_mac_close():
    pandas.set_option('max_columns', 100)
    pandas.set_option('display.width', 1000)
    quote_ctx = OpenQuoteContext('172.18.7.65',11111)
    trade_ctx_hk = OpenHKTradeContext('172.18.7.65',11111)
    while True:
        print(trade_ctx_hk.unlock_trade('321321'))
        print(trade_ctx_hk.order_list_query())
        print(quote_ctx.get_market_snapshot('HK.00700'))
        time.sleep(100)
        print(quote_ctx.get_global_state())


if __name__ == '__main__':
    test_mac_close()
