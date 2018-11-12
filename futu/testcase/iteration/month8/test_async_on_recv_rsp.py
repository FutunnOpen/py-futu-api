#-*-coding:utf-8-*-

from futuquant import *
from futuquant.testcase.person.eva.utils.logUtil import Logs
import pandas

class TestAll(object):
    dir = 'mac20180831'


    def __init__(self, tradeEnv = TrdEnv.SIMULATE):
        # 加密通道
        # SysConfig.enable_proto_encrypt(True)
        # SysConfig.enable_proto_encrypt(True)

        pandas.set_option('display.width', 1000)
        pandas.set_option('max_columns', 1000)

        host = '127.0.0.1'
        port = 21111
        self.quote_ctx = OpenQuoteContext(host , port )
        self.quote_ctx.start()
        self.tradeEnv = tradeEnv

        if self.tradeEnv == TrdEnv.REAL:
            self.trade_cn = OpenHKCCTradeContext(host, port)  # A股通
        else:
            self.trade_cn = OpenCNTradeContext(host, port)  # web模拟交易

        self.trade_hk = OpenHKTradeContext(host, port)
        self.trade_us = OpenUSTradeContext(host, port)


    def test_on_recv_rsp(self):
        logger = Logs().getNewLogger('test_on_recv_rsp', TestAll.dir)

        #行情
        subTypes = [SubType.QUOTE, SubType.ORDER_BOOK, SubType.BROKER, SubType.TICKER, SubType.RT_DATA, SubType.K_1M,
                    SubType.K_5M, SubType.K_15M, SubType.K_30M, SubType.K_60M, SubType.K_DAY, SubType.K_WEEK,SubType.K_MON]
        print('subscribe ',self.quote_ctx.subscribe(code_list = ['HK.00700'], subtype_list=subTypes))
        handlers = [BrokerTest(), CurKlineTest(), OrderBookTest(), RTDataTest(), TickerTest(), StockQuoteTest()]
        #设置推送监听
        for h in handlers:
            self.quote_ctx.set_handler(h)

        #交易

        #设置推送监听
        self.trade_hk.set_handler(TradeOrderTest())
        self.trade_hk.set_handler(TradeDealTest())
        self.trade_us.set_handler(TradeOrderTest())
        self.trade_us.set_handler(TradeDealTest())
        self.trade_cn.set_handler(TradeOrderTest())
        self.trade_cn.set_handler(TradeDealTest())

        # 解锁交易unlock
        trade_pwd = '321321'
        logger.info('HK解锁交易')
        logger.info(self.trade_hk.unlock_trade(trade_pwd))
        logger.info('US解锁交易')
        logger.info(self.trade_us.unlock_trade(trade_pwd))
        logger.info('CN解锁交易')
        logger.info(self.trade_cn.unlock_trade(trade_pwd))

        # 股票信息
        price_hk = 3.98
        qty_hk = 500
        code_hk = 'HK.01357'
        price_us = 32.14
        qty_us = 2
        code_us = 'US.JD'
        price_cn = 10.15
        qty_cn = 100
        code_cn = 'SZ.000001'

        # 下单 place_order
        # 港股普通订单-买入
        logger.info('港股普通订单-买入')
        logger.info(self.trade_hk.place_order(price=price_hk, qty=qty_hk,
                                         code=code_hk,
                                         trd_side=TrdSide.BUY,
                                         order_type=OrderType.NORMAL,
                                         adjust_limit=0, trd_env=self.tradeEnv,
                                         acc_id=0))

        # 美股普通订单-买入
        logger.info('美股普通订单-买入')
        logger.info(self.trade_us.place_order(price=price_us, qty=qty_us,
                                         code=code_us,
                                         trd_side=TrdSide.BUY,
                                         order_type=OrderType.NORMAL,
                                         adjust_limit=0, trd_env=self.tradeEnv,
                                         acc_id=0))

        # A股普通订单-买入
        logger.info('A股普通订单-买入')
        logger.info(self.trade_cn.place_order(price=price_cn, qty=qty_cn,
                                         code=code_cn,
                                         trd_side=TrdSide.BUY,
                                         order_type=OrderType.NORMAL,
                                         adjust_limit=0,
                                         trd_env=self.tradeEnv, acc_id=0))

    def test_on_recv_rsp_nest(self):
        #回调中订阅并设置监听
        logger = Logs().getNewLogger('test_on_recv_rsp', TestAll.dir)

        subTypes = [SubType.QUOTE]
        print('set_handler(StockQuoteTest()) ',self.quote_ctx.set_handler(StockQuoteTest()))
        print('subscribe ', self.quote_ctx.subscribe(code_list=['HK.00700'], subtype_list=subTypes))

    def test_sub(self):

        subTypes = [SubType.BROKER]
        print('set_handler(BrokerTest()) ', self.quote_ctx.set_handler(BrokerTest()))
        print('subscribe ', self.quote_ctx.subscribe(code_list=['HK.00700'], subtype_list=subTypes))
        # time.sleep(20)
        # print('time.sleep(5)   end！')
        # self.quote_ctx.close()


    def test_quote(self,logger):
        logger.info('---------------test_quote()-----------------')

        logger.info('获取交易日 get_trading_days')
        logger.info(self.quote_ctx.get_trading_days(market=Market.HK, start=None, end=None))
        logger.info('获取股票信息 get_stock_basicinfo')
        logger.info(self.quote_ctx.get_stock_basicinfo(market=Market.HK, stock_type=SecurityType.STOCK, code_list=None))
        logger.info(self.quote_ctx.get_stock_basicinfo(market=Market.HK, stock_type=SecurityType.WARRANT, code_list=None))
        logger.info(self.quote_ctx.get_stock_basicinfo(market=Market.US, stock_type=SecurityType.STOCK, code_list=None))
        logger.info('获取复权因子 get_autype_list')
        logger.info(self.quote_ctx.get_autype_list(code_list=['HK.00388', 'US.AAPL', 'SZ.300104']))
        logger.info('获取市场快照 get_market_snapshot')
        logger.info(self.quote_ctx.get_market_snapshot(code_list=['HK.00388', 'US.AAPL', 'SZ.300104']))
        logger.info('获取板块集合下的子板块列表 get_plate_list')
        logger.info(self.quote_ctx.get_plate_list(market=Market.HK, plate_class=Plate.ALL))
        logger.info(self.quote_ctx.get_plate_list(market=Market.US, plate_class=Plate.ALL))
        logger.info(self.quote_ctx.get_plate_list(market=Market.SH, plate_class=Plate.ALL))
        logger.info('获取板块下的股票列表 get_plate_stock')
        logger.info(self.quote_ctx.get_plate_stock(plate_code='HK.BK1160'))
        logger.info(self.quote_ctx.get_plate_stock(plate_code='SH.BK0045'))
        logger.info('获取牛牛程序全局状态 get_global_state')
        logger.info(self.quote_ctx.get_global_state())
        logger.info('获取历史K线 get_history_kline')
        logger.info(
            self.quote_ctx.get_history_kline(code='HK.00388', start=None, end=None, ktype=KLType.K_DAY, autype=AuType.QFQ,
                                        fields=[KL_FIELD.ALL]))
        logger.info(
            self.quote_ctx.get_history_kline(code='US.AAPL', start=None, end=None, ktype=KLType.K_MON, autype=AuType.HFQ,
                                        fields=[KL_FIELD.ALL]))
        logger.info(
            self.quote_ctx.get_history_kline(code='SZ.300601', start=None, end=None, ktype=KLType.K_WEEK, autype=AuType.NONE,
                                        fields=[KL_FIELD.ALL]))
        logger.info('获取多支股票多个单点历史K线 get_multi_points_history_kline')
        logger.info(self.quote_ctx.get_multi_points_history_kline(code_list=['HK.00388', 'US.JD', 'SH.000001'],
                                                             dates=['2018-01-01', '2018-08-02'], fields=KL_FIELD.ALL,
                                                             ktype=KLType.K_15M, autype=AuType.HFQ,
                                                             no_data_mode=KLNoDataMode.BACKWARD))

        logger.info('订阅 subscribe-QUOTE')
        codes1 = ['HK.00388', 'HK.800000', 'US.AAPL', 'SH.601318', 'SH.000001', 'SZ.000001']
        logger.info(self.quote_ctx.subscribe(code_list=codes1, subtype_list=SubType.QUOTE))
        logger.info('获取报价 get_stock_quote')
        logger.info(self.quote_ctx.get_stock_quote(code_list=codes1))

        logger.info('订阅 subscribe-TICKER')
        codes2 = ['HK.00388','US.MSFT','SH.601998']
        logger.info(self.quote_ctx.subscribe(code_list=codes2, subtype_list=SubType.TICKER))
        logger.info('获取逐笔 get_rt_ticker')
        logger.info(self.quote_ctx.get_rt_ticker(code='HK.00388', num=1000))
        logger.info(self.quote_ctx.get_rt_ticker(code='US.MSFT', num=1000))
        logger.info(self.quote_ctx.get_rt_ticker(code='SH.601998', num=1000))

        logger.info('订阅 subscribe-KL')
        codes3 = ['HK.00388','US.FB','SZ.000885']
        logger.info(self.quote_ctx.subscribe(code_list=codes3, subtype_list=[SubType.K_5M,SubType.K_DAY,SubType.K_WEEK]))
        logger.info('获取实时K线 get_cur_kline')
        logger.info(self.quote_ctx.get_cur_kline(code='HK.00388', num=1000, ktype=SubType.K_5M, autype=AuType.QFQ))
        logger.info(self.quote_ctx.get_cur_kline(code='US.FB', num=500, ktype=SubType.K_DAY, autype=AuType.HFQ))
        logger.info(self.quote_ctx.get_cur_kline(code='SZ.000885', num=750, ktype=SubType.K_WEEK, autype=AuType.NONE))

        logger.info('订阅 subscribe-order_book')
        codes4 = ['HK.01810','US.AMZN']
        logger.info(self.quote_ctx.subscribe(code_list=codes4, subtype_list=SubType.ORDER_BOOK))
        logger.info('获取摆盘 get_order_book')
        logger.info(self.quote_ctx.get_order_book(code='HK.01810'))
        logger.info(self.quote_ctx.get_order_book(code='US.AMZN'))

        logger.info('订阅 subscribe-rt_data')
        codes5 = ['HK.01357','US.MDR','SZ.000565']
        logger.info(self.quote_ctx.subscribe(code_list=codes5, subtype_list=SubType.RT_DATA))
        logger.info('获取分时数据 get_rt_data')
        logger.info(self.quote_ctx.get_rt_data(code='HK.01357'))
        logger.info(self.quote_ctx.get_rt_data(code='US.MDR'))
        logger.info(self.quote_ctx.get_rt_data(code='SZ.000565'))

        logger.info('订阅 subscribe-BROKER')
        codes6 = ['HK.01478']
        logger.info(self.quote_ctx.subscribe(code_list=codes6, subtype_list=SubType.BROKER))
        logger.info('获取经纪队列 get_broker_queue')
        logger.info(self.quote_ctx.get_broker_queue(code='HK.01478'))

        logger.info('查询订阅 query_subscription')
        logger.info(self.quote_ctx.query_subscription(is_all_conn=True))

        time.sleep(61)
        logger.info('反订阅 unsubscribe')
        subTypes = [SubType.QUOTE, SubType.ORDER_BOOK, SubType.BROKER, SubType.TICKER, SubType.RT_DATA, SubType.K_1M,
                    SubType.K_5M, SubType.K_15M, SubType.K_30M, SubType.K_60M, SubType.K_DAY, SubType.K_WEEK,
                    SubType.K_MON]
        codes=codes1+codes2+codes3+codes4+codes5+codes6
        logger.info(self.quote_ctx.unsubscribe(code_list = codes, subtype_list = subTypes))

        logger.info('查询订阅 query_subscription')
        logger.info(self.quote_ctx.query_subscription(is_all_conn=True))

    def test_quote_async(self,logger):

        logger.info('---------------test_quote_async()-----------------')

        # 异步实时数据
        # 设置监听
        handlers = [CurKlineTest(), OrderBookTest(), RTDataTest(), TickerTest(), StockQuoteTest(), BrokerTest()]
        for handler in handlers:
            self.quote_ctx.set_handler(handler)
        # 订阅
        codes = ['HK.00388', 'US.AAPL', 'SH.601318']
        subTypes = [SubType.QUOTE, SubType.ORDER_BOOK, SubType.BROKER, SubType.TICKER, SubType.RT_DATA, SubType.K_1M,
                    SubType.K_5M, SubType.K_15M, SubType.K_30M, SubType.K_60M, SubType.K_DAY, SubType.K_WEEK,
                    SubType.K_MON]
        self.quote_ctx.subscribe(code_list=codes, subtype_list=subTypes)

    def test_trade(self,logger):

        logger.info('---------------test_trade()-----------------')
        # 上下文实例
        host = '127.0.0.1'
        port = 21111

        if self.tradeEnv == TrdEnv.REAL:
            self.trade_cn = OpenHKCCTradeContext(host, port)  # A股通
        else:
            self.trade_cn = OpenCNTradeContext(host, port)  # web模拟交易

            self.trade_hk = OpenHKTradeContext(host, port)
            self.trade_us = OpenUSTradeContext(host, port)

        # 解锁交易unlock
        trade_pwd = '123123'
        logger.info('HK解锁交易')
        logger.info(self.trade_hk.unlock_trade(trade_pwd))
        logger.info('US解锁交易')
        logger.info(self.trade_us.unlock_trade(trade_pwd))
        logger.info('CN解锁交易')
        logger.info(self.trade_cn.unlock_trade(trade_pwd))

        # 股票信息
        price_hk = 3.98
        qty_hk = 500
        code_hk = 'HK.01357'
        price_us = 32.14
        qty_us = 2
        code_us = 'US.JD'
        price_cn = 10.15
        qty_cn = 100
        code_cn = 'SZ.000001'

        # 查询最大可买可卖
        logger.info(code_hk + ' price=' + str(price_hk) + ' 最大可买可卖')
        logger.info(self.trade_hk.acctradinginfo_query(order_type=OrderType.NORMAL, code=code_hk, price=price_hk, order_id=0,
                                                  adjust_limit=0, trd_env=self.tradeEnv, acc_id=0, acc_index=0))
        logger.info(code_us + ' price=' + str(price_us) + ' 最大可买可卖')
        logger.info(self.trade_us.acctradinginfo_query(order_type=OrderType.NORMAL, code=code_us, price=price_us, order_id=0,
                                                  adjust_limit=0, trd_env=self.tradeEnv, acc_id=0, acc_index=0))
        logger.info(code_cn + 'price=' + str(price_cn) + ' 最大可买可卖')
        logger.info(self.trade_cn.acctradinginfo_query(order_type=OrderType.NORMAL, code=code_cn, price=price_cn, order_id=0,
                                                  adjust_limit=0, trd_env=self.tradeEnv, acc_id=0, acc_index=0))

        # 下单 place_order
        # 港股普通订单-买入
        logger.info('港股普通订单-买入')
        logger.info(self.trade_hk.place_order(price=price_hk, qty=qty_hk,
                                         code=code_hk,
                                         trd_side=TrdSide.BUY,
                                         order_type=OrderType.NORMAL,
                                         adjust_limit=0, trd_env=self.tradeEnv,
                                         acc_id=0))

        # 美股普通订单-买入
        logger.info('美股普通订单-买入')
        logger.info(self.trade_us.place_order(price=price_us, qty=qty_us,
                                         code=code_us,
                                         trd_side=TrdSide.BUY,
                                         order_type=OrderType.NORMAL,
                                         adjust_limit=0, trd_env=self.tradeEnv,
                                         acc_id=0))

        # A股普通订单-买入
        logger.info('A股普通订单-买入')
        logger.info(self.trade_cn.place_order(price=price_cn, qty=qty_cn,
                                         code=code_cn,
                                         trd_side=TrdSide.BUY,
                                         order_type=OrderType.NORMAL,
                                         adjust_limit=0,
                                         trd_env=self.tradeEnv, acc_id=0))

        # 查询今日订单 order_list_query
        ret_code_order_list_query_hk, ret_data_order_list_query_hk = self.trade_hk.order_list_query(order_id="",
                                                                                               status_filter_list=[],
                                                                                               code='', start='',
                                                                                               end='',
                                                                                               trd_env=self.tradeEnv,
                                                                                               acc_id=0)
        logger.info('港股今日订单 ' + str(ret_code_order_list_query_hk))
        logger.info(ret_data_order_list_query_hk)
        ret_code_order_list_query_us, ret_data_order_list_query_us = self.trade_us.order_list_query(order_id="",
                                                                                               status_filter_list=[],
                                                                                               code='', start='',
                                                                                               end='',
                                                                                               trd_env=self.tradeEnv,
                                                                                               acc_id=0)
        logger.info('美股今日订单 ' + str(ret_code_order_list_query_us))
        logger.info(ret_data_order_list_query_us)
        ret_code_order_list_query_cn, ret_data_order_list_query_cn = self.trade_cn.order_list_query(order_id="",
                                                                                               status_filter_list=[],
                                                                                               code='', start='',
                                                                                               end='',
                                                                                               trd_env=self.tradeEnv,
                                                                                               acc_id=0)
        logger.info('A股今日订单 ' + str(ret_code_order_list_query_cn))
        logger.info(ret_data_order_list_query_cn)

        # 修改订单modify_order
        order_ids_hk = ret_data_order_list_query_hk['order_id'].tolist()
        order_ids_us = ret_data_order_list_query_us['order_id'].tolist()
        order_ids_cn = ret_data_order_list_query_cn['order_id'].tolist()

        logger.info('港股改单，order_id = ' + order_ids_hk[0])
        logger.info(
            self.trade_hk.modify_order(modify_order_op=ModifyOrderOp.NORMAL, order_id=order_ids_hk[0], qty=qty_hk * 2,
                                  price=price_hk - 1, adjust_limit=0,
                                  trd_env=self.tradeEnv, acc_id=0))

        logger.info('美股改单，order_id = ' + order_ids_us[0])
        logger.info(
            self.trade_us.modify_order(modify_order_op=ModifyOrderOp.NORMAL, order_id=order_ids_us[0], qty=qty_us * 2,
                                  price=price_us - 1, adjust_limit=0,
                                  trd_env=self.tradeEnv, acc_id=0))

        # A股-修改订单数量/价格
        logger.info('A股改单，order_id = ' + order_ids_cn[0])
        logger.info(
            self.trade_cn.modify_order(modify_order_op=ModifyOrderOp.NORMAL, order_id= order_ids_cn[0], qty=qty_cn * 2,
                                  price=price_cn - 1, adjust_limit=0,
                                  trd_env=self.tradeEnv, acc_id=0))

        # 查询账户信息 accinfo_query
        logger.info('HK 账户信息')
        logger.info(self.trade_hk.accinfo_query(trd_env=self.tradeEnv, acc_id=0))
        logger.info('US 账户信息')
        logger.info(self.trade_us.accinfo_query(trd_env=self.tradeEnv, acc_id=0))
        logger.info('CN 账户信息')
        logger.info(self.trade_cn.accinfo_query(trd_env=self.tradeEnv, acc_id=0))

        # 查询持仓列表 position_list_query
        logger.info('HK 持仓列表')
        logger.info(
            self.trade_hk.position_list_query(code='', pl_ratio_min=None, pl_ratio_max=None, trd_env=self.tradeEnv, acc_id=0))
        logger.info('US 持仓列表')
        logger.info(
            self.trade_us.position_list_query(code='', pl_ratio_min=None, pl_ratio_max=None, trd_env=self.tradeEnv, acc_id=0))
        logger.info('CN 持仓列表')
        logger.info(
            self.trade_cn.position_list_query(code='', pl_ratio_min=None, pl_ratio_max=None, trd_env=self.tradeEnv, acc_id=0))

        # 查询历史订单列表 history_order_list_query
        logger.info('HK 历史订单列表')
        logger.info(self.trade_hk.history_order_list_query(status_filter_list=[], code='', start='', end='',
                                                      trd_env=self.tradeEnv, acc_id=0))
        logger.info('US 历史订单列表')
        logger.info(self.trade_us.history_order_list_query(status_filter_list=[], code='', start='', end='',
                                                      trd_env=self.tradeEnv, acc_id=0))
        logger.info('CN 历史订单列表')
        logger.info(self.trade_cn.history_order_list_query(status_filter_list=[], code='', start='', end='',
                                                      trd_env=self.tradeEnv, acc_id=0))

        # 查询今日成交列表 deal_list_query
        logger.info('HK 今日成交列表')
        logger.info(self.trade_hk.deal_list_query(code="", trd_env=self.tradeEnv, acc_id=0))
        logger.info('US 今日成交列表')
        logger.info(self.trade_us.deal_list_query(code="", trd_env=self.tradeEnv, acc_id=0))
        logger.info('CN 今日成交列表')
        logger.info(self.trade_cn.deal_list_query(code="", trd_env=self.tradeEnv, acc_id=0))

        # 查询历史成交列表 history_deal_list_query
        logger.info('HK 历史成交列表')
        logger.info(self.trade_hk.history_deal_list_query(code='', start='', end='', trd_env=self.tradeEnv, acc_id=0))
        logger.info('US 历史成交列表')
        logger.info(self.trade_us.history_deal_list_query(code='', start='', end='', trd_env=self.tradeEnv, acc_id=0))
        logger.info('CN 历史成交列表')
        logger.info(self.trade_cn.history_deal_list_query(code='', start='', end='', trd_env=self.tradeEnv, acc_id=0))


    def test_trade_async(self,logger):

        logger.info('---------------test_trade_async()-----------------')

        # 解锁交易unlock
        trade_pwd = '123123'
        logger.info('HK解锁交易')
        logger.info(self.trade_hk.unlock_trade(trade_pwd))
        logger.info('US解锁交易')
        logger.info(self.trade_us.unlock_trade(trade_pwd))
        logger.info('CN解锁交易')
        logger.info(self.trade_cn.unlock_trade(trade_pwd))
        # 设置监听
        handler_tradeOrder = TradeOrderTest()
        handler_tradeDealtrade = TradeDealTest()
        self.trade_hk.set_handler(handler_tradeOrder)
        self.trade_hk.set_handler(handler_tradeDealtrade)
        self.trade_us.set_handler(handler_tradeOrder)
        self.trade_us.set_handler(handler_tradeDealtrade)
        self.trade_cn.set_handler(handler_tradeOrder)
        self.trade_cn.set_handler(handler_tradeDealtrade)
        # 开启异步
        self.trade_hk.start()
        self.trade_us.start()
        self.trade_cn.start()

        # 股票信息
        price_hk = 3.98
        qty_hk = 500
        code_hk = 'HK.01357'
        price_us = 32.14
        qty_us = 2
        code_us = 'US.JD'
        price_cn = 10.15
        qty_cn = 100
        code_cn = 'SZ.000001'

        # 查询最大可买可卖
        logger.info(code_hk + ' price=' + str(price_hk) + ' 最大可买可卖')
        logger.info(self.trade_hk.acctradinginfo_query(order_type=OrderType.NORMAL, code=code_hk, price=price_hk, order_id=0,
                                                  adjust_limit=0, trd_env=self.tradeEnv, acc_id=0, acc_index=0))
        logger.info(code_us + ' price=' + str(price_us) + ' 最大可买可卖')
        logger.info(self.trade_us.acctradinginfo_query(order_type=OrderType.NORMAL, code=code_us, price=price_us, order_id=0,
                                                  adjust_limit=0, trd_env=self.tradeEnv, acc_id=0, acc_index=0))
        logger.info(code_cn + 'price=' + str(price_cn) + ' 最大可买可卖')
        logger.info(self.trade_cn.acctradinginfo_query(order_type=OrderType.NORMAL, code=code_cn, price=price_cn, order_id=0,
                                                  adjust_limit=0, trd_env=self.tradeEnv, acc_id=0, acc_index=0))

        # 下单 place_order
        # 港股普通订单-买入
        logger.info('港股普通订单-买入')
        logger.info(self.trade_hk.place_order(price=price_hk, qty=qty_hk,
                                         code=code_hk,
                                         trd_side=TrdSide.BUY,
                                         order_type=OrderType.NORMAL,
                                         adjust_limit=0, trd_env=self.tradeEnv,
                                         acc_id=0))

        # 美股普通订单-买入
        logger.info('美股普通订单-买入')
        logger.info(self.trade_us.place_order(price=price_us, qty=qty_us,
                                         code=code_us,
                                         trd_side=TrdSide.BUY,
                                         order_type=OrderType.NORMAL,
                                         adjust_limit=0, trd_env=self.tradeEnv,
                                         acc_id=0))

        # A股普通订单-买入
        logger.info('A股普通订单-买入')
        logger.info(self.trade_cn.place_order(price=price_cn, qty=qty_cn,
                                         code=code_cn,
                                         trd_side=TrdSide.BUY,
                                         order_type=OrderType.NORMAL,
                                         adjust_limit=0,
                                         trd_env=self.tradeEnv, acc_id=0))

        # 查询今日订单 order_list_query
        ret_code_order_list_query_hk, ret_data_order_list_query_hk = self.trade_hk.order_list_query(order_id="",
                                                                                               status_filter_list=[],
                                                                                               code='', start='',
                                                                                               end='',
                                                                                               trd_env=self.tradeEnv,
                                                                                               acc_id=0)
        logger.info('港股今日订单 ' + str(ret_code_order_list_query_hk))
        logger.info(ret_data_order_list_query_hk)
        ret_code_order_list_query_us, ret_data_order_list_query_us = self.trade_us.order_list_query(order_id="",
                                                                                               status_filter_list=[],
                                                                                               code='', start='',
                                                                                               end='',
                                                                                               trd_env=self.tradeEnv,
                                                                                               acc_id=0)
        logger.info('美股今日订单 ' + str(ret_code_order_list_query_us))
        logger.info(ret_data_order_list_query_us)
        ret_code_order_list_query_cn, ret_data_order_list_query_cn = self.trade_cn.order_list_query(order_id="",
                                                                                               status_filter_list=[],
                                                                                               code='', start='',
                                                                                               end='',
                                                                                               trd_env=self.tradeEnv,
                                                                                               acc_id=0)
        logger.info('A股今日订单 ' + str(ret_code_order_list_query_cn))
        logger.info(ret_data_order_list_query_cn)

        # 修改订单modify_order
        order_ids_hk = ret_data_order_list_query_hk['order_id'].tolist()
        order_ids_us = ret_data_order_list_query_us['order_id'].tolist()
        order_ids_cn = ret_data_order_list_query_cn['order_id'].tolist()

        logger.info('港股改单，order_id = ' + order_ids_hk[0])
        logger.info(
            self.trade_hk.modify_order(modify_order_op=ModifyOrderOp.NORMAL, order_id=order_ids_hk[0], qty=qty_hk * 2,
                                  price=price_hk - 1, adjust_limit=0,
                                  trd_env=self.tradeEnv, acc_id=0))

        logger.info('美股改单，order_id = ' + order_ids_us[0])
        logger.info(
            self.trade_us.modify_order(modify_order_op=ModifyOrderOp.NORMAL, order_id=order_ids_us[0], qty=qty_us * 2,
                                  price=price_us - 1, adjust_limit=0,
                                  trd_env=self.tradeEnv, acc_id=0))

    def test_symple(self,logger):

        logger.info('--------------------test_symple()-------------------------')

        logger.info('获取交易日 get_trading_days')
        logger.info(self.quote_ctx.get_trading_days(market=Market.HK, start='2018-8-1', end='2018-8-31'))
        trade_pwd = '123123'
        logger.info('HK解锁交易')
        logger.info(self.trade_hk.unlock_trade(trade_pwd))

        logger.info('港股普通订单-买入')
        price_hk = 3.98
        qty_hk = 500
        code_hk = 'HK.01357'
        tradeEnv = TrdEnv.REAL
        logger.info(self.trade_hk.place_order(price=price_hk, qty=qty_hk,
                                         code=code_hk,
                                         trd_side=TrdSide.BUY,
                                         order_type=OrderType.NORMAL,
                                         adjust_limit=0, trd_env=tradeEnv,
                                         acc_id=0))



