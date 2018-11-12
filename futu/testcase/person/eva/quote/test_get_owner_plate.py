#-*-coding=utf-8-*-

import pandas
from futuquant import *
from futuquant.testcase.person.eva.datas.collect_stock import *

class GetOwnerPlate(object):
    #获取股票行业分类

    def __init__(self):
        pandas.set_option('display.width', 1000)
        pandas.set_option('max_columns', 1000)

    def test1(self):
        host='127.0.0.1'
        port=11111
        quote_ctx = OpenQuoteContext(host,port)
        print(quote_ctx.get_owner_plate('HK.28100'))


if __name__ == '__main__':
    gop = GetOwnerPlate()
    gop.test1()

