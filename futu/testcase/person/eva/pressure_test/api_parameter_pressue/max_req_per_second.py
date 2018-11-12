#-*-coding:utf-8-*-

import futuquant
from futuquant.common.constant import *
import time
from evatest.utils.logUtil import Logs

class MaxReqPerSec(object):
    '''计算各接口每秒最大请求次数'''

    def __init__(self):
        #日志
        timestamp = (int)(time.time())
        self.logger = Logs().getNewLogger(str(timestamp),'MaxReqPerSec')

    #行情接口
    def test_maxReqPerSec_get_stock_quote(self):
        quote_ctx = futuquant.OpenQuoteContext(host='127.0.0.1', port=11111)
        code_list = ['HK.00700']
        subtype_list = [SubType.QUOTE]
        quote_ctx.subscribe(code_list= code_list,subtype_list=subtype_list)

        req_times_succ = 0
        req_times_total = 0
        t_start = time.time()
        while time.time()<=(t_start+1):
            ret_code,ret_data = quote_ctx.get_stock_quote(['HK.00700'])
            req_times_total += 1
            if ret_code is RET_OK:
                req_times_succ += 1
            else:
                self.logger.info('get_stock_quote req_times_total = ' + str(req_times_total) + ' ret_code = ' + str(ret_code) +' ret_data = '+ret_data)
        quote_ctx.unsubscribe(code_list= code_list,subtype_list=subtype_list)
        quote_ctx.close()
        self.logger.info('get_stock_quote req_times_total = '+str(req_times_total)+' req_times_succ = '+str(req_times_succ))

    def test_maxReqPerSec_get_rt_ticker(self):
        quote_ctx = futuquant.OpenQuoteContext(host='127.0.0.1', port=11111)
        code = 'HK.00700'
        subtype =SubType.TICKER
        quote_ctx.subscribe(code_list=code,subtype_list=subtype)

        req_times_succ = 0
        req_times_total = 0
        t_start = time.time()
        while time.time()<=(t_start+1):
            ret_code,ret_data = quote_ctx.get_rt_ticker(code=code)
            req_times_total += 1
            if ret_code is RET_OK:
                req_times_succ += 1
            else:
                self.logger.info('get_rt_ticker req_times_total = ' + str(req_times_total) + ' ret_code = ' + str(ret_code) +' ret_data = '+ret_data)
        quote_ctx.unsubscribe(code_list=code,subtype_list=subtype)
        quote_ctx.close()
        self.logger.info('get_rt_ticker req_times_total = '+str(req_times_total)+' req_times_succ = '+str(req_times_succ))

    def test_maxReqPerSec_get_cur_kline(self):
        quote_ctx = futuquant.OpenQuoteContext(host='127.0.0.1', port=11111)
        code = 'HK.00700'
        ktype = SubType.K_DAY
        quote_ctx.subscribe(code_list=code ,subtype_list=ktype)

        req_times_succ = 0
        req_times_total = 0
        t_start = time.time()
        while time.time()<=(t_start+1):
            ret_code,ret_data = quote_ctx.get_cur_kline(code=code,ktype=ktype, num=10)
            req_times_total += 1
            if ret_code is RET_OK:
                req_times_succ += 1
            else:
                self.logger.info('get_cur_kline req_times_total = ' + str(req_times_total) + ' ret_code = ' + str(ret_code) + ' ret_data = ' + ret_data)
        quote_ctx.unsubscribe(code_list=code,subtype_list=ktype)
        quote_ctx.close()
        self.logger.info('get_cur_kline req_times_total = '+str(req_times_total)+' req_times_succ = '+str(req_times_succ))

    def test_maxReqPerSec_get_order_book(self):
        quote_ctx = futuquant.OpenQuoteContext(host='127.0.0.1', port=11111)
        code = 'HK.00700'
        ktype = SubType.ORDER_BOOK
        quote_ctx.subscribe(code_list=code ,subtype_list=ktype)

        req_times_succ = 0
        req_times_total = 0
        t_start = time.time()
        while time.time()<=(t_start+1):
            ret_code,ret_data = quote_ctx.get_order_book(code=code)
            req_times_total += 1
            if ret_code is RET_OK:
                req_times_succ += 1
            else:
                self.logger.info('get_order_book req_times_total = ' + str(req_times_total) + ' ret_code = ' + str(ret_code) + ' ret_data = ' + ret_data)
        quote_ctx.unsubscribe(code_list=code ,subtype_list=ktype)
        quote_ctx.close()
        self.logger.info('get_order_book req_times_total = '+str(req_times_total)+' req_times_succ = '+str(req_times_succ))

    def test_maxReqPerSec_get_rt_data(self):
        quote_ctx = futuquant.OpenQuoteContext(host='127.0.0.1', port=11111)
        code = 'HK.00700'
        ktype = SubType.RT_DATA
        quote_ctx.subscribe(code_list=code ,subtype_list=ktype)

        req_times_succ = 0
        req_times_total = 0
        t_start = time.time()
        while time.time()<=(t_start+1):
            ret_code,ret_data = quote_ctx.get_rt_data(code=code)
            req_times_total += 1
            if ret_code is RET_OK:
                req_times_succ += 1
            else:
                self.logger.info('get_rt_data req_times_total = ' + str(req_times_total) + ' ret_code = ' + str(ret_code) + ' ret_data = ' + ret_data)
        quote_ctx.unsubscribe(code_list=code ,subtype_list=ktype)
        quote_ctx.close()
        self.logger.info('get_rt_data req_times_total = '+str(req_times_total)+' req_times_succ = '+str(req_times_succ))

    def test_maxReqPerSec_get_broker_queue(self):
        quote_ctx = futuquant.OpenQuoteContext(host='127.0.0.1', port=11111)
        code = 'HK.00700'
        ktype = SubType.BROKER
        quote_ctx.subscribe(code_list=code ,subtype_list=ktype)

        req_times_succ = 0
        req_times_total = 0
        t_start = time.time()
        while time.time()<=(t_start+1):
            ret_code,bid_frame_table, ask_frame_table = quote_ctx.get_broker_queue(code=code)
            req_times_total += 1
            if ret_code is RET_OK:
                req_times_succ += 1
            else:
                self.logger.info('get_broker_queue req_times_total = ' + str(req_times_total) + ' ret_code = ' + str(ret_code) + ' ret_data = ' + bid_frame_table+ask_frame_table)
        quote_ctx.unsubscribe(code_list=code ,subtype_list=ktype)
        quote_ctx.close()
        self.logger.info('get_broker_queue req_times_total = '+str(req_times_total)+' req_times_succ = '+str(req_times_succ))

    def test_maxReqPerSec_subscribe(self):
        quote_ctx = futuquant.OpenQuoteContext(host='127.0.0.1', port=11111)

        req_times_succ = 0
        req_times_total = 0
        t_start = time.time()
        while time.time()<=(t_start+1):
            ret_code,ret_data = quote_ctx.subscribe(code_list = ['HK.00700'], subtype_list = [SubType.K_1M])
            req_times_total += 1
            if ret_code is RET_OK:
                req_times_succ += 1
            else:
                self.logger.info('subscribe req_times_total = ' + str(req_times_total) + ' ret_code = ' + str(ret_code) + ' ret_data = ' + ret_data)
        quote_ctx.close()
        self.logger.info('subscribe req_times_total = '+str(req_times_total)+' req_times_succ = '+str(req_times_succ))

    def test_maxReqPerSec_unsubscribe(self):
        quote_ctx = futuquant.OpenQuoteContext(host='127.0.0.1', port=11111)
        #获取测试股票
        stock_types = [SecurityType.STOCK, SecurityType.WARRANT, SecurityType.ETF, SecurityType.BOND, SecurityType.IDX]
        codes = []
        for stock_type in stock_types:
            ret_code, ret_data = quote_ctx.get_stock_basicinfo(market = Market.HK ,stock_type = stock_type)
            codes += ret_data['code'].tolist()
        #订阅，创造反订阅的条件
        subtype = SubType.K_1M
        quote_ctx.subscribe(code_list= codes, subtype_list= subtype)
        # time.sleep(61)

        req_times_succ = 0
        req_times_total = 0
        t_start = time.time()
        while time.time()<=(t_start+1):
            ret_code,ret_data = quote_ctx.unsubscribe(code_list = codes[req_times_total], subtype_list = subtype)
            req_times_total += 1
            if ret_code is RET_OK:
                req_times_succ += 1
            else:
                self.logger.info('unsubscribe req_times_total = ' + str(req_times_total) + ' ret_code = ' + str(ret_code) + ' ret_data = ' + ret_data)
        quote_ctx.close()
        self.logger.info('unsubscribe req_times_total = '+str(req_times_total)+' req_times_succ = '+str(req_times_succ))

    def test_maxReqPerSec_query_subscription(self):
        quote_ctx = futuquant.OpenQuoteContext(host='127.0.0.1', port=11111)

        req_times_succ = 0
        req_times_total = 0
        t_start = time.time()
        while time.time()<=(t_start+1):
            ret_code,ret_data = quote_ctx.query_subscription()
            req_times_total += 1
            if ret_code is RET_OK:
                req_times_succ += 1
            else:
                self.logger.info('query_subscription req_times_total = ' + str(req_times_total) + ' ret_code = ' + str(ret_code) + ' ret_data = ' + ret_data)
        quote_ctx.close()
        self.logger.info('query_subscription req_times_total = '+str(req_times_total)+' req_times_succ = '+str(req_times_succ))

    def test_maxReqPerSec_get_trading_days(self):
        quote_ctx = futuquant.OpenQuoteContext(host='127.0.0.1', port=11111)

        req_times_succ = 0
        req_times_total = 0
        t_start = time.time()
        while time.time()<=(t_start+1):
            ret_code,ret_data = quote_ctx.get_trading_days(market = Market.HK)
            req_times_total += 1
            if ret_code is RET_OK:
                req_times_succ += 1
            else:
                self.logger.info('get_trading_days req_times_total = ' + str(req_times_total) + ' ret_code = ' + str(ret_code) + ' ret_data = ' + ret_data)
        quote_ctx.close()
        self.logger.info('get_trading_days req_times_total = '+str(req_times_total)+' req_times_succ = '+str(req_times_succ))

    def test_maxReqPerSec_get_stock_basicinfo(self):
        quote_ctx = futuquant.OpenQuoteContext(host='127.0.0.1', port=11111)

        req_times_succ = 0
        req_times_total = 0
        t_start = time.time()
        while time.time()<=(t_start+1):
            ret_code,ret_data = quote_ctx.get_stock_basicinfo(market = Market.HK)
            req_times_total += 1
            if ret_code is RET_OK:
                req_times_succ += 1
            else:
                self.logger.info('get_stock_basicinfo req_times_total = ' + str(req_times_total) + ' ret_code = ' + str(ret_code) + ' ret_data = ' + ret_data)
        quote_ctx.close()
        self.logger.info('get_stock_basicinfo req_times_total = '+str(req_times_total)+' req_times_succ = '+str(req_times_succ))

    def test_maxReqPerSec_get_autype_list(self):
        quote_ctx = futuquant.OpenQuoteContext(host='127.0.0.1', port=11111)

        req_times_succ = 0
        req_times_total = 0
        t_start = time.time()
        while time.time()<=(t_start+1):
            ret_code,ret_data = quote_ctx.get_autype_list(code_list=['HK.00700'])
            req_times_total += 1
            if ret_code is RET_OK:
                req_times_succ += 1
            else:
                self.logger.info('get_autype_list req_times_total = ' + str(req_times_total) + ' ret_code = ' + str(ret_code) + ' ret_data = ' + ret_data)
        quote_ctx.close()
        self.logger.info('get_autype_list req_times_total = '+str(req_times_total)+' req_times_succ = '+str(req_times_succ))

    def test_maxReqPerSec_get_global_state(self):
        quote_ctx = futuquant.OpenQuoteContext(host='127.0.0.1', port=11111)

        req_times_succ = 0
        req_times_total = 0
        t_start = time.time()
        while time.time()<=(t_start+1):
            ret_code,ret_data = quote_ctx.get_global_state()
            req_times_total += 1
            if ret_code is RET_OK:
                req_times_succ += 1
            else:
                self.logger.info('get_global_state req_times_total = ' + str(req_times_total) + ' ret_code = ' + str(ret_code) + ' ret_data = ' + ret_data)

        quote_ctx.close()
        self.logger.info('get_global_state req_times_total = '+str(req_times_total)+' req_times_succ = '+str(req_times_succ))

    def test_maxReqPerSec_get_history_kline(self):
        quote_ctx = futuquant.OpenQuoteContext(host='127.0.0.1', port=11111)

        req_times_succ = 0
        req_times_total = 0
        t_start = time.time()
        while time.time()<=(t_start+1):
            ret_code,ret_data = quote_ctx.get_history_kline(code = 'HK.00700')
            req_times_total += 1
            if ret_code is RET_OK:
                req_times_succ += 1
            else:
                self.logger.info('get_history_kline req_times_total = ' + str(req_times_total) + ' ret_code = ' + str(ret_code) + ' ret_data = ' + ret_data)

        quote_ctx.close()
        self.logger.info('get_history_kline req_times_total = '+str(req_times_total)+' req_times_succ = '+str(req_times_succ))

    def test_maxReqPerSec_get_multi_points_history_kline(self):
        quote_ctx = futuquant.OpenQuoteContext(host='127.0.0.1', port=11111)

        req_times_succ = 0
        req_times_total = 0
        t_start = time.time()
        while time.time()<=(t_start+1):
            ret_code,ret_data = quote_ctx.get_multi_points_history_kline(code_list = ['HK.00700'],dates = ['2018-5-30 9:30:00','2018-5-29'],
                                       fields = KL_FIELD.ALL_REAL,)
            req_times_total += 1
            if ret_code is RET_OK:
                req_times_succ += 1
            else:
                self.logger.info('get_multi_points_history_kline req_times_total = ' + str(req_times_total) + ' ret_code = ' + str(ret_code) + ' ret_data = ' + ret_data)
        quote_ctx.close()
        self.logger.info('get_multi_points_history_kline req_times_total = '+str(req_times_total)+' req_times_succ = '+str(req_times_succ))

    #交易接口
    def test_maxReqPerSec_get_acc_list(self):
        trade_ctx = futuquant.OpenHKTradeContext(host='127.0.0.1', port=11111)
        trade_ctx.unlock_trade(password='123123')

        req_times_succ = 0
        req_times_total = 0
        t_start = time.time()
        while time.time()<=(t_start+1):
            ret_code,ret_data = trade_ctx.get_acc_list()
            req_times_total += 1
            if ret_code is RET_OK:
                req_times_succ += 1
            else:
                self.logger.info('get_acc_list req_times_total = ' + str(req_times_total) + ' ret_code = ' + str(ret_code) + ' ret_data = ' + ret_data)
        trade_ctx.close()
        self.logger.info('get_acc_list req_times_total = '+str(req_times_total)+' req_times_succ = '+str(req_times_succ))

    def test_maxReqPerSec_accinfo_query(self):
        trade_ctx = futuquant.OpenHKTradeContext(host='127.0.0.1', port=11111)
        trade_ctx.unlock_trade(password='123123')

        req_times_succ = 0
        req_times_total = 0
        t_start = time.time()
        while time.time()<=(t_start+1):
            ret_code,ret_data = trade_ctx.accinfo_query()
            req_times_total += 1
            if ret_code is RET_OK:
                req_times_succ += 1
            else:
                self.logger.info('accinfo_query req_times_total = ' + str(req_times_total) + ' ret_code = ' + str(ret_code) + ' ret_data = ' + ret_data)
        trade_ctx.close()
        self.logger.info('accinfo_query req_times_total = '+str(req_times_total)+' req_times_succ = '+str(req_times_succ))

    def test_maxReqPerSec_order_list_query(self):
        trade_ctx = futuquant.OpenHKTradeContext(host='127.0.0.1', port=11111)
        trade_ctx.unlock_trade(password='123123')

        req_times_succ = 0
        req_times_total = 0
        t_start = time.time()
        while time.time()<=(t_start+1):
            ret_code,ret_data = trade_ctx.order_list_query()
            req_times_total += 1
            if ret_code is RET_OK:
                req_times_succ += 1
            else:
                self.logger.info('order_list_query req_times_total = ' + str(req_times_total) + ' ret_code = ' + str(ret_code) + ' ret_data = ' + ret_data)
        trade_ctx.close()
        self.logger.info('order_list_query req_times_total = '+str(req_times_total)+' req_times_succ = '+str(req_times_succ))

    def test_maxReqPerSec_position_list_query(self):
        trade_ctx = futuquant.OpenHKTradeContext(host='127.0.0.1', port=11111)
        trade_ctx.unlock_trade(password='123123')

        req_times_succ = 0
        req_times_total = 0
        t_start = time.time()
        while time.time()<=(t_start+1):
            ret_code,ret_data = trade_ctx.position_list_query()
            req_times_total += 1
            if ret_code is RET_OK:
                req_times_succ += 1
            else:
                self.logger.info('position_list_query req_times_total = ' + str(req_times_total) + ' ret_code = ' + str(ret_code) + ' ret_data = ' + ret_data)
        trade_ctx.close()
        self.logger.info('position_list_query req_times_total = '+str(req_times_total)+' req_times_succ = '+str(req_times_succ))

    def test_maxReqPerSec_deal_list_query(self):
        trade_ctx = futuquant.OpenHKTradeContext(host='127.0.0.1', port=11111)
        trade_ctx.unlock_trade(password='123123')

        req_times_succ = 0
        req_times_total = 0
        t_start = time.time()
        while time.time()<=(t_start+1):
            ret_code,ret_data = trade_ctx.deal_list_query()
            req_times_total += 1
            if ret_code is RET_OK:
                req_times_succ += 1
            else:
                self.logger.info('deal_list_query req_times_total = ' + str(req_times_total) + ' ret_code = ' + str(ret_code) + ' ret_data = ' + ret_data)
        trade_ctx.close()
        self.logger.info('deal_list_query req_times_total = '+str(req_times_total)+' req_times_succ = '+str(req_times_succ))