class BrokerTest(BrokerHandlerBase):
    logger = Logs().getNewLogger('BrokerTest',TestAll.dir)
    global ta
    ta = TestAll()
    def on_recv_rsp(self, rsp_pb):
        ret_code,stock_code,ret_data = super(BrokerTest, self).on_recv_rsp(rsp_pb)
        #打印日志
        BrokerTest.logger.info('BrokerTest')
        BrokerTest.logger.info(stock_code)
        BrokerTest.logger.info(ret_code)
        BrokerTest.logger.info(ret_data)

        # global ta
        # ta.test_symple(BrokerTest.logger)

        # ta.test_quote(logger)
        # ta.test_quote_async(logger)
        # ta.test_trade(logger,True)
        # ta.test_trade_async(logger,False)

        return RET_OK,ret_data

class CurKlineTest(CurKlineHandlerBase):
    '''获取实时K线 get_cur_kline 和 CurKlineHandlerBase'''
    logger = Logs().getNewLogger('CurKlineTest',TestAll.dir)
    global ta
    ta = TestAll()
    def on_recv_rsp(self, rsp_pb):
        ret_code, ret_data = super(CurKlineTest, self).on_recv_rsp(rsp_pb)
        # 打印,记录日志
        CurKlineTest.logger.info('CurKlineTest')
        CurKlineTest.logger.info(ret_code)
        CurKlineTest.logger.info(ret_data)

        global ta
        ta.test_symple(CurKlineTest.logger)

        # ta.test_quote(logger)
        # ta.test_quote_async(logger)
        # ta.test_trade(logger, True)
        # ta.test_trade_async(logger,False)

        return RET_OK, ret_data

