#-*-coding:utf-8-*-
from futuquant import *
import pandas

class Test(object):
    # 8月迭代相关接口特性简单体验

    def __init__(self):
        pandas.set_option('max_columns', 100)
        pandas.set_option('display.width', 1000)

    def test_quote(self):
        quote_ctx = OpenQuoteContext(host = '172.18.10.58', port = 21111)

        #get_holding_change_list获取高管持仓
        print(quote_ctx.get_holding_change_list(code='US.DIS', holder_type=StockHolder.EXECUTIVE, start=None, end=None))

        #get_owner_plate获取股票行业分类
        print(quote_ctx.get_owner_plate('HK.800000'))

        # request_history_kline请求历史K线
        req_key = None
        for i in range(10):
            print(i)
            ret_code, ret_data, req_key = quote_ctx.request_history_kline(code='HK.00700',start='2018-8-1', end='2018-8-16',ktype=KLType.K_1M,autype=AuType.QFQ,fields=[KL_FIELD.ALL],max_count=331,page_req_key=req_key)
            print(ret_data)

        #美股期权行情
        subtypes = [SubType.QUOTE, SubType.ORDER_BOOK, SubType.BROKER, SubType.TICKER, SubType.RT_DATA, SubType.K_1M,
                    SubType.K_5M, SubType.K_15M, SubType.K_60M, SubType.K_DAY]
        print('订阅',quote_ctx.subscribe(code_list=['US.AAPL180928C225000'], subtype_list=subtypes))
        print('查询订阅',quote_ctx.query_subscription())
        print('获取报价',quote_ctx.get_stock_quote(code_list = ['US.AAPL180928C225000','US.AAPL']))
        print('获取逐笔',quote_ctx.get_rt_ticker(code='US.AAPL180928C225000', num=1000))
        print('获取分时',quote_ctx.get_rt_data(code = 'US.AAPL180928C225000'))
        print('获取摆盘',quote_ctx.get_order_book(code = 'US.AAPL180928C225000'))
        print('获取实时K线',quote_ctx.get_cur_kline(code = 'US.AAPL180928C225000', num=200, ktype=SubType.K_5M, autype=AuType.HFQ))
        print('请求历史K线',quote_ctx.request_history_kline(code = 'US.AAPL180928C225000',start=None,end=None,ktype=KLType.K_DAY,autype=AuType.QFQ,fields=KL_FIELD.ALL_REAL,max_count=1000,page_req_key=None))

        #通过标的股查询期权get_option_chain
        print(quote_ctx.get_option_chain(code = 'US.DIS', start='2018-9-1',end='2018-9-30', option_type=OptionType.ALL,option_cond_type=OptionCondType.OUTSIDE))

        #get_market_snapshot查询美股期权行情
        print(quote_ctx.get_market_snapshot(code_list=['US.AAPL180928C225000']))

        #get_market_snapshot正股增加动态PE
        print(quote_ctx.get_market_snapshot(code_list = ['HK.00700','US.AAPL','SZ.000001']))


    def test_trade(self):
        host = '172.18.10.58'
        port = 21112
        trade_us = OpenUSTradeContext(host, port)

        # 添加入参acc_index
        # 美股期权交易
        print(trade_us.unlock_trade('123123'))
        print('下单',trade_us.place_order(price = 5.13 ,qty = 2, code = 'US.AAPL180928C222500', trd_side=TrdSide.SELL, order_type=OrderType.NORMAL,adjust_limit=0, trd_env=TrdEnv.REAL, acc_id=0, acc_index=1))
        print('修改订单',trade_us.modify_order(modify_order_op=ModifyOrderOp.CANCEL, order_id = '5192778383921057258', qty = 2, price = 0,adjust_limit = 0,trd_env = TrdEnv.REAL,acc_id = 0,acc_index = 1))
        print('查询最大可买可卖',trade_us.acctradinginfo_query(order_type=OrderType.NORMAL, code='HK.00700', price=358,order_id=0, adjust_limit=0, trd_env=TrdEnv.REAL, acc_id=0,acc_index=1))
        print('查询持仓列表',trade_us.position_list_query(code='', pl_ratio_min=None, pl_ratio_max=0.5, trd_env=TrdEnv.REAL, acc_id=0,acc_index=1))
        print('查询账户信息',trade_us.accinfo_query(trd_env=TrdEnv.REAL, acc_id=0))
        print('查询今日订单列表',trade_us.order_list_query(order_id="", status_filter_list=[], code='', start='', end='',trd_env=TrdEnv.REAL,acc_id=0,acc_index=1))
        print('查询历史订单列表',trade_us.history_order_list_query(status_filter_list=[], code='', start='', end='',trd_env=TrdEnv.REAL, acc_id=1))
        print('查询今日成交列表',trade_us.deal_list_query(code="", trd_env=TrdEnv.REAL, acc_id=0,acc_index=1))
        print('查询历史成交列表',trade_us.history_deal_list_query(code='', start='', end='', trd_env=TrdEnv.REAL, acc_id=0, acc_index =1))

if __name__ == '__main__':
    test = Test()
    test.test_quote()
    test.test_trade()
