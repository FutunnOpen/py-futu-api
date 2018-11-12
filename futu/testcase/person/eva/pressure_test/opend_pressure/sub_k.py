#-*-coding:utf-8-*-

from futuquant import *

class Sub(object):

    def sub_k(self):

        quote_ctx = OpenQuoteContext(host= '127.0.0.1', port=11111)
        quote_ctx.start()
        quote_ctx.set_handler(CurKlineTest())

        #挂机测稳定性：K线种类数（8）*股票个数 > 100
        kTypes = [SubType.K_1M,SubType.K_5M,SubType.K_15M, SubType.K_30M, SubType.K_60M, SubType.K_DAY, SubType.K_WEEK, SubType.K_MON]
        ret_code_basic ,ret_data_basic = quote_ctx.get_stock_basicinfo(Market.HK, SecurityType.STOCK)
        code_list = ret_data_basic['code'].tolist()

        for code in code_list:
            for kType in kTypes:
                quote_ctx.subscribe(code, kType)



class CurKlineTest(CurKlineHandlerBase):
    '''获取实时K线 get_cur_kline 和 CurKlineHandlerBase'''

    def on_recv_rsp(self, rsp_pb):
        ret_code, ret_data = super(CurKlineTest, self).on_recv_rsp(rsp_pb)
        print(ret_data)

        return RET_OK, ret_data

if __name__ == '__main__':
    Sub().sub_k()