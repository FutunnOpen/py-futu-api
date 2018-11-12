#-*-coding:utf-8-*-
from futuquant import *
import pandas

class GetOptionChain(object):

    def __init__(self):
        pandas.set_option('max_columns', 100)
        pandas.set_option('display.width', 1000)

    def test1(self):
        host = '127.0.0.1'#'172.18.6.144'
        port = 11111
        quote_ctx = OpenQuoteContext(host,port)
        print(quote_ctx.get_option_chain(code = 'US.DIS', start=None,
                                         end=None, option_type=OptionType.ALL,
                                         option_cond_type=OptionCondType.OUTSIDE))
        quote_ctx.close()


if __name__ == '__main__':
    goc = GetOptionChain()
    goc.test1()