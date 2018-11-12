#-*-coding:utf-8-*-

import futuquant
from futuquant.common.constant import *
import time

class MaxCodesLen(object):
    '''
    计算入参code_list的最大值
    '''

    def __init__(self):
        self.quote_ctx = futuquant.OpenQuoteContext('127.0.0.1',11111)
        self.quote_ctx.start()

    def test_subscribe(self,code_list):
        api_name = 'subscribe'

        index_left = 0
        index_right = len(code_list) - 1
        index_mid = len(code_list) - 1
        while (index_mid > 0 and index_mid < len(code_list)):
            # 调用接口
            ret_code, ret_data = self.quote_ctx.ret_code, ret_data = self.quote_ctx.subscribe(code_list[0:index_mid], subtype_list = [SubType.RT_DATA])
            print(api_name+' ret_code = ' + str(ret_code) + ' len(code_list)= ' + str(index_mid))
            if ret_code == RET_OK:
                if index_mid < len(code_list)-1 and index_left < index_right:
                    index_left = index_mid + 1
                else:
                    print(api_name+' 可请求成功的code_list最大长度 = ' + str(index_mid))
                    break
            else:
                index_right = index_mid - 1
            index_mid = (index_left + index_right) // 2

    def get_market_all(self):
        '''获取3大市场下的所有股票'''
        markets = [Market.HK, Market.SZ, Market.SH, Market.US]
        stockTypes = [SecurityType.STOCK, SecurityType.WARRANT, SecurityType.IDX, SecurityType.BOND, SecurityType.ETF]
        codes = []
        for market in markets:
            for stock_type in stockTypes:
                ret_code, ret_data = self.quote_ctx.get_stock_basicinfo(market=market, stock_type=stock_type)
                codes += ret_data['code'].tolist()
                print('market = %s, stock_type = %s, len(codes) = %d'%(market, stock_type, len(ret_data['code'].tolist())))
        # self.logger.info('3大市场所有股票总数 = '+ str(len(codes)))

        return codes



if __name__ == '__main__':
    l1 = [1,2,3,4,5]
    l2 = [4,5,1,1,2,3,3,4,2,5]
    s1 = set(l1 )
    s2 = set(l2)
    print(s1)
    print(s2)




