#-*-coding:utf-8-*-

from futu import *
import pandas
import logging


class Log(object):
    def get_logger(self,fName):
        logger = logging.getLogger(fName)
        log_abs_name = os.getcwd() + os.path.sep +'log'+os.path.sep+ os.path.sep +fName + str((int)(time.time())) + '.txt'
        logger.info(log_abs_name + '\n')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler = logging.FileHandler(log_abs_name)
        handler.setFormatter(formatter)
        console = logging.StreamHandler(stream=sys.stdout)

        logger.addHandler(handler)  # 设置日志输出到文件
        logger.addHandler(console)  # 设置日志输出到屏幕控制台
        logger.setLevel(logging.DEBUG)  # 设置打印的日志等级
        return logger


class BeforePublishTest(object):
    #上线前测试用例，遍历所有接口保证可执行

    def __init__(self):
        pandas.set_option('max_columns',100)
        pandas.set_option('display.width',1000)
        # self.host = '172.18.10.58'
        self.host = '127.0.0.1'
        self.port_quote = 11111
        self.port_trade = 11112 # 测试环境


    def test_quotation(self):
        #行情接口测试

        #日志
        logger = Log().get_logger('quotation')

        #上下文实例
        quote_ctx = OpenQuoteContext(self.host, self.port_quote)
        quote_ctx.start()
        
        #同步接口
        logger.info('获取交易日 get_trading_days')
        logger.info(quote_ctx.get_trading_days(market = Market.HK, start=None, end=None))
        logger.info('获取股票信息 get_stock_basicinfo')
        logger.info(quote_ctx.get_stock_basicinfo(market = Market.HK, stock_type=SecurityType.STOCK, code_list=None))
        logger.info(quote_ctx.get_stock_basicinfo(market=Market.HK, stock_type=SecurityType.WARRANT, code_list=None))
        logger.info(quote_ctx.get_stock_basicinfo(market=Market.US, stock_type=SecurityType.STOCK, code_list=None))
        logger.info('获取复权因子 get_autype_list')
        logger.info(quote_ctx.get_autype_list(code_list = ['HK.00700','US.AAPL','SZ.300104']))
        logger.info('获取市场快照 get_market_snapshot')
        logger.info(quote_ctx.get_market_snapshot(code_list = ['HK.00700','US.AAPL','SZ.300104']))
        logger.info('获取板块集合下的子板块列表 get_plate_list')
        logger.info(quote_ctx.get_plate_list( market = Market.HK, plate_class = Plate.ALL))
        logger.info(quote_ctx.get_plate_list(market=Market.US, plate_class=Plate.ALL))
        logger.info(quote_ctx.get_plate_list(market=Market.SH, plate_class=Plate.ALL))
        logger.info('获取板块下的股票列表 get_plate_stock')
        logger.info(quote_ctx.get_plate_stock(plate_code = 'HK.BK1160'))
        logger.info(quote_ctx.get_plate_stock(plate_code='SH.BK0045'))
        logger.info('获取牛牛程序全局状态 get_global_state')
        logger.info(quote_ctx.get_global_state())
        logger.info('获取历史K线 get_history_kline')
        logger.info(quote_ctx.get_history_kline(code='HK.00700',start=None,end=None,ktype=KLType.K_DAY,autype=AuType.QFQ,fields=[KL_FIELD.ALL]))
        logger.info(quote_ctx.get_history_kline(code='US.AAPL', start=None, end=None, ktype=KLType.K_MON, autype=AuType.HFQ,fields=[KL_FIELD.ALL]))
        logger.info(quote_ctx.get_history_kline(code='SZ.300601', start=None, end=None, ktype=KLType.K_WEEK, autype=AuType.NONE,fields=[KL_FIELD.ALL]))
        logger.info('获取多支股票多个单点历史K线 get_multi_points_history_kline')
        logger.info(quote_ctx.get_multi_points_history_kline(code_list = ['HK.00700','US.JD','SH.000001'],dates=['2018-01-01', '2018-08-02'],fields=KL_FIELD.ALL,ktype=KLType.K_15M,autype=AuType.HFQ,no_data_mode=KLNoDataMode.BACKWARD))

        logger.info('订阅 subscribe-QUOTE')
        codes1 = ['HK.00700', 'HK.800000', 'US.AAPL', 'SH.601318', 'SH.000001', 'SZ.000001']
        logger.info(quote_ctx.subscribe(code_list=codes1, subtype_list=SubType.QUOTE))
        logger.info('获取报价 get_stock_quote')
        logger.info(quote_ctx.get_stock_quote(code_list=codes1))

        logger.info('订阅 subscribe-TICKER')
        codes2 = ['HK.00388','US.MSFT','SH.601998']
        logger.info(quote_ctx.subscribe(code_list=codes2, subtype_list=SubType.TICKER))
        logger.info('获取逐笔 get_rt_ticker')
        logger.info(quote_ctx.get_rt_ticker(code='HK.00388', num=1000))
        logger.info(quote_ctx.get_rt_ticker(code='US.MSFT', num=1000))
        logger.info(quote_ctx.get_rt_ticker(code='SH.601998', num=1000))

        logger.info('订阅 subscribe-KL')
        codes3 = ['HK.00772','US.FB','SZ.000885']
        logger.info(quote_ctx.subscribe(code_list=codes3, subtype_list=[SubType.K_5M,SubType.K_DAY,SubType.K_WEEK]))
        logger.info('获取实时K线 get_cur_kline')
        logger.info(quote_ctx.get_cur_kline(code='HK.00772', num=1000, ktype=SubType.K_5M, autype=AuType.QFQ))
        logger.info(quote_ctx.get_cur_kline(code='US.FB', num=500, ktype=SubType.K_DAY, autype=AuType.HFQ))
        logger.info(quote_ctx.get_cur_kline(code='SZ.000885', num=750, ktype=SubType.K_WEEK, autype=AuType.NONE))

        logger.info('订阅 subscribe-order_book')
        codes4 = ['HK.01810','US.AMZN']
        logger.info(quote_ctx.subscribe(code_list=codes4, subtype_list=SubType.ORDER_BOOK))
        logger.info('获取摆盘 get_order_book')
        logger.info(quote_ctx.get_order_book(code='HK.01810'))
        logger.info(quote_ctx.get_order_book(code='US.AMZN'))

        logger.info('订阅 subscribe-rt_data')
        codes5 = ['HK.01357','US.MDR','SZ.000565']
        logger.info(quote_ctx.subscribe(code_list=codes5, subtype_list=SubType.RT_DATA))
        logger.info('获取分时数据 get_rt_data')
        logger.info(quote_ctx.get_rt_data(code='HK.01357'))
        logger.info(quote_ctx.get_rt_data(code='US.MDR'))
        logger.info(quote_ctx.get_rt_data(code='SZ.000565'))

        logger.info('订阅 subscribe-BROKER')
        codes6 = ['HK.01478']
        logger.info(quote_ctx.subscribe(code_list=codes6, subtype_list=SubType.BROKER))
        logger.info('获取经纪队列 get_broker_queue')
        logger.info(quote_ctx.get_broker_queue(code='HK.01478'))

        logger.info('查询订阅 query_subscription')
        logger.info(quote_ctx.query_subscription(is_all_conn=True))
        logger.info(quote_ctx.get_order_detail('SZ.000001'))
        time.sleep(61)
        logger.info('反订阅 unsubscribe')
        subTypes = [SubType.QUOTE, SubType.ORDER_BOOK, SubType.BROKER, SubType.TICKER, SubType.RT_DATA, SubType.K_1M,
                    SubType.K_5M, SubType.K_15M, SubType.K_30M, SubType.K_60M, SubType.K_DAY, SubType.K_WEEK,
                    SubType.K_MON]
        codes=codes1+codes2+codes3+codes4+codes5+codes6
        logger.info(quote_ctx.unsubscribe(code_list = codes, subtype_list = subTypes))

        logger.info('查询订阅 query_subscription')
        logger.info(quote_ctx.query_subscription(is_all_conn=True))

        #异步实时数据
        # 设置监听
        handlers = [CurKlineTest(), OrderBookTest(), RTDataTest(), TickerTest(), StockQuoteTest(), BrokerTest()]
        for handler in handlers:
            quote_ctx.set_handler(handler)
        # 订阅
        codes = ['HK.00700', 'US.AAPL', 'SH.601318']
        quote_ctx.subscribe(code_list=codes, subtype_list=subTypes)
        # time.sleep(5 * 60)  # 订阅5分钟
        # quote_ctx.stop()
        # quote_ctx.close()

    def test_trade(self,tradeEnv = TrdEnv.REAL):
        #交易接口测试

        #日志
        logger = Log().get_logger('trade_'+tradeEnv)


        #上下文实例
        trade_hk = OpenHKTradeContext(self.host, self.port_trade)
        trade_us = OpenUSTradeContext(self.host, self.port_trade)
        if tradeEnv == TrdEnv.REAL:
            trade_cn = OpenHKCCTradeContext(self.host, self.port_trade)   #A股通
        else:
            trade_cn = OpenCNTradeContext(self.host, self.port_trade)   #web模拟交易
        logger.info('交易环境：'+tradeEnv)
        #解锁交易unlock
        trade_pwd = '123123'
        logger.info('HK解锁交易')
        logger.info(trade_hk.unlock_trade(trade_pwd))
        logger.info('US解锁交易')
        logger.info(trade_us.unlock_trade(trade_pwd))
        logger.info('CN解锁交易')
        logger.info(trade_cn.unlock_trade(trade_pwd))
        print(trade_hk.get_acc_list())
        # 设置监听
        handler_tradeOrder = TradeOrderTest()
        handler_tradeDealtrade = TradeDealTest()
        trade_hk.set_handler(handler_tradeOrder)
        trade_hk.set_handler(handler_tradeDealtrade)
        trade_us.set_handler(handler_tradeOrder)
        trade_us.set_handler(handler_tradeDealtrade)
        trade_cn.set_handler(handler_tradeOrder)
        trade_cn.set_handler(handler_tradeDealtrade)
        # 开启异步
        trade_hk.start()
        trade_us.start()
        trade_cn.start()

        #股票信息
        price_hk = 5.9
        qty_hk = 500
        code_hk = 'HK.01357'
        price_us = 24.1
        qty_us = 2
        code_us = 'US.JD'
        price_cn = 10.15
        qty_cn = 100
        code_cn = 'SZ.000001'
        
        #查询最大可买可卖
        logger.info(code_hk+' price='+str(price_hk)+' 最大可买可卖')
        logger.info(trade_hk.acctradinginfo_query(order_type = OrderType.NORMAL, code=code_hk, price=price_hk, order_id = 0, adjust_limit=0, trd_env=tradeEnv, acc_id=0, acc_index=0))
        logger.info(code_us+' price='+str(price_us)+' 最大可买可卖')
        logger.info(trade_us.acctradinginfo_query(order_type=OrderType.NORMAL, code=code_us, price=price_us, order_id=0,
                                            adjust_limit=0, trd_env=tradeEnv, acc_id=0, acc_index=0))
        logger.info(code_cn+'price='+str(price_cn)+' 最大可买可卖')
        logger.info(trade_cn.acctradinginfo_query(order_type=OrderType.NORMAL, code=code_cn, price=price_cn, order_id=0,
                                            adjust_limit=0, trd_env=tradeEnv, acc_id=0, acc_index=0))

        # 下单 place_order
        for i in range(3):
            print(i)
            #港股普通订单-买入
            logger.info('港股普通订单-买入')
            logger.info(trade_hk.place_order(price=price_hk - i, qty=qty_hk * (i+1),
                                 code=code_hk,
                                 trd_side=TrdSide.BUY,
                                 order_type=OrderType.NORMAL,
                                 adjust_limit=0, trd_env=tradeEnv,
                                 acc_id=0))

            #港股普通订单-卖出
            logger.info('港股普通订单-卖出')
            logger.info(trade_hk.place_order(price=price_hk + i, qty=qty_hk * (i+1),
                                       code=code_hk,
                                       trd_side=TrdSide.SELL,
                                       order_type=OrderType.NORMAL,
                                       adjust_limit=0, trd_env=tradeEnv,
                                       acc_id=0))
            #美股普通订单-买入
            logger.info('美股普通订单-买入')
            logger.info(trade_us.place_order(price=price_us - i, qty=qty_us * (i+1),
                                       code=code_us,
                                       trd_side=TrdSide.BUY,
                                       order_type=OrderType.NORMAL,
                                       adjust_limit=0, trd_env=tradeEnv,
                                       acc_id=0))
            # 美股普通订单-卖出
            logger.info('美股普通订单-卖出')
            logger.info(trade_us.place_order(price=price_us + i, qty=qty_us * (i+1),
                                 code=code_us,
                                 trd_side=TrdSide.SELL,
                                 order_type=OrderType.NORMAL,
                                 adjust_limit=0, trd_env=tradeEnv,
                                 acc_id=0))
            #A股普通订单-买入
            logger.info('A股普通订单-买入')
            logger.info(trade_cn.place_order(price=price_cn + i, qty=qty_cn * (i+1),
                                      code=code_cn,
                                      trd_side=TrdSide.BUY,
                                      order_type=OrderType.NORMAL,
                                      adjust_limit=0,
                                      trd_env=tradeEnv, acc_id=0))
            logger.info('A股普通订单-卖出')
            logger.info(trade_cn.place_order(price=price_cn + i, qty=qty_cn * (i+1),
                                            code=code_cn,
                                            trd_side=TrdSide.SELL,
                                            order_type=OrderType.NORMAL,
                                            adjust_limit=0,
                                            trd_env=tradeEnv, acc_id=0))

        #查询今日订单 order_list_query
        ret_code_order_list_query_hk, ret_data_order_list_query_hk = trade_hk.order_list_query(order_id="",
                                                                                               status_filter_list=[],
                                                                                               code='', start='',
                                                                                               end='',
                                                                                               trd_env=tradeEnv,
                                                                                               acc_id=0)
        logger.info('港股今日订单 '+str(ret_code_order_list_query_hk))
        logger.info(ret_data_order_list_query_hk)
        ret_code_order_list_query_us, ret_data_order_list_query_us = trade_us.order_list_query(order_id="",
                                                                                               status_filter_list=[],
                                                                                               code='', start='',
                                                                                               end='',
                                                                                               trd_env=tradeEnv,
                                                                                               acc_id=0)
        logger.info('美股今日订单 '+str(ret_code_order_list_query_us))
        logger.info(ret_data_order_list_query_us)
        ret_code_order_list_query_cn, ret_data_order_list_query_cn = trade_cn.order_list_query(order_id="",
                                                                                                    status_filter_list=[],
                                                                                                    code='', start='',
                                                                                                    end='',
                                                                                                    trd_env=tradeEnv,
                                                                                                    acc_id=0)
        logger.info('A股今日订单 '+str(ret_code_order_list_query_cn))
        logger.info(ret_data_order_list_query_cn)

        # 修改订单modify_order
        order_ids_hk = ret_data_order_list_query_hk['order_id'].tolist()
        order_ids_us = ret_data_order_list_query_us['order_id'].tolist()
        order_ids_cn = ret_data_order_list_query_cn['order_id'].tolist()

        for order_id_hk in order_ids_hk:
            #港股-修改订单数量/价格
            logger.info('港股改单，order_id = '+order_id_hk)
            logger.info(trade_hk.modify_order(modify_order_op=ModifyOrderOp.NORMAL, order_id=order_id_hk , qty=qty_hk*2, price=price_hk-1, adjust_limit=0,
                                    trd_env=tradeEnv, acc_id=0))
            time.sleep(2)
            #撤单
            logger.info('港股撤单，order_id = '+order_id_hk)
            logger.info(trade_hk.modify_order(modify_order_op=ModifyOrderOp.CANCEL, order_id=order_id_hk, qty=0, price=0, adjust_limit=0,
                                      trd_env=tradeEnv, acc_id=0))

        for order_id_us in order_ids_us:
            #美股-修改订单数量/价格
            logger.info('美股改单，order_id = '+order_id_us)
            logger.info(trade_us.modify_order(modify_order_op=ModifyOrderOp.NORMAL, order_id=order_id_us , qty=qty_us*2, price=price_us-1, adjust_limit=0,
                                    trd_env=tradeEnv, acc_id=0))
            time.sleep(2)
            #撤单
            logger.info('美股撤单，order_id = '+ order_id_us)
            logger.info(trade_us.modify_order(modify_order_op=ModifyOrderOp.CANCEL, order_id=order_id_us, qty=0, price=0, adjust_limit=0,
                                      trd_env=tradeEnv, acc_id=0))

        for order_id_cn in order_ids_cn:
            #A股-修改订单数量/价格
            logger.info('A股改单，order_id = '+order_id_cn)
            logger.info(trade_cn.modify_order(modify_order_op=ModifyOrderOp.NORMAL, order_id=order_id_cn , qty=qty_cn*2, price=price_cn-1, adjust_limit=0,
                                    trd_env=tradeEnv, acc_id=0))
            time.sleep(2)
            #撤单
            logger.info('A股撤单，order_id = '+order_id_cn)
            logger.info(trade_cn.modify_order(modify_order_op=ModifyOrderOp.CANCEL, order_id=order_id_cn, qty=0, price=0, adjust_limit=0,
                                      trd_env=tradeEnv, acc_id=0))

        #查询账户信息 accinfo_query
        logger.info('HK 账户信息')
        logger.info(trade_hk.accinfo_query(trd_env=tradeEnv, acc_id=0))
        logger.info('US 账户信息')
        logger.info(trade_us.accinfo_query(trd_env=tradeEnv, acc_id=0))
        logger.info('CN 账户信息')
        logger.info(trade_cn.accinfo_query(trd_env=tradeEnv, acc_id=0))

        #查询持仓列表 position_list_query
        logger.info('HK 持仓列表')
        logger.info(trade_hk.position_list_query( code='', pl_ratio_min=None, pl_ratio_max=None, trd_env=tradeEnv, acc_id=0))
        logger.info('US 持仓列表')
        logger.info(trade_us.position_list_query(code='', pl_ratio_min=None, pl_ratio_max=None, trd_env=tradeEnv, acc_id=0))
        logger.info('CN 持仓列表')
        logger.info(trade_cn.position_list_query(code='', pl_ratio_min=None, pl_ratio_max=None, trd_env=tradeEnv, acc_id=0))

        #查询历史订单列表 history_order_list_query
        logger.info('HK 历史订单列表')
        logger.info(trade_hk.history_order_list_query(status_filter_list=[], code='', start='', end='',
                                 trd_env=tradeEnv, acc_id=0))
        logger.info('US 历史订单列表')
        logger.info(trade_us.history_order_list_query(status_filter_list=[], code='', start='', end='',
                                                trd_env=tradeEnv, acc_id=0))
        logger.info('CN 历史订单列表')
        logger.info(trade_cn.history_order_list_query(status_filter_list=[], code='', start='', end='',
                                                trd_env=tradeEnv, acc_id=0))

        #查询今日成交列表 deal_list_query
        logger.info('HK 今日成交列表')
        logger.info(trade_hk.deal_list_query(code="", trd_env=tradeEnv, acc_id=0))
        logger.info('US 今日成交列表')
        logger.info(trade_us.deal_list_query(code="", trd_env=tradeEnv, acc_id=0))
        logger.info('CN 今日成交列表')
        logger.info(trade_cn.deal_list_query(code="", trd_env=tradeEnv, acc_id=0))

        #查询历史成交列表 history_deal_list_query
        logger.info('HK 历史成交列表')
        logger.info(trade_hk.history_deal_list_query(code = '', start='', end='', trd_env=tradeEnv, acc_id=0))
        logger.info('US 历史成交列表')
        logger.info(trade_us.history_deal_list_query(code='', start='', end='', trd_env=tradeEnv, acc_id=0))
        logger.info('CN 历史成交列表')
        logger.info(trade_cn.history_deal_list_query(code='', start='', end='', trd_env=tradeEnv, acc_id=0))
        trade_hk.close()
        trade_us.close()
        trade_cn.close()


    
