#-*-coding:utf-8-*-
from futu import *
import pandas
import unittest

f1 = open('test_new_protocol.txt','a')
f2 = open('test_new_protoco2.txt','a')

class GetOrderDetail(unittest.TestCase):
    # 以下为有效入参的用例
    def test_get_order_detail_hk_stock(self):
        case_name = sys._getframe().f_code.co_name
        print(case_name, file=f1, flush=True)
        print(case_name, file=f2, flush=True)
        code = 'HK.00700'
        quote_ctx1.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx1.get_order_detail(code)
        print(ret_data, file=f1, flush=True)  # 应该是空值
        quote_ctx2.subscribe(code, SubType.ORDER_DETAIL)
        ret_code, ret_data = quote_ctx2.get_order_detail(code)
        print(ret_data, file=f2, flush=True)

    def test_get_order_detail_hk_warrrant(self):
        case_name = sys._getframe().f_code.co_name
        print(case_name, file=f1, flush=True)
        print(case_name, file=f2, flush=True)
        code = 'HK.62246'
        quote_ctx1.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx1.get_order_detail(code)
        # self.assertEqual(ret_code,RET_OK)
        print(ret_code, file=f1, flush=True)
        print(ret_data, file=f1, flush=True)  # 应该是空值
        quote_ctx2.subscribe(code, SubType.ORDER_DETAIL)
        ret_code, ret_data = quote_ctx2.get_order_detail(code)
        # self.assertEqual(ret_code, RET_OK)
        print(ret_code, file=f2, flush=True)
        print(ret_data, file=f2, flush=True)

    def test_get_order_detail_hk_idx(self):
        case_name = sys._getframe().f_code.co_name
        print(case_name, file=f1, flush=True)
        print(case_name, file=f2, flush=True)
        code = 'HK.800000'
        quote_ctx1.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx1.get_order_detail(code)
        self.assertEqual(ret_code,RET_OK)
        print(ret_data, file=f1, flush=True)  # 应该是空值
        quote_ctx2.subscribe(code, SubType.ORDER_DETAIL)
        ret_code, ret_data = quote_ctx2.get_order_detail(code)
        self.assertEqual(ret_code, RET_OK)
        print(ret_data, file=f2, flush=True)

    def test_get_order_detail_hk_future(self):
        case_name = sys._getframe().f_code.co_name
        print(case_name, file=f1, flush=True)
        print(case_name, file=f2, flush=True)
        code = 'HK_FUTURE.999010'
        quote_ctx1.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx1.get_order_detail(code)
        self.assertEqual(ret_code,RET_OK)
        print(ret_data, file=f1, flush=True)  # 应该是空值
        quote_ctx2.subscribe(code, SubType.ORDER_DETAIL)
        ret_code, ret_data = quote_ctx2.get_order_detail(code)
        self.assertEqual(ret_code, RET_OK)
        print(ret_data, file=f2, flush=True)

    def test_get_order_detail_us_stock(self):
        case_name = sys._getframe().f_code.co_name
        print(case_name, file=f1, flush=True)
        print(case_name, file=f2, flush=True)
        code = 'US.AAPL'
        quote_ctx1.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx1.get_order_detail(code)
        print(ret_data, file=f1, flush=True)  # 应该是空值
        quote_ctx2.subscribe(code, SubType.ORDER_DETAIL)
        ret_code, ret_data = quote_ctx2.get_order_detail(code)
        print(ret_data, file=f2, flush=True)

    def test_get_order_detail_us_idx(self):
        case_name = sys._getframe().f_code.co_name
        print(case_name, file=f1, flush=True)
        print(case_name, file=f2, flush=True)
        code = 'US..DJI'
        quote_ctx1.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx1.get_order_detail(code)
        self.assertEqual(ret_code,RET_OK)
        print(ret_data, file=f1, flush=True)  # 应该是空值
        quote_ctx2.subscribe(code, SubType.ORDER_DETAIL)
        ret_code, ret_data = quote_ctx2.get_order_detail(code)
        self.assertEqual(ret_code, RET_OK)
        print(ret_data, file=f2, flush=True)

    def test_get_order_detail_us_etf(self):
        case_name = sys._getframe().f_code.co_name
        print(case_name, file=f1, flush=True)
        print(case_name, file=f2, flush=True)
        code = 'US.BOM'
        quote_ctx1.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx1.get_order_detail(code)
        self.assertEqual(ret_code,RET_OK)
        print(ret_data, file=f1, flush=True)  # 应该是空值
        quote_ctx2.subscribe(code, SubType.ORDER_DETAIL)
        ret_code, ret_data = quote_ctx2.get_order_detail(code)
        self.assertEqual(ret_code, RET_OK)
        print(ret_data, file=f2, flush=True)

    def test_get_order_detail_us_option(self):
        case_name = sys._getframe().f_code.co_name
        print(case_name, file=f1, flush=True)
        print(case_name, file=f2, flush=True)
        code = 'US.AAPL190111C167500'
        quote_ctx1.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx1.get_order_detail(code)
        print(ret_code, file=f1, flush=True)
        # self.assertEqual(ret_code,RET_OK)
        print(ret_data, file=f1, flush=True)  # 应该是空值
        quote_ctx2.subscribe(code, SubType.ORDER_DETAIL)
        ret_code, ret_data = quote_ctx2.get_order_detail(code)
        # self.assertEqual(ret_code, RET_OK)
        print(ret_code, file=f2, flush=True)
        print(ret_data, file=f2, flush=True)

    def test_get_order_detail_cn_idx(self):
        case_name = sys._getframe().f_code.co_name
        print(case_name, file=f1, flush=True)
        print(case_name, file=f2, flush=True)
        code = 'SZ.399241'
        quote_ctx1.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx1.get_order_detail(code)
        self.assertEqual(ret_code,RET_OK)
        print(ret_data, file=f1, flush=True)  # 应该是空值
        quote_ctx2.subscribe(code, SubType.ORDER_DETAIL)
        ret_code, ret_data = quote_ctx2.get_order_detail(code)
        self.assertEqual(ret_code, RET_OK)
        print(ret_data, file=f2, flush=True)

    def test_get_order_detail_cn_stock1(self):
        case_name = sys._getframe().f_code.co_name
        print(case_name, file=f1, flush=True)
        print(case_name, file=f2, flush=True)
        code = 'SH.000001'
        quote_ctx1.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx1.get_order_detail(code)
        self.assertEqual(ret_code,RET_OK)
        print(ret_data, file=f1, flush=True)  # 不是空值
        quote_ctx2.subscribe(code, SubType.ORDER_DETAIL)
        ret_code, ret_data = quote_ctx2.get_order_detail(code)
        self.assertEqual(ret_code, RET_OK)
        print(ret_data, file=f2, flush=True)
        # print(len((ret_data['Ask'][1])))

    def test_get_order_detail_cn_stock2(self):
        case_name = sys._getframe().f_code.co_name
        print(case_name, file=f1, flush=True)
        print(case_name, file=f2, flush=True)
        code = 'SZ.000001'
        quote_ctx1.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx1.get_order_detail(code)
        self.assertEqual(ret_code,RET_OK)
        print(ret_data, file=f1, flush=True)  # 不是空值
        quote_ctx2.subscribe(code, SubType.ORDER_DETAIL)
        ret_code, ret_data = quote_ctx2.get_order_detail(code)
        self.assertEqual(ret_code, RET_OK)
        print(ret_data, file=f2, flush=True)
        # print(len((ret_data['Ask'][1])))
        # print(len((ret_data['Bid'][1])))

    def test_get_order_detail_cn_stock3(self):
        case_name = sys._getframe().f_code.co_name
        print(case_name, file=f1, flush=True)
        print(case_name, file=f2, flush=True)
        # 委买明细和委卖都超过50
        code = 'SZ.300104'
        quote_ctx1.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx1.get_order_detail(code)
        print(ret_data, file=f1, flush=True)  # 不是空值
        quote_ctx2.subscribe(code, SubType.ORDER_DETAIL)
        ret_code, ret_data = quote_ctx2.get_order_detail(code)
        print(ret_data, file=f2, flush=True)
        # print(len((ret_data['Ask'][1])))
        # print(len((ret_data['Bid'][1])))

    def test_get_order_detail_cn_stock4(self):
        case_name = sys._getframe().f_code.co_name
        print(case_name, file=f1, flush=True)
        print(case_name, file=f2, flush=True)
        # 委买明细有，委卖是0
        code = 'SH.600159'
        quote_ctx1.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx1.get_order_detail(code)
        self.assertEqual(ret_code,RET_OK)
        print(ret_data, file=f1, flush=True)  # 不是空值
        quote_ctx2.subscribe(code, SubType.ORDER_DETAIL)
        ret_code, ret_data = quote_ctx2.get_order_detail(code)
        self.assertEqual(ret_code, RET_OK)
        print(ret_data, file=f2, flush=True)
        # print(len((ret_data['Ask'][1])))
        # print(len((ret_data['Bid'][1])))

    def test_get_order_detail_cn_stock5(self):
        # 委买明细和委卖都小于50
        case_name = sys._getframe().f_code.co_name
        print(case_name, file=f1, flush=True)
        print(case_name, file=f2, flush=True)
        code = 'SH.600403'
        quote_ctx1.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx1.get_order_detail(code)
        print(ret_code, file=f1, flush=True)
        quote_ctx2.subscribe(code, SubType.ORDER_DETAIL)
        ret_code, ret_data = quote_ctx2.get_order_detail(code)
        print(ret_code, file=f2, flush=True)
        # print(ret_data['code'])  # 不是空值
        #         # print(ret_data['Ask'])
        #         # print(ret_data['Bid'])
        #         # print(len((ret_data['Ask'][1])))
        #         # print(len((ret_data['Bid'][1])))

    # 以下为无效入参的用例
    def test_get_order_detail_wrong_market(self):
        case_name = sys._getframe().f_code.co_name
        print(case_name, file=f1, flush=True)
        print(case_name, file=f2, flush=True)
        code = 'hk.00700'
        quote_ctx1.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx1.get_order_detail(code)
        self.assertEqual(ret_code,RET_ERROR)
        print(ret_data, file=f1, flush=True)  # 打印错误提示信息
        quote_ctx2.subscribe(code, SubType.ORDER_DETAIL)
        ret_code, ret_data = quote_ctx2.get_order_detail(code)
        self.assertEqual(ret_code, RET_ERROR)
        print(ret_data, file=f2, flush=True)

    def test_get_order_detail_wrong_code1(self):
        case_name = sys._getframe().f_code.co_name
        print(case_name, file=f1, flush=True)
        print(case_name, file=f2, flush=True)
        code = 'HK.007021'
        quote_ctx1.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx1.get_order_detail(code)
        self.assertEqual(ret_code,RET_ERROR)
        print(ret_data, file=f1, flush=True)  # 打印错误提示信息
        quote_ctx2.subscribe(code, SubType.ORDER_DETAIL)
        ret_code, ret_data = quote_ctx2.get_order_detail(code)
        self.assertEqual(ret_code, RET_ERROR)
        print(ret_data, file=f2, flush=True)


    def test_get_order_detail_wrong_code2(self):
        case_name = sys._getframe().f_code.co_name
        print(case_name, file=f1, flush=True)
        print(case_name, file=f2, flush=True)
        code = 'SZ.3001040'
        quote_ctx1.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx1.get_order_detail(code)
        self.assertEqual(ret_code,RET_ERROR)
        print(ret_data, file=f1, flush=True)  # 打印错误提示信息
        quote_ctx2.subscribe(code, SubType.ORDER_DETAIL)
        ret_code, ret_data = quote_ctx2.get_order_detail(code)
        self.assertEqual(ret_code, RET_ERROR)
        print(ret_data, file=f2, flush=True)

    def test_get_order_detail_wrong_code3(self):
        case_name = sys._getframe().f_code.co_name
        print(case_name, file=f1, flush=True)
        print(case_name, file=f2, flush=True)
        code = ''
        quote_ctx1.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx1.get_order_detail(code)
        self.assertEqual(ret_code,RET_ERROR)
        print(ret_data, file=f1, flush=True)  # 打印错误提示信息
        quote_ctx2.subscribe(code, SubType.ORDER_DETAIL)
        ret_code, ret_data = quote_ctx2.get_order_detail(code)
        self.assertEqual(ret_code, RET_ERROR)
        print(ret_data, file=f2, flush=True)

    def test_get_order_detail_stopped_code(self):
        case_name = sys._getframe().f_code.co_name
        print(case_name, file=f1, flush=True)
        print(case_name, file=f2, flush=True)
        code = 'US.UWTIF'
        quote_ctx1.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx1.get_order_detail(code)
        print(ret_data, file=f1, flush=True)  # 打印错误提示信息
        quote_ctx2.subscribe(code, SubType.ORDER_DETAIL)
        ret_code, ret_data = quote_ctx2.get_order_detail(code)
        print(ret_data, file=f2, flush=True)

    def test_get_order_detail_wrong_type(self):
        case_name = sys._getframe().f_code.co_name
        print(case_name, file=f1, flush=True)
        print(case_name, file=f2, flush=True)
        code = ['SZ.300104','SZ.002356']
        quote_ctx1.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx1.get_order_detail(code)
        self.assertEqual(ret_code,RET_ERROR)
        print(ret_data, file=f1, flush=True)  # 打印错误提示信息
        quote_ctx1.subscribe(code, SubType.ORDER_DETAIL)
        ret_code, ret_data = quote_ctx2.get_order_detail(code)
        self.assertEqual(ret_code, RET_ERROR)
        print(ret_data, file=f2, flush=True)

    def test_get_order_detail_not_subscribe(self):
        case_name = sys._getframe().f_code.co_name
        print(case_name, file=f1, flush=True)
        print(case_name, file=f2, flush=True)
        code = 'SZ.300104'
        ret_code, ret_data = quote_ctx1.get_order_detail(code)
        print(ret_data, file=f1, flush=True)
        ret_code, ret_data = quote_ctx2.get_order_detail(code)
        print(ret_data, file=f2, flush=True)