class OrderBookTest(OrderBookHandlerBase):
    logger = Logs().getNewLogger('OrderBookTest',TestAll.dir)
    global ta
    ta = TestAll()

    def on_recv_rsp(self, rsp_pb):
        ret_code ,ret_data = super(OrderBookTest, self).on_recv_rsp(rsp_pb)
        #打印
        OrderBookTest.logger.info('OrderBookTest')
        OrderBookTest.logger.info(ret_code)
        OrderBookTest.logger.info(ret_data)

        global ta
        ta.test_symple(OrderBookTest.logger)

        # ta.test_quote(logger)
        # ta.test_quote_async(logger)
        # ta.test_trade(logger, True)
        # ta.test_trade_async(logger,False)

        return RET_OK, ret_data

class RTDataTest(RTDataHandlerBase):
    logger = Logs().getNewLogger('RTDataTest',TestAll.dir)
    global ta
    ta = TestAll()
    def on_recv_rsp(self, rsp_pb):
        ret_code,ret_data = super(RTDataTest, self).on_recv_rsp(rsp_pb)
        #打印信息
        RTDataTest.logger.info('RTDataTest')
        RTDataTest.logger.info(ret_code)
        RTDataTest.logger.info(ret_data)

        global ta
        ta.test_symple(RTDataTest.logger)

        # ta.test_quote(logger)
        # ta.test_quote_async(logger)
        # ta.test_trade(logger, True)
        # ta.test_trade_async(logger,False)

        return RET_OK,ret_data