class CurKlineTest(CurKlineHandlerBase):
    '''获取实时K线 get_cur_kline 和 CurKlineHandlerBase'''
    logger = Log().get_logger('CurKlineTest')
    def on_recv_rsp(self, rsp_pb):
        ret_code, ret_data = super(CurKlineTest, self).on_recv_rsp(rsp_pb)
        # 打印,记录日志
        CurKlineTest.logger.info('CurKlineHandlerBase ')
        CurKlineTest.logger.info(ret_code)
        CurKlineTest.logger.info(ret_data)
        return RET_OK, ret_data


class OrderBookTest(OrderBookHandlerBase):
    '''买卖经济推送'''
    logger = Log().get_logger('OrderBookTest')
    def on_recv_rsp(self, rsp_pb):
        ret_code, ret_data = super(OrderBookTest, self).on_recv_rsp(rsp_pb)
        # 打印
        OrderBookTest.logger.info('OrderBookHandlerBase ')
        OrderBookTest.logger.info(ret_code)
        OrderBookTest.logger.info(ret_data)
        return RET_OK, ret_data


class RTDataTest(RTDataHandlerBase):
    '''分时推送'''
    logger = Log().get_logger('RTDataTest')
    def on_recv_rsp(self, rsp_pb):
        ret_code, ret_data = super(RTDataTest, self).on_recv_rsp(rsp_pb)
        # 打印信息
        RTDataTest.logger.info('RTDataHandlerBase ')
        RTDataTest.logger.info(ret_code)
        RTDataTest.logger.info(ret_data)
        return RET_OK, ret_data


