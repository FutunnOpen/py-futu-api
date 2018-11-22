#-*-coding:utf-8-*-

import futu
from futu.quote.quote_response_handler import *
from futu.common.constant import *
from evatest.utils.logUtil import Logs
import time


# port=11118 285706压测
class QoutationAsynPush(object):
    '''
    gateway负载测试：订阅3大市场各类股票的13种实时行情数据，求最大可订阅股票个数
    '''
    timestamp = (int)(time.time())
    dir = 'QoutationAsynPush_'+str(timestamp)

    def __init__(self):
        # 加密通道
        # SysConfig.enable_proto_encrypt(True)
        # SysConfig.enable_proto_encrypt(True)

        self.quote_ctx = futu.OpenQuoteContext(host='127.0.0.1',port=11118)
        self.quote_ctx.start()


    def allStockQoutation(self):
        '''
        订阅多只股票的行情数据
        :return:
        '''
        logger = Logs().getNewLogger('allStockQoutation', QoutationAsynPush.dir)
        markets= [Market.HK,Market.SH,Market.SZ] #Market.US,
        stockTypes = [SecurityType.STOCK,SecurityType.WARRANT,SecurityType.IDX,SecurityType.BOND,SecurityType.ETF]

        for stockType in stockTypes:
            for market in markets:
                ret_code_stock_basicinfo ,ret_data_stock_basicinfo = self.quote_ctx.get_stock_basicinfo(market,stockType)
                codes = ret_data_stock_basicinfo['code'].tolist()
                codes_len = len(codes)
                code_sub = 0
                code_sub_succ = 0
                for code in codes:
                    ret_code = self.aStockQoutation(code,logger)
                    code_sub += 1
                    if ret_code is RET_OK:
                        code_sub_succ += 1
                    logger.info('市场 = %s，股票类型 = %s, 股票总数 = %d, 已发起订阅 = %d，订阅成功 = %d' % (market, stockType, codes_len, code_sub,code_sub_succ))  # 记录
                logger.info('end-------->市场 = %s，股票类型 = %s, 股票总数 = %d, 已发起订阅 = %d，订阅成功 = %d' % ( market, stockType, codes_len, code_sub,code_sub_succ))  # 记录

        time.sleep(5)
        self.quote_ctx.stop()
        self.quote_ctx.close()


    def aStockQoutation(self,code,logger):
        '''
        订阅一只股票的实时行情数据，接收推送
        :param code: 股票代码
        :return:
        '''

        #实时数据：设置监听-->订阅-->调用接口-------------------------------------
        # 分时
        self.quote_ctx.set_handler(RTDataTest())
        self.quote_ctx.subscribe(code, SubType.RT_DATA)



        ret_code_rt_data, ret_data_rt_data = self.quote_ctx.get_rt_data(code)
        logger.info(code+' ret_code_rt_data = '+str(ret_code_rt_data))
        if ret_code_rt_data is RET_ERROR:
            logger.info('ret_data_rt_data = '+ret_data_rt_data)
        # 逐笔
        self.quote_ctx.set_handler(TickerTest())
        self.quote_ctx.subscribe(code, SubType.TICKER)
        ret_code_rt_ticker, ret_data_rt_ticker = self.quote_ctx.get_rt_ticker(code)
        logger.info(code + ' ret_code_rt_ticker = ' + str(ret_code_rt_ticker))
        if ret_code_rt_ticker is RET_ERROR:
            logger.info('ret_data_rt_ticker = '+ret_data_rt_ticker)
        # 报价
        self.quote_ctx.set_handler(StockQuoteTest())
        self.quote_ctx.subscribe(code, SubType.QUOTE)
        ret_code_stock_quote, ret_data_stock_quote = self.quote_ctx.get_stock_quote([code])
        logger.info(code + ' ret_code_stock_quote = ' + str(ret_code_stock_quote))
        if ret_code_stock_quote is RET_ERROR:
            logger.info('ret_data_stock_quote = '+ret_data_stock_quote)
        # 实时K线
        self.quote_ctx.set_handler(CurKlineTest())
        kTypes = [SubType.K_1M, SubType.K_5M, SubType.K_15M, SubType.K_30M, SubType.K_60M, SubType.K_DAY,SubType.K_WEEK, SubType.K_MON]
        auTypes = [AuType.NONE, AuType.QFQ, AuType.HFQ]
        num = 10
        ret_code_cur_kline = RET_OK
        for kType in kTypes:
            self.quote_ctx.subscribe(code, kType)
            for auType in auTypes:
                ret_code_cur_kline_temp, ret_data_cur_kline_temp = self.quote_ctx.get_cur_kline(code, num, kType, auType)
                if ret_code_cur_kline_temp is RET_ERROR:
                    ret_code_cur_kline = RET_ERROR
                    logger.info('ret_code = ' + str(ret_code_cur_kline_temp)+ ' ret_data = '+ret_data_cur_kline_temp+' kType = '+kType+' auType = '+auType)
        logger.info(code + ' ret_code_cur_kline = ' + str(ret_code_cur_kline))
        # 摆盘
        self.quote_ctx.set_handler(OrderBookTest())
        self.quote_ctx.subscribe(code, SubType.ORDER_BOOK)
        ret_code_order_book, ret_data_order_book = self.quote_ctx.get_order_book(code)
        logger.info(code + ' ret_code_order_book = ' + str(ret_code_order_book))
        if ret_code_order_book is RET_ERROR:
            logger.info('ret_data_order_book = '+ret_data_order_book)
        # 经纪队列
        self.quote_ctx.set_handler(BrokerTest())
        self.quote_ctx.subscribe(code, SubType.BROKER)
        ret_code_broker_queue, bid_frame_table, ask_frame_table = self.quote_ctx.get_broker_queue(code)
        logger.info(code + ' ret_code_broker_queue = ' + str(ret_code_broker_queue))
        if ret_code_broker_queue is RET_ERROR:
            logger.info('bid_frame_table = '+bid_frame_table +' ask_frame_table = '+ask_frame_table)
        #历史数据----------------------------------------------------------------
        '''
        #获取复权因子
        ret_code_autype_list ,ret_data_autype_list = self.quote_ctx.get_autype_list([code])
        logger.info(code + ' ret_code_autype_list = ' + str(ret_code_autype_list))
        if ret_code_autype_list is RET_ERROR:
            logger.info('ret_data_autype_list = '+ret_data_autype_list)
        #获取历史K线
        start = '2017-1-1'
        end = '2018-6-1'
        fields = KL_FIELD.ALL_REAL
        ret_code_history_kline = RET_OK
        for kType in kTypes:
            for auType in auTypes:
                ret_code_history_kline_temp , ret_data_history_kline_temp = self.quote_ctx.get_history_kline(code,start,end,kType,auType,fields)
                if ret_code_history_kline_temp is RET_ERROR:
                    ret_code_history_kline = RET_ERROR
                    logger.info('ret_code = ' + str(ret_code_history_kline_temp) + ' ret_data = ' + ret_data_history_kline_temp + ' kType = ' + kType + ' auType = ' + auType)
        logger.info(code + ' ret_code_history_kline = ' + str(ret_code_history_kline))
        #获取多支股票多个单点历史K线
        dates = ['2018-1-1','2018-1-2','2018-3-16 9:30:00','2018-4-30 16:00:00','2018-5-27 13:30:59']
        no_data_modes = [KLNoDataMode.FORWARD, KLNoDataMode.BACKWARD, KLNoDataMode.NONE]
        ret_code_multi_points_history_kline = RET_OK
        for kType in kTypes:
            for auType in auTypes:
                for no_data_mode in no_data_modes:
                    ret_code_MPHK_temp, ret_data_MPHK_temp = self.quote_ctx.get_multi_points_history_kline([code],dates,fields,kType,auType,no_data_mode)
                    if ret_code_MPHK_temp is RET_ERROR:
                        ret_code_multi_points_history_kline = RET_ERROR
                        logger.info('ret_code = ' + str(ret_code_multi_points_history_kline) + ' ret_data = ' + ret_data_MPHK_temp + ' kType = ' + kType + ' auType = ' + auType+' no_data_mode = '+no_data_mode)
        logger.info(code + ' ret_code_multi_points_history_kline = ' + str(ret_code_multi_points_history_kline))
        
        return ret_code_rt_data+ret_code_rt_ticker+ret_code_stock_quote+ret_code_cur_kline+ret_code_order_book+ret_code_broker_queue+ret_code_autype_list+ret_code_history_kline+ret_code_multi_points_history_kline
        '''
        return ret_code_rt_data + ret_code_rt_ticker + ret_code_stock_quote + ret_code_cur_kline + ret_code_order_book + ret_code_broker_queue

