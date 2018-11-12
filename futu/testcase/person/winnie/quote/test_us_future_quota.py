# -*- coding:utf-8 -*-
from futuquant import *
import pandas


def test_subscribe():
    code = ['US_OPTION.AAPL180921P260000']
    host = '127.0.0.1'
    port = 11111
    quote_ctx = OpenQuoteContext(host, port)
    print(quote_ctx.subscribe(code, SubType.TICKER))
    print(quote_ctx.query_subscription())


if __name__ == '__main__':
    test_subscribe()