class TickerTest(TickerHandlerBase):
    '''获取逐笔 get_rt_ticker 和 TickerHandlerBase'''
    logger = Log().get_logger('TickerTest')
    def on_recv_rsp(self, rsp_pb):
        ret_code, ret_data = super(TickerTest, self).on_recv_rsp(rsp_pb)
        # 打印
        TickerTest.logger.info('TickerHandlerBase ')
        TickerTest.logger.info(ret_code)
        TickerTest.logger.info(ret_data)
        return RET_OK, ret_data


class StockQuoteTest(StockQuoteHandlerBase):
    # 获取报价get_stock_quote和StockQuoteHandlerBase
    logger = Log().get_logger('StockQuoteTest')
    def on_recv_rsp(self, rsp_str):
        ret_code, ret_data = super(StockQuoteTest, self).on_recv_rsp(
            rsp_str)  # 基类的on_recv_rsp方法解包返回了报价信息，格式与get_stock_quote一样
        # 打印
        StockQuoteTest.logger.info('StockQuoteTest ')
        StockQuoteTest.logger.info(ret_code)
        StockQuoteTest.logger.info(ret_data)
        return RET_OK, ret_data


class BrokerTest(BrokerHandlerBase):
    '''经济队列推送'''
    logger = Log().get_logger('BrokerTest')
    def on_recv_rsp(self, rsp_pb):
        ret_code, stock_code, ret_data = super(BrokerTest, self).on_recv_rsp(rsp_pb)
        # 打印
        BrokerTest.logger.info('BrokerHandlerBase ')
        BrokerTest.logger.info(ret_code)
        BrokerTest.logger.info(stock_code)
        BrokerTest.logger.info(ret_data)

        return RET_OK, ret_data


