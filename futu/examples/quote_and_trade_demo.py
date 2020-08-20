# -*- coding: utf-8 -*-
"""
Examples for use the python functions: get push data
"""
from time import sleep
from futu import *



class StockQuoteTest(StockQuoteHandlerBase):
    """
    获得报价推送数据
    """
    def on_recv_rsp(self, rsp_pb):
        """数据响应回调函数"""
        ret_code, content = super(StockQuoteTest, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            logger.debug("StockQuoteTest: error, msg: %s" % content)
            return RET_ERROR, content
        print("* StockQuoteTest : %s" % content)
        return RET_OK, content


class CurKlineTest(CurKlineHandlerBase):
    """ kline push"""
    def on_recv_rsp(self, rsp_pb):
        """数据响应回调函数"""
        ret_code, content = super(CurKlineTest, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            print("* CurKlineTest: error, msg: %s" % content)
        return RET_OK, content


class RTDataTest(RTDataHandlerBase):
    """ 获取分时推送数据 """
    def on_recv_rsp(self, rsp_pb):
        """数据响应回调函数"""
        ret_code, content = super(RTDataTest, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            print("* RTDataTest: error, msg: %s" % content)
            return RET_ERROR, content
        print("* RTDataTest :%s \n" % content)
        return RET_OK, content


class TickerTest(TickerHandlerBase):
    """ 获取逐笔推送数据 """
    def on_recv_rsp(self, rsp_pb):
        """数据响应回调函数"""
        ret_code, content = super(TickerTest, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            print("* TickerTest: error, msg: %s" % content)
            return RET_ERROR, content
        print("* TickerTest\n", content)
        return RET_OK, content


class OrderBookTest(OrderBookHandlerBase):
    """ 获得摆盘推送数据 """
    def on_recv_rsp(self, rsp_pb):
        """数据响应回调函数"""
        ret_code, content = super(OrderBookTest, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            print("* OrderBookTest: error, msg: %s" % content)
            return RET_ERROR, content
        print("* OrderBookTest\n", content)
        return RET_OK, content


class BrokerTest(BrokerHandlerBase):
    """ 获取经纪队列推送数据 """
    def on_recv_rsp(self, rsp_pb):
        """数据响应回调函数"""
        ret_code, stock_code, contents = super(BrokerTest, self).on_recv_rsp(rsp_pb)
        if ret_code == RET_OK:
            bid_content = contents[0]
            ask_content = contents[1]
            print("* BrokerTest code \n", stock_code)
            print("* BrokerTest bid \n", bid_content)
            print("* BrokerTest ask \n", ask_content)
        return ret_code


class SysNotifyTest(SysNotifyHandlerBase):
    """sys notify"""
    def on_recv_rsp(self, rsp_pb):
        """receive response callback function"""
        ret_code, content = super(SysNotifyTest, self).on_recv_rsp(rsp_pb)

        if ret_code == RET_OK:
            main_type, sub_type, msg = content
            print("* SysNotify main_type='{}' sub_type='{}' msg='{}'\n".format(main_type, sub_type, msg))
        else:
            print("* SysNotify error:{}\n".format(content))
        return ret_code, content


class TradeOrderTest(TradeOrderHandlerBase):
    """ order update push"""
    def on_recv_rsp(self, rsp_pb):
        ret, content = super(TradeOrderTest, self).on_recv_rsp(rsp_pb)

        if ret == RET_OK:
            print("* TradeOrderTest content={}\n".format(content))

        return ret, content


class TradeDealTest(TradeDealHandlerBase):
    """ order update push"""
    def on_recv_rsp(self, rsp_pb):
        ret, content = super(TradeDealTest, self).on_recv_rsp(rsp_pb)

        if ret == RET_OK:
            print("TradeDealTest content={}".format(content))

        return ret, content


def quote_test():
    '''
    行情接口调用测试
    :return:
    '''
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

    # 设置异步回调接口
    quote_ctx.set_handler(StockQuoteTest())
    quote_ctx.set_handler(CurKlineTest())
    quote_ctx.set_handler(RTDataTest())
    quote_ctx.set_handler(TickerTest())
    quote_ctx.set_handler(OrderBookTest())
    quote_ctx.set_handler(BrokerTest())
    quote_ctx.set_handler(SysNotifyTest())
    # quote_ctx.start()

    # 获取推送数据
    big_sub_codes = ['HK.02318', 'HK.02828', 'HK.00939', 'HK.01093', 'HK.01299', 'HK.00175',
                     'HK.01299', 'HK.01833', 'HK.00005', 'HK.00883', 'HK.00388', 'HK.01398',
                     'HK.01114', 'HK.02800', 'HK.02018', 'HK.03988', 'HK.00386', 'HK.01211',
                     'HK.00700', 'HK.01177',  'HK.02601', 'HK.02628', 'HK.HSImain']
    subtype_list = [SubType.QUOTE, SubType.ORDER_BOOK, SubType.TICKER, SubType.K_DAY, SubType.RT_DATA, SubType.BROKER]

    sub_codes =  ['HK.00700', 'HK.HSImain']

    # print("* get_owner_plate : {}\n".format(quote_ctx.get_owner_plate(code_list)))
    # print("* get_referencestock_list : {}\n".format(quote_ctx.get_referencestock_list(
    #     code_list[0], SecurityReferenceType.WARRANT)))
    # # print("* get_holding_change_list : {}\n".format(quote_ctx.get_holding_change_list(
    # #     "US.AAPL", StockHolder.EXECUTIVE, "2018-01-01", None)))
    #
    # print("* request_history_kline : {}\n".format(quote_ctx.request_history_kline(
    #     code_list[0], "2018-01-01", None, KLType.K_1M, AuType.QFQ, [KL_FIELD.ALL], 50000)))

    # 测试大量数据定阅
    # if len(big_sub_codes):
    #     print("* subscribe : {}\n".format(quote_ctx.subscribe(big_sub_codes, subtype_list)))

    """
    if True:
        print("* subscribe : {}\n".format(quote_ctx.subscribe(code_list, subtype_list)))
        print("* query_subscription : {}\n".format(quote_ctx.query_subscription(True)))
        sleep(60.1)
        print("* unsubscribe : {}\n".format(quote_ctx.unsubscribe(code_list, subtype_list)))
        print("* query_subscription : {}\n".format(quote_ctx.query_subscription(True)))
        sleep(1)
    """
    print("* subscribe : {}\n".format(quote_ctx.subscribe(sub_codes, subtype_list)))

    # # """
    # print("* get_stock_basicinfo : {}\n".format(quote_ctx.get_stock_basicinfo(Market.HK, SecurityType.ETF)))
    # print("* get_cur_kline : {}\n".format(quote_ctx.get_cur_kline(code_list[0], 10, SubType.K_DAY, AuType.QFQ)))
    #
    # print("* get_rt_data : {}\n".format(quote_ctx.get_rt_data(code_list[0])))
    # print("* get_rt_ticker : {}\n".format(quote_ctx.get_rt_ticker(code_list[0], 10)))
    #
    # print("* get_broker_queue : {}\n".format(quote_ctx.get_broker_queue(code_list[0])))
    # print("* get_order_book : {}\n".format(quote_ctx.get_order_book(code_list[0])))
    # print("* request_history_kline : {}\n".format(quote_ctx.request_history_kline('HK.00700', start='2017-06-20', end='2017-06-22')))
    # # """
    #
    # # """
    # print("* get_multi_points_history_kline : {}\n".format(quote_ctx.get_multi_points_history_kline(code_list, ['2017-06-20', '2017-06-22', '2017-06-23'], KL_FIELD.ALL,
    #                                                KLType.K_DAY, AuType.QFQ)))
    # print("* get_autype_list : {}\n".format(quote_ctx.get_autype_list("HK.00700")))
    #
    # print("* get_trading_days : {}\n".format(quote_ctx.get_trading_days(Market.HK, '2018-11-01', '2018-11-20')))
    #
    # print("* get_market_snapshot : {}\n".format(quote_ctx.get_market_snapshot('HK.21901')))
    # print("* get_market_snapshot : {}\n".format(quote_ctx.get_market_snapshot(code_list)))
    #
    # print("* get_plate_list : {}\n".format(quote_ctx.get_plate_list(Market.HK, Plate.ALL)))
    # print("* get_plate_stock : {}\n".format(quote_ctx.get_plate_stock('HK.BK1001')))
    # """

    # """
    sleep(15)
    quote_ctx.close()
    # """


def trade_hkcc_test():
    """
    A股通交易测试
    :return:
    """
    trd_ctx = OpenHKCCTradeContext(host='127.0.0.1', port=11111)
    trd_ctx.set_handler(TradeOrderTest())
    trd_ctx.set_handler(TradeDealTest())
    trd_ctx.start()

    # 交易请求必须先解锁 !!!
    pwd_unlock = '979899'
    print("* unlock_trade : {}\n".format(trd_ctx.unlock_trade(pwd_unlock)))

    print("* accinfo_query : {}\n".format(trd_ctx.accinfo_query()))
    print("* position_list_query : {}\n".format(trd_ctx.position_list_query(pl_ratio_min=-50, pl_ratio_max=50)))
    print("* order_list_query : {}\n".format(trd_ctx.order_list_query(status_filter_list=[OrderStatus.DISABLED])))
    print("* get_acc_list : {}\n".format(trd_ctx.get_acc_list()))
    print("* order_list_query : {}\n".format(trd_ctx.order_list_query(status_filter_list=[OrderStatus.SUBMITTED])))

    ret_code, ret_data = trd_ctx.place_order(0.1, 100, "SZ.000979", TrdSide.BUY)
    print("* place_order : {}\n".format(ret_data))
    if ret_code == RET_OK:
        order_id = ret_data['order_id'][0]
        print("* modify_order : {}\n".format(trd_ctx.modify_order(ModifyOrderOp.CANCEL, order_id, 0, 0)))

    print("* deal_list_query : {}\n".format(trd_ctx.deal_list_query(code="000979")))
    print("* history_order_list_query : {}\n".format(trd_ctx.history_order_list_query(status_filter_list=[OrderStatus.FILLED_ALL, OrderStatus.FILLED_PART],
                                           code="512310", start="", end="2018-2-1")))

    print("* history_deal_list_query : {}\n".format(trd_ctx.history_deal_list_query(code="", start="", end="2018-6-1")))

    sleep(10)
    trd_ctx.close()


def trade_hk_test():
    '''
    港股交易测试
    :return:
    '''
    trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
    trd_ctx.set_handler(TradeOrderTest())
    trd_ctx.set_handler(TradeDealTest())
    trd_ctx.start()

    # 交易请求必须先解锁 !!!
    pwd_unlock = '979899'
    print("* unlock_trade : {}\n".format(trd_ctx.unlock_trade(pwd_unlock)))

    # """
    print("* accinfo_query : {}\n".format(trd_ctx.accinfo_query()))
    print("* position_list_query : {}\n".format(trd_ctx.position_list_query(pl_ratio_min=-50, pl_ratio_max=50)))
    print("* order_list_query : {}\n".format(trd_ctx.order_list_query(status_filter_list=[OrderStatus.DISABLED])))
    print("* get_acc_list : {}\n".format(trd_ctx.get_acc_list()))
    print("* order_list_query : {}\n".format(trd_ctx.order_list_query(status_filter_list=[OrderStatus.SUBMITTED])))

    ret_code, ret_data = trd_ctx.place_order(700.0, 100, "HK.00700", TrdSide.SELL)
    print("* place_order : {}\n".format(ret_data))
    if ret_code == RET_OK:
        order_id = ret_data['order_id'][0]
        print("* modify_order : {}\n".format(trd_ctx.modify_order(ModifyOrderOp.CANCEL, order_id, 0, 0)))

    print("* deal_list_query : {}\n".format(trd_ctx.deal_list_query(code="00700")))
    print("* history_order_list_query : {}\n".format(trd_ctx.history_order_list_query(status_filter_list=[OrderStatus.FILLED_ALL, OrderStatus.FILLED_PART],
                                           code="00700", start="", end="2018-2-1")))

    print("* history_deal_list_query : {}\n".format(trd_ctx.history_deal_list_query(code="", start="", end="2018-6-1")))
    # """

    sleep(100000)
    trd_ctx.close()


if __name__ =="__main__":
    set_futu_debug_model(True)
    '''
    默认rsa密钥在futu.common下的conn_key.txt
    注意同步配置FutuOpenD的FTGateway.xml中的 rsa_private_key 字段
    '''
    # SysConfig.set_init_rsa_file()

    ''' 是否启用协议加密 '''
    # SysConfig.enable_proto_encrypt(False)

    '''设置通讯协议格式 '''
    # SysConfig.set_proto_fmt(ProtoFMT.Json)

    '''设置client信息'''
    # SysConfig.set_client_info('sample', 0)

    ''' 行情api测试 '''
    quote_test()

    ''' 交易api测试 '''
    # trade_hk_test()

    # trade_hkcc_test()