class TickerTest(TickerHandlerBase):
    '''获取逐笔 get_rt_ticker 和 TickerHandlerBase'''
    logger = Logs().getNewLogger('TickerTest',TestAll.dir)
    global ta
    ta = TestAll()

    def on_recv_rsp(self, rsp_pb):
        ret_code, ret_data = super(TickerTest, self).on_recv_rsp(rsp_pb)
        # 打印,记录日志
        TickerTest.logger.info('TickerTest')
        TickerTest.logger.info(ret_code)
        TickerTest.logger.info(ret_data)

        global ta
        ta.test_symple(TickerTest.logger)

        # ta.test_quote(logger)
        # ta.test_quote_async(logger)
        # ta.test_trade(logger, True)
        # ta.test_trade_async(logger,False)

        return RET_OK, ret_data

class StockQuoteTest(StockQuoteHandlerBase):
    # 获取报价get_stock_quote和StockQuoteHandlerBase
    logger = Logs().getNewLogger('StockQuoteTest',TestAll.dir)
    global ta
    ta = TestAll()

    def on_recv_rsp(self, rsp_str):
        ret_code, ret_data = super(StockQuoteTest,self).on_recv_rsp(rsp_str) # 基类的on_recv_rsp方法解包返回了报价信息，格式与get_stock_quote一样
        #打印,记录日志
        StockQuoteTest.logger.info('StockQuoteTest')
        StockQuoteTest.logger.info(ret_code)
        StockQuoteTest.logger.info(ret_data)

        global ta
        ta.test_sub()

        # ta.test_symple(StockQuoteTest.logger)

        # ta.test_quote(logger)
        # ta.test_quote_async(logger)
        # ta.test_trade(logger, True)
        # ta.test_trade_async(logger,False)

        return RET_OK, ret_data


