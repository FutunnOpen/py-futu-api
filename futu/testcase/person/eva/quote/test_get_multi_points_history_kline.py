#-*-coding:utf-8-*-

import futuquant
from futuquant.common.constant import *
import pandas

class GetMultiPointsHistoryKline(object):

    def __init__(self):
        pandas.set_option('display.width', 1000)
        pandas.set_option('max_columns', 1000)

    def test1(self):
        quote_ctx = futuquant.OpenQuoteContext(host='127.0.0.1',port=11111)
        #入参
        fields = KL_FIELD.ALL_REAL#[KL_FIELD.DATE_TIME, KL_FIELD.OPEN, KL_FIELD.HIGH, KL_FIELD.LOW, KL_FIELD.CLOSE, KL_FIELD.LAST_CLOSE]
        ktype = KLType.K_MON
        autype = AuType.QFQ
        no_data_mode = KLNoDataMode.FORWARD
        #日期<=5个
        dates = '2017-5-4 9:30:00' #['2017-5-4 9:30:00','2017-5-4 9:35:00','2017-5-4 9:40:00','2017-5-5']   #'2017-1-1', '2018-1-1', '2018-4-1', '2018-2-1',
        #股票代码
        codes = ['HK.00700','US.AAPL']
        ret_code_multi_points,ret_data_multi_points = quote_ctx.get_multi_points_history_kline( codes, dates, fields, ktype, autype, no_data_mode)
        quote_ctx.close()
        # ret_code, ret_data = quote_ctx.get_stock_basicinfo(market='HK', stock_type='STOCK')
        # codes = ret_data['code'].tolist()[:2]

        print(ret_code_multi_points)
        print(ret_data_multi_points)
        # for data in ret_data_multi_points.iterrows():
        #     print(data)


if __name__ == '__main__':
    gmphk = GetMultiPointsHistoryKline()
    gmphk.test1()