#-*-coding:utf-8-*-

import futuquant
from futuquant.common.constant import *
from evatest.utils.logUtil import Logs
import time

class MaxCodesLen(object):
    '''
    计算入参code_list的最大值
    '''

    def __init__(self):
        self.quote_ctx = futuquant.OpenQuoteContext('127.0.0.1',11111)
        self.quote_ctx.start()
        timestamp = (int)(time.time())
        self.logger = Logs().getNewLogger(str(timestamp),'MaxCodesLen')
        self.code_list = self.get_market_all()

    def close(self):
        self.quote_ctx.stop()
        self.quote_ctx.close()

    def test_get_autype_list(self):
        api_name = 'get_autype_list'

        index_left = 0
        index_right = len(self.code_list) - 1
        index_mid = len(self.code_list) - 1
        while (index_mid >= 0 and index_mid < len(self.code_list)):
            # 调用接口
            ret_code, ret_data = self.quote_ctx.ret_code, ret_data = self.quote_ctx.get_autype_list(self.code_list[0:index_mid])
            self.logger.info(api_name + ' ret_code = ' + str(ret_code) + ' len(code_list)= ' + str(index_mid))
            if ret_code == RET_OK:
                if index_mid < len(self.code_list) - 1 and index_left < index_right:
                    index_left = index_mid + 1
                else:
                    self.logger.info(api_name + ' 可请求成功的code_list最大长度 = ' + str(index_mid))
                    break
            else:
                index_right = index_mid - 1
            index_mid = (index_left + index_right) // 2

    def test_get_multi_points_history_kline(self):
        api_name = 'get_multi_points_history_kline'

        index_left = 0
        index_right = len(self.code_list) - 1
        index_mid = len(self.code_list) - 1
        while (index_mid >= 0 and index_mid < len(self.code_list)):
            # 调用接口
            ret_code, ret_data = self.quote_ctx.ret_code, ret_data = self.quote_ctx.get_multi_points_history_kline(self.code_list[0:index_mid],
                                                                                                                   dates = ['2018-5-28'],
                                                                                                                   fields = KL_FIELD.ALL_REAL,
                                                                                                                   ktype = KLType.K_DAY,
                                                                                                                   autype = AuType.QFQ,
                                                                                                                   no_data_mode = KLNoDataMode.FORWARD)
            self.logger.info(api_name+' ret_code = ' + str(ret_code) + ' len(code_list)= ' + str(index_mid))
            if ret_code == RET_OK:
                if index_mid < len(self.code_list)-1 and index_left < index_right:
                    index_left = index_mid + 1
                else:
                    self.logger.info(api_name+' 可请求成功的code_list最大长度 = ' + str(index_mid))
                    break
            else:
                index_right = index_mid - 1
            index_mid = (index_left + index_right) // 2

    def test_subscribe(self):
        api_name = 'subscribe'

        index_left = 0
        index_right = len(self.code_list) - 1
        index_mid = len(self.code_list) - 1
        while (index_mid > 0 and index_mid < len(self.code_list)):
            # 调用接口
            ret_code, ret_data = self.quote_ctx.ret_code, ret_data = self.quote_ctx.subscribe(self.code_list[0:index_mid], subtype_list = [SubType.RT_DATA])
            self.logger.info(api_name+' ret_code = ' + str(ret_code) + ' len(code_list)= ' + str(index_mid))
            if ret_code == RET_OK:
                if index_mid < len(self.code_list)-1 and index_left < index_right:
                    index_left = index_mid + 1
                else:
                    self.logger.info(api_name+' 可请求成功的code_list最大长度 = ' + str(index_mid))
                    break
            else:
                index_right = index_mid - 1
            index_mid = (index_left + index_right) // 2

    def test_get_market_snapshot(self):
        api_name = 'get_market_snapshot'

        index_left = 0
        index_right = len(self.code_list) - 1
        index_mid = len(self.code_list) - 1
        req_times = 0
        while (index_mid >= 0 and index_mid < len(self.code_list)):
            # 调用接口
            ret_code, ret_data = self.quote_ctx.ret_code, ret_data = self.quote_ctx.get_market_snapshot(self.code_list[0:index_mid])
            req_times += 1  #
            self.logger.info(api_name+' ret_code = ' + str(ret_code) + ' len(code_list)= ' + str(index_mid))
            if ret_code == RET_OK:
                if index_mid < len(self.code_list)-1 and index_left < index_right:
                    index_left = index_mid + 1
                else:
                    self.logger.info(api_name+' 可请求成功的code_list最大长度 = ' + str(index_mid))
                    break
            else:
                index_right = index_mid - 1
            index_mid = (index_left + index_right) // 2

            if req_times >= 10:
                time.sleep(30)      #每30秒最多请求10次

    def test_get_stock_quote(self):
        api_name = 'get_stock_quote'

        index_left = 0
        index_right = len(self.code_list) - 1
        index_mid = len(self.code_list) - 1
        req_times = 0
        while (index_mid >= 0 and index_mid < len(self.code_list)):
            # 调用接口
            ret_code, ret_data = self.quote_ctx.ret_code, ret_data = self.quote_ctx.get_stock_quote(self.code_list[0:index_mid])
            req_times += 1  #
            self.logger.info(api_name+' ret_code = ' + str(ret_code) + ' len(code_list)= ' + str(index_mid))
            if ret_code == RET_OK:
                if index_mid < len(self.code_list)-1 and index_left < index_right:
                    index_left = index_mid + 1
                else:
                    self.logger.info(api_name+' 可请求成功的code_list最大长度 = ' + str(index_mid))
                    break
            else:
                index_right = index_mid - 1
            index_mid = (index_left + index_right) // 2

            if req_times >= 10:
                time.sleep(30)      #每30秒最多请求10次

    def get_market_all(self):
        '''获取3大市场下的所有股票'''
        markets = [Market.HK, Market.SZ, Market.SH, Market.US]
        stockTypes = [SecurityType.STOCK, SecurityType.WARRANT, SecurityType.IDX, SecurityType.BOND, SecurityType.ETF]
        codes = []
        for market in markets:
            for stock_type in stockTypes:
                ret_code, ret_data = self.quote_ctx.get_stock_basicinfo(market=market, stock_type=stock_type)
                codes += ret_data['code'].tolist()
                # print('market = %s, stock_type = %s, len(codes) = %d'%(market, stock_type, len(ret_data['code'].tolist())))
        self.logger.info('3大市场所有股票总数 = '+ str(len(codes)))
        return codes


if __name__ == '__main__':
        mcl = MaxCodesLen()
        mcl.test_subscribe()




