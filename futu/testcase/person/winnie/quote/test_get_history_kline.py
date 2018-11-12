# -*-coding:utf-8-*-

from futuquant import *
from futuquant.common.constant import *
import pandas


class CurKlineTest(CurKlineHandlerBase):
    def on_recv_rsp(self, rsp_str):
        ret_code, data = super(CurKlineTest,self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print(data)  # "CurKlineTest: error, msg: %s" %
            return RET_ERROR, data

        print(data) # CurKlineTest自己的处理逻辑

        return RET_OK, data


class GetHistoryKline(object):
    def test1(self):
        # 设置打印信息
        pandas.set_option('max_columns', 100)
        pandas.set_option('display.width', 1000)
        quote_ctx = OpenQuoteContext(host='172.18.10.58', port=11111)
        code = 'HK.00700'
        end = '2018-08-01'
        start = '2018-06-20'
        ktype = KLType.K_WEEK
        autype = AuType.HFQ
        # autype = AuType.NONE
        fields = KL_FIELD.ALL_REAL

        ret_code, ret_data = quote_ctx.get_history_kline(code, start, end, ktype, autype, fields)

        print(ret_code)
        print(ret_data)
        quote_ctx.close()


def test_handler():  # 异步推送数据
    pandas.set_option('max_columns', 100)
    pandas.set_option('display.width', 1000)
    # SysConfig.set_all_thread_daemon(True)
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    handler = CurKlineTest()
    quote_ctx.set_handler(handler)
    quote_ctx.subscribe(['HK.00700'], SubType.K_1M)

    # print(quote_ctx.get_cur_kline('HK.00700', 8, SubType.K_1M, AuType.QFQ))
    # time.sleep(15)
    # quote_ctx.close()


if __name__ == '__main__':
    # ghk = GetHistoryKline()
    # for i in range(10):
    # ghk.test1()
    test_handler()