class TradeOrderTest(TradeOrderHandlerBase):
    '''订单状态推送'''
    logger = Logs().getNewLogger('TradeOrderTest',TestAll.dir)
    global ta
    ta = TestAll()

    def on_recv_rsp(self, rsp_pb):
        ret_code,ret_data = super(TradeOrderTest, self).on_recv_rsp(rsp_pb)
        TradeOrderTest.logger.info('TradeOrderHandlerBase')
        TradeOrderTest.logger.info(ret_code)
        TradeOrderTest.logger.info(ret_data)

        global ta
        ta.test_symple(TradeOrderTest.logger)

        # ta.test_quote(logger)
        # ta.test_quote_async(logger)
        # ta.test_trade(logger, True)
        # ta.test_trade_async(logger,False)

        return RET_OK,ret_data

class TradeDealTest(TradeDealHandlerBase):
    '''订单成交推送 '''
    logger = Logs().getNewLogger('TradeDealTest', TestAll.dir)
    global ta
    ta = TestAll()

    def on_recv_rsp(self, rsp_pb):
        ret_code,ret_data = super(TradeDealTest, self).on_recv_rsp(rsp_pb)
        TradeDealTest.logger.info('TradeDealHandlerBase')
        TradeDealTest. logger.info(ret_code)
        TradeDealTest.logger.info(ret_data)

        global ta
        ta.test_symple(TradeDealTest.logger)

        # ta.test_quote(logger)
        # ta.test_quote_async(logger)
        # ta.test_trade(logger, True)
        # ta.test_trade_async(logger,False)

        return RET_OK,ret_data


if __name__ =='__main__':
    ta = TestAll()
    ta.test_on_recv_rsp_nest()
    # ta.test_on_recv_rsp(TrdEnv.REAL)