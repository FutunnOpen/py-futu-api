#-*-coding:utf-8-*-

from futu import *
import pandas

class GetMulHtryKl(object):

    def test1(self):
        pandas.set_option('display.width',1000)
        pandas.set_option('max_columns',1000)

        quote_ctx = OpenQuoteContext(host='127.0.0.1',port=11111)
        codelist = ['SH.601789']
        start = '2017-01-22'    #'2018-07-01'
        end = '2017-06-22'
        ktype = KLType.K_DAY
        autype = AuType.QFQ
        ret_code, ret_data = quote_ctx.get_multiple_history_kline(codelist = codelist,start = start,end = end,ktype = ktype,autype = autype)
        print(ret_code)
        print(ret_data)
        quote_ctx.close()



if __name__ == '__main__':
    GetMulHtryKl().test1()