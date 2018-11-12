#-*-coding:utf-8-*-
import pandas

from futuquant.testcase.person.eva.trade.Handler import *
from futuquant.trade.open_trade_context import *
from futuquant import *
import datetime
import logging


class TradeUS(object):
    # 下单接口，查询持仓
    #背景：用户反馈ubuntu和mac同时挂机，ubuntu下单后查询持仓不是最新数据，mac查询到最新持仓。

    def __init__(self):
        pandas.set_option('max_columns', 100)
        pandas.set_option('display.width', 1000)

    def test_plateOrder_noPush(self):
        quote_host = '127.0.0.1'
        quote_port = 11111
        quote_ctx = OpenQuoteContext(quote_host ,quote_port)
        trade_us = OpenUSTradeContext('127.0.0.1',11114)
        #日志
        logger = self.getNewLogger('plate_order_time_out_100063')
        #解锁交易
        logger.info('unlock '+str(trade_us.unlock_trade('123123')))
        #订阅订单状态推送
        handler_order = TradeOrderTest()
        handler_order.set_logger(logger)
        trade_us.set_handler(handler_order)
        #订阅订单成交推送
        handler_deal = TradeDealTest()
        handler_deal.set_logger(logger)
        trade_us.set_handler(handler_deal)
        # 获取美股股票列表
        ret_code_quote, ret_data = quote_ctx.get_stock_basicinfo(market=Market.US, stock_type=SecurityType.STOCK,code_list=[])
        codes = ret_data['code'].tolist()
        #逐只股票获取报价并下单
        for index in range(len(codes)):
            code = codes[index]
            print(index, code)
            ret_code_sub, ret_data_sub = quote_ctx.subscribe(code, [SubType.QUOTE, SubType.ORDER_BOOK])
            logger.info('subscribe '+str((ret_code_sub, ret_data_sub)) )
            ret_code_quote,ret_data_quote = quote_ctx.get_stock_quote([code])
            ret_code_orderBook , ret_data_orderBook = quote_ctx.get_order_book(code)
            if ret_code_quote == RET_ERROR:
                logger.info('get_stock_quote '+str((ret_code_quote,ret_data_quote)) )
                continue
            if  ret_code_orderBook == RET_ERROR :
                logger.info('get_order_book ' + str(ret_code_orderBook,ret_data_orderBook) )
                continue
            #获取股票现价和价差
            price_quote = ret_data_quote['last_price'].tolist()[0]
            price_spread = ret_data_quote['price_spread'].tolist()[0]
            price_spread_num = 20
            price_bid = ret_data_orderBook.get('Bid')[0][0]
            price = min(price_quote, price_bid)   #下单价格
            if price <= 0:  #下单价格不能小于等于0
                continue
            #下单
            acc_index = 0
            price_tmp = price - (price_spread * price_spread_num) #下买入单，低于当前价20个档位
            if price_tmp >0:
                price = price_tmp
            '''  '''
            logger.info('place_order 买入 code= ' +code+' price= '+str(price))
            ret_code_buy ,ret_data_buy = trade_us.place_order(price=price, qty=1, code=code, trd_side=TrdSide.BUY, order_type=OrderType.NORMAL,adjust_limit=0, trd_env=TrdEnv.REAL, acc_id=0, acc_index=acc_index)
            logger.info('place_order 【买入】 ' + str((ret_code_buy ,ret_data_buy)) )
            if ret_code_buy == RET_ERROR:
                dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S%f')
                print('%s 买入 code= %s price = %f' %(dt, code, price))
                print('place_order ',(ret_code_buy ,ret_data_buy))
            time.sleep(10)
            ret_code_position, ret_data_position = trade_us.position_list_query(code='', pl_ratio_min=None,pl_ratio_max=None, trd_env=TrdEnv.REAL,acc_id=0,acc_index=acc_index)
            logger.info('position_list_query ret_code = '+str(ret_code_position)+' len(ret_data) = '+str(len(ret_data_position)))

            price = price + (price_spread * price_spread_num)#下卖出单，高于当前价20个档位
            logger.info('place_order 卖出 code= ' + code + ' price= ' + str(price))
            ret_code_sell, ret_data_sell = trade_us.place_order(price=price, qty=1, code=code, trd_side=TrdSide.SELL, order_type=OrderType.NORMAL,adjust_limit=0, trd_env=TrdEnv.REAL, acc_id=0, acc_index=acc_index)
            logger.info('place_order 【卖出】 ' + str((ret_code_sell, ret_data_sell)) )
            if ret_code_sell == RET_ERROR:
                dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S%f')
                print('%s 卖出 code= %s price = %f' % (dt, code, price))
                print('place_order ', (ret_code_sell, ret_data_sell))
            time.sleep(10)
            # logger.info(trade_us.position_list_query(code='', pl_ratio_min=None, pl_ratio_max=None, trd_env=TrdEnv.REAL,acc_id=0,acc_index=acc_index))
            ret_code_position, ret_data_position = trade_us.position_list_query(code='', pl_ratio_min=None,pl_ratio_max=None, trd_env=TrdEnv.REAL,acc_id=0,acc_index=acc_index)
            logger.info('position_list_query ret_code = ' + str(ret_code_position) + ' len(ret_data) = ' + str(len(ret_data_position)))
            time.sleep(2*60)
            ret_code_unsub, ret_data_unsub = quote_ctx.unsubscribe(code, SubType.QUOTE)
            logger.info('unsubscribe '+str((ret_code_unsub, ret_data_unsub)))
            #重新获取一次行情上下文，防止因重登录断开
            quote_ctx.close()
            quote_ctx = OpenQuoteContext(quote_host ,quote_port)
            #重头开始下单
            if index == len(codes)-1:
                index = 0

    def test_plate_order_noPush_timing(self):
        start_time = datetime.datetime( 2018, 9, 17, 21, 1, 1)
        while( start_time > datetime.datetime.now() ):
            print(datetime.datetime.now())
            sleep(60)
        #美股开盘，触发下单
        self.test_plateOrder_noPush()

    def test_mac(self):
        host = '127.0.0.1'  # mac-patrick
        port = 11111

        trade_us = OpenUSTradeContext(host, port)
        trade_us.unlock_trade('123123')
        logger = self.getNewLogger('mac_11111(2)')
        for i in range(1000):
            logger.info('position_list_query')
            logger.info(trade_us.position_list_query(code='', pl_ratio_min=None, pl_ratio_max=None,trd_env=TrdEnv.REAL, acc_id=0,acc_index=1))
            time.sleep(30*60)

    def getNewLogger(self,name,dir= None):
        '''

        :param name: 日志实例名
        :param dir: 日志所在文件夹名
        :return:
        '''
        logger = logging.getLogger(name)
        dir_path = os.getcwd() + os.path.sep + 'log'
        if dir is None:
            dir = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        dir_path = dir_path+os.path.sep+dir
        if os.path.exists(dir_path) is False:
            os.makedirs(dir_path)
        log_abs_name = dir_path + os.path.sep + name + '.txt'
        print(log_abs_name+'\n')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler = logging.FileHandler(log_abs_name)
        handler.setFormatter(formatter)
        console = logging.StreamHandler(stream=sys.stdout)

        logger.addHandler(handler)  # 设置日志输出到文件
        # logger.addHandler(console)  # 设置日志输出到屏幕控制台
        logger.setLevel(logging.DEBUG)  # 设置打印的日志等级

        return logger