class BrokerTest(BrokerHandlerBase):
    logger = Logs().getNewLogger('BrokerTest', QoutationAsynPush.dir)
    def on_recv_rsp(self, rsp_pb):
        ret_code,stock_code,ret_data = super(BrokerTest, self).on_recv_rsp(rsp_pb)
        #打印日志
        BrokerTest.logger.info('BrokerTest')
        BrokerTest.logger.info(stock_code)
        BrokerTest.logger.info(ret_code)
        BrokerTest.logger.info(ret_data)

        return RET_OK,ret_data

class CurKlineTest(CurKlineHandlerBase):
    '''获取实时K线 get_cur_kline 和 CurKlineHandlerBase'''
    logger = Logs().getNewLogger('CurKlineTest', QoutationAsynPush.dir)
    def on_recv_rsp(self, rsp_pb):
        ret_code, ret_data = super(CurKlineTest, self).on_recv_rsp(rsp_pb)
        # 打印,记录日志
        CurKlineTest.logger.info('CurKlineTest')
        CurKlineTest.logger.info(ret_code)
        CurKlineTest.logger.info(ret_data)
        return RET_OK, ret_data

class OrderBookTest(OrderBookHandlerBase):
    logger = Logs().getNewLogger('OrderBookTest', QoutationAsynPush.dir)

    def on_recv_rsp(self, rsp_pb):
        ret_code ,ret_data = super(OrderBookTest, self).on_recv_rsp(rsp_pb)
        #打印
        OrderBookTest.logger.info('OrderBookTest')
        OrderBookTest.logger.info(ret_code)
        OrderBookTest.logger.info(ret_data)
        return RET_OK, ret_data