class TradeOrderTest(TradeOrderHandlerBase):
    '''订单状态推送'''
    logger = Log().get_logger('TradeOrderTest')
    def on_recv_rsp(self, rsp_pb):
        ret_code,ret_data = super(TradeOrderTest, self).on_recv_rsp(rsp_pb)
        TradeOrderTest.logger.info('TradeOrderHandlerBase')
        TradeOrderTest.logger.info(ret_code)
        TradeOrderTest.logger.info(ret_data)

        return RET_OK,ret_data


class TradeDealTest(TradeDealHandlerBase):
    '''订单成交推送 '''
    logger = Log().get_logger('TradeDealTest')
    def on_recv_rsp(self, rsp_pb):
        ret_code,ret_data = super(TradeDealTest, self).on_recv_rsp(rsp_pb)
        TradeDealTest.logger.info('TradeDealHandlerBase')
        TradeDealTest. logger.info(ret_code)
        TradeDealTest.logger.info(ret_data)
        return RET_OK,ret_data

class OrderDetailTest(OrderDetailHandlerBase):
    def on_recv_rsp(self, rsp_str):
        ret_code, err_or_stock_code, data = super(OrderDetailTest, self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("OrderDetailTest: error, msg: {}".format(err_or_stock_code))
            return RET_ERROR, data

        print("OrderDetailTest: stock: {} data: {} ".format(err_or_stock_code, data))  # OrderDetailTest

        return RET_OK, data

if __name__ == '__main__':
    # trade_ctx_us = OpenUSTradeContext('127.0.0.1',11112)
    # print(trade_ctx_us.place_order(35.4,1,'US.CTRP',TrdSide.BUY,OrderType.NORMAL))
    aa = BeforePublishTest()
    quote_ctx = OpenQuoteContext('127.0.0.1',11111)
    handlers = [CurKlineTest(), OrderBookTest(), RTDataTest(), TickerTest(), StockQuoteTest(), BrokerTest()]
    for handler in handlers:
        quote_ctx.set_handler(handler)
    ret_code, ret_data = quote_ctx.get_stock_basicinfo(Market.HK, SecurityType.STOCK)
    code_list = list(ret_data['code'])[100:600]
    print(len(code_list))
    print(quote_ctx.query_subscription(code_list))
    quote_ctx.set_handler(CurKlineTest())
    print(quote_ctx.subscribe(code_list, [SubType.TICKER, SubType.K_1M]))# , SubType.RT_DATA, SubType.TICKER, SubType.QUOTE
    print(quote_ctx.query_subscription(code_list))
    # quote_ctx.close()

    # aa.test_quotation()
    # aa.test_trade(TrdEnv.REAL)
    # time.sleep(30)
    # aa.test_trade(TrdEnv.SIMULATE)
    # order_id_hk=3609064270230150378
    # trade_hk = OpenHKTradeContext('127.0.0.1', 11111)
    # print('111')
    # print(trade_hk.modify_order(modify_order_op=ModifyOrderOp.CANCEL, order_id=order_id_hk, qty=0, price=0, adjust_limit=0,
    #                                   trd_env=TrdEnv.SIMULATE, acc_id=0))