if __name__ == '__main__':
    mrps = MaxReqPerSec()

    mrps.test_maxReqPerSec_get_stock_quote()
    mrps.test_maxReqPerSec_get_rt_ticker()
    mrps.test_maxReqPerSec_get_cur_kline()
    mrps.test_maxReqPerSec_get_order_book()
    mrps.test_maxReqPerSec_get_rt_data()
    mrps.test_maxReqPerSec_get_broker_queue()
    mrps.test_maxReqPerSec_subscribe()
    # time.sleep(1)
    # mrps.test_maxReqPerSec_unsubscribe()
    mrps.test_maxReqPerSec_query_subscription()
    mrps.test_maxReqPerSec_get_trading_days()
    mrps.test_maxReqPerSec_get_stock_basicinfo()
    mrps.test_maxReqPerSec_get_autype_list()
    mrps.test_maxReqPerSec_get_global_state()
    mrps.test_maxReqPerSec_get_history_kline()
    mrps.test_maxReqPerSec_get_multi_points_history_kline()

    mrps.test_maxReqPerSec_get_acc_list()
    mrps.test_maxReqPerSec_accinfo_query()
    mrps.test_maxReqPerSec_order_list_query()
    mrps.test_maxReqPerSec_position_list_query()
    mrps.test_maxReqPerSec_deal_list_query()