class RTDataTest(RTDataHandlerBase):
    logger = Logs().getNewLogger('RTDataTest', QoutationAsynPush.dir)
    def on_recv_rsp(self, rsp_pb):
        ret_code,ret_data = super(RTDataTest, self).on_recv_rsp(rsp_pb)
        #打印信息
        RTDataTest.logger.info('RTDataTest')
        RTDataTest.logger.info(ret_code)
        RTDataTest.logger.info(ret_data)

        return RET_OK,ret_data

class TickerTest(TickerHandlerBase):
    '''获取逐笔 get_rt_ticker 和 TickerHandlerBase'''
    logger = Logs().getNewLogger('TickerTest', QoutationAsynPush.dir)
    def on_recv_rsp(self, rsp_pb):
        ret_code, ret_data = super(TickerTest, self).on_recv_rsp(rsp_pb)
        # 打印,记录日志
        TickerTest.logger.info('TickerTest')
        TickerTest.logger.info(ret_code)
        TickerTest.logger.info(ret_data)
        return RET_OK, ret_data

class StockQuoteTest(StockQuoteHandlerBase):
    # 获取报价get_stock_quote和StockQuoteHandlerBase
    logger = Logs().getNewLogger('StockQuoteTest', QoutationAsynPush.dir)
    def on_recv_rsp(self, rsp_str):
        ret_code, ret_data = super(StockQuoteTest,self).on_recv_rsp(rsp_str) # 基类的on_recv_rsp方法解包返回了报价信息，格式与get_stock_quote一样
        #打印,记录日志
        StockQuoteTest.logger.info('StockQuoteTest')
        StockQuoteTest.logger.info(ret_code)
        StockQuoteTest.logger.info(ret_data)
        return RET_OK, ret_data



if __name__ =='__main__':
    q = QoutationAsynPush()
    q.allStockQoutation()