class TradeOrderTest(TradeOrderHandlerBase):
    '''订单状态推送'''
    __logger = None
    def set_logger(self, logger):
        TradeOrderTest.__logger = logger

    def on_recv_rsp(self, rsp_pb):
        ret_code,ret_data = super(TradeOrderTest, self).on_recv_rsp(rsp_pb)
        # print('TradeOrderTest  ret_code = %d, ret_data = \n%s'%(ret_code,str(ret_data)))
        TradeOrderTest.__logger.info('【订单状态推送】 '+str((ret_code,ret_data)) )
        return RET_OK,ret_data

class TradeDealTest(TradeDealHandlerBase):
    '''订单成交推送 '''

    __logger = None
    def set_logger(self, logger):
        TradeDealTest.__logger = logger

    def on_recv_rsp(self, rsp_pb):
        ret_code,ret_data = super(TradeDealTest, self).on_recv_rsp(rsp_pb)
        # print('TradeDealTest  ret_code = %d, ret_data = \n%s' % (ret_code,str(ret_data)))
        TradeDealTest.__logger.info('【订单成交推送】 ' +str((ret_code,ret_data)) )
        return RET_OK,ret_data


if __name__ == '__main__':
    trd_us = TradeUS()
    trd_us.test_plate_order_noPush_timing()

