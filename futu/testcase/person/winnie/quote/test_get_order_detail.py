#-*-coding:utf-8-*-
from futu import *
import pandas
import unittest


class GetOrderDetail(unittest.TestCase):
    # 以下为有效入参的用例
    def test_get_order_detail_hk_stock(self):
        code = 'HK.00700'
        quote_ctx.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx.get_order_detail(code)
        print(ret_code)
        print(ret_data)  # 应该是空值

    def test_get_order_detail_hk_warrrant(self):
        code = 'HK.62246'
        quote_ctx.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_OK)
        print(ret_data)  # 应该是空值

    def test_get_order_detail_hk_idx(self):
        code = 'HK.800000'
        quote_ctx.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_OK)
        print(ret_data)  # 应该是空值

    def test_get_order_detail_hk_future(self):
        code = 'HK_FUTURE.999010'
        quote_ctx.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_OK)
        print(ret_data)  # 应该是空值

    def test_get_order_detail_us_stock(self):
        code = 'US.AAPL'
        quote_ctx.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx.get_order_detail(code)
        print(RET_OK)
        print(ret_data)  # 应该是空值

    def test_get_order_detail_us_idx(self):
        code = 'US..DJI'
        quote_ctx.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_OK)
        print(ret_data)  # 应该是空值

    def test_get_order_detail_us_etf(self):
        code = 'US.BOM'
        quote_ctx.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_OK)
        print(ret_data)  # 应该是空值

    def test_get_order_detail_us_option(self):
        code = 'US.AAPL181109C240000'
        quote_ctx.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_OK)
        print(ret_data)  # 应该是空值

    def test_get_order_detail_cn_idx(self):
        code = 'SZ.399241'
        quote_ctx.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx.get_order_detail(code)
        # self.assertEqual(ret_code,RET_OK)
        print(ret_code)
        print(ret_data)  # 应该是空值

    def test_get_order_detail_cn_stock1(self):
        code = 'SH.000001'
        quote_ctx.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx.get_order_detail(code)
        # self.assertEqual(ret_code,RET_OK)
        print(ret_code)
        print(ret_data)  # 不是空值
        print(len((ret_data['Ask'][1])))

    def test_get_order_detail_cn_stock2(self):
        code = 'SZ.000001'
        quote_ctx.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_OK)
        print(ret_data)  # 不是空值
        print(len((ret_data['Ask'][1])))
        print(len((ret_data['Bid'][1])))

    def test_get_order_detail_cn_stock3(self):
        # 委买明细和委卖都超过50
        code = 'SZ.300104'
        quote_ctx.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx.get_order_detail(code)
        print(ret_code)
        print(ret_data)  # 不是空值
        print(len((ret_data['Ask'][1])))
        print(len((ret_data['Bid'][1])))

    def test_get_order_detail_cn_stock4(self):
        # 委买明细有，委卖是0
        code = 'SH.600159'
        quote_ctx.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_OK)
        print(ret_data)  # 不是空值
        print(len((ret_data['Ask'][1])))
        print(len((ret_data['Bid'][1])))

    def test_get_order_detail_cn_stock5(self):
        # 委买明细和委卖都小于50
        code = 'SH.600403'
        quote_ctx.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx.get_order_detail(code)
        print(ret_code)
        print(ret_data['code'])  # 不是空值
        print(ret_data['Ask'])
        print(ret_data['Bid'])
        print(len((ret_data['Ask'][1])))
        print(len((ret_data['Bid'][1])))

    # 以下为无效入参的用例
    def test_get_order_detail_wrong_market(self):
        code = 'hk.00700'
        quote_ctx.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_ERROR)
        print(ret_data)  # 打印错误提示信息

    def test_get_order_detail_wrong_code1(self):
        code = 'HK.007021'
        quote_ctx.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_ERROR)
        print(ret_code, ret_data)  # 打印错误提示信息


    def test_get_order_detail_wrong_code2(self):
        code = 'SZ.3001040'
        quote_ctx.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_ERROR)
        print(ret_data)  # 打印错误提示信息

    def test_get_order_detail_wrong_code3(self):
        code = ''
        quote_ctx.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_ERROR)
        print(ret_data)  # 打印错误提示信息

    def test_get_order_detail_stopped_code(self):
        code = 'US.UWTIF'
        quote_ctx.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx.get_order_detail(code)
        # self.assertEqual(ret_code,RET_ERROR)
        print(ret_code)
        print(ret_data)  # 打印错误提示信息

    def test_get_order_detail_wrong_type(self):
        code = ['SZ.300104','SZ.002356']
        quote_ctx.subscribe(code, SubType.ORDER_DETAIL)
        ret_code,ret_data = quote_ctx.get_order_detail(code)
        self.assertEqual(ret_code,RET_ERROR)
        print(ret_data)  # 打印错误提示信息

    def test_get_order_detail_not_subscribe(self):
        code = 'SZ.300104'
        ret_code, ret_data = quote_ctx.get_order_detail(code)
        print(ret_code)
        print(ret_data)


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
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
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
    # unittest.main()
    # god = GetOrderDetail()
    # god.test_get_order_detail_wrong_code1()
    # code_list = ['US.AAPL']
    # print(quote_ctx.subscribe(code_list, SubType.QUOTE))
    # print(quote_ctx.get_stock_quote(code_list))
    # 高频接口测试
    handler = OrderDetailTest()
    quote_ctx.set_handler(handler)
    print(quote_ctx.subscribe(['HK.00100', 'HK.18141','SZ.3001040'], [SubType.ORDER_DETAIL]))
    print(quote_ctx.subscribe(['HK.0010'], [SubType.ORDER_DETAIL]))
    print(quote_ctx.subscribe(['SZ.3001040'], [SubType.ORDER_DETAIL]))
    print(quote_ctx.query_subscription())
    # print(quote_ctx.subscribe(['HK.00700','US.AAPL','HK.14871','SH.600030'], [SubType.ORDER_DETAIL]))
    # time.sleep(15)
    # quote_ctx.close()