class OrderDetailTest(OrderDetailHandlerBase):
    def on_recv_rsp(self, rsp_str):
        ret_code, data = super(OrderDetailTest, self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("OrderDetailTest: error, msg: %s" % data)
            return RET_ERROR, data

        print("OrderDetailTest ", data)  # OrderDetailTest自己的处理逻辑
        print(len((data['Ask'][1])))
        print(len((data['Bid'][1])))
        return RET_OK, data


if __name__ == '__main__':
    # SysConfig.set_all_thread_daemon(True)
    quote_ctx1 = OpenQuoteContext(host='127.0.0.1', port=11111)
    quote_ctx2 = OpenQuoteContext(host='127.0.0.1', port=11112)
    # trade_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
    # trade_ctx_us = OpenUSTradeContext(host='127.0.0.1', port=11111)
    # trade_ctx_cn = OpenCNTradeContext(host='127.0.0.1', port=11111)
    # pandas.set_option('max_columns', 100)
    # pandas.set_option('display.width', 1000)
    # print(trade_ctx.unlock_trade('321321'))
    # print(trade_ctx.place_order(100, 1, 'HK.002000', trd_side=TrdSide.BUY))
    # print(trade_ctx_us.place_order(100, 1, 'US.2321', trd_side=TrdSide.BUY))
    # print(trade_ctx_cn.place_order(100, 1, 'SZ.00121212', trd_side=TrdSide.BUY))
    # 低频接口测试
    unittest.main()
    # god = GetOrderDetail()
    # god.test_get_order_detail_wrong_code1()
    # code_list = ['US.AAPL']
    # print(quote_ctx.subscribe(code_list, SubType.QUOTE))
    # print(quote_ctx.get_stock_quote(code_list))
    # 高频接口测试
    # handler = OrderDetailTest()
    # quote_ctx.set_handler(handler)
    # print(quote_ctx.subscribe(['HK.00100', 'HK.18141','SZ.3001040'], [SubType.ORDER_DETAIL]))
    # print(quote_ctx.subscribe(['HK.0010'], [SubType.ORDER_DETAIL]))
    # print(quote_ctx.subscribe(['SZ.3001040'], [SubType.ORDER_DETAIL]))
    # print(quote_ctx.query_subscription())
    # print(quote_ctx.subscribe(['HK.00700','US.AAPL','HK.14871','SH.600030'], [SubType.ORDER_DETAIL]))
    # time.sleep(15)
    # quote_ctx.close()
