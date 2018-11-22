# -*- coding:utf-8 -*-
from futu import *
import pandas


def test_get_option_chain():
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    ret_code, ret_data = quote_ctx.get_option_chain(code='US.AAPL', start='2018-01-02', end='2018-08-30',
                                                    option_type=OptionType.CALL, option_cond_type=OptionCondType.WITHIN)
    print(ret_data)


if __name__ == '__main__':
    pandas.set_option('max_columns', 100)
    pandas.set_option('display.width', 1000)
    test_get_option_chain()



