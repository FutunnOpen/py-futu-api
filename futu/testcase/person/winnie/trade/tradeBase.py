#-*-coding:utf-8-*-

from futu import *
import unittest
import random


host_local='127.0.0.1'
port_quote = 11111
port_trade = 11111
trade_pwd = '321321'


class TradeHKBase(unittest.TestCase):
    '''港股交易测试基类'''

    @classmethod
    def setUpClass(cls):
        # 每次调用该类时触发一次
        global logger, trade_ctx, quote_ctx
        # 实例化日志对象
        # logger = Logs.geLogger(cls.__name__)
        # 实例化上下文对象
        trade_ctx = OpenHKTradeContext(host=host_local, port=port_trade)
        quote_ctx = OpenQuoteContext(host=host_local, port=port_quote)
        # 解锁交易
        trade_ctx.unlock_trade(trade_pwd)

    def setUp(self):
        # 每次调用def test()时触发一次
        self.trade_ctx = trade_ctx
        self.logger = logger
        self.quote_ctx = quote_ctx
        # self.quoteBase = QuotationBase()    #依赖行情测试基类的部分常用方法

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        trade_ctx.close()
        quote_ctx.close()


    def placeOrder(self, code, trd_side, order_type, deal ,trd_env=TrdEnv.SIMULATE, price = None,qty = None,adjust_limit = None,acc_id=0, acc_index=1):
        '''
        快速下单，必填code, trd_side, order_type并关注trd_env即可。
        :param code: 必填，股票代码
        :param trd_side: 必填，买卖方向
        :param order_type: 必填，订单类型
        :param deal：必填，bool,是否立刻成交,True-立刻成交
        :param trd_env: 环境，默认是模拟环境。
        :param price:  订单价格，默认偏离最高/最低价5个价位
        :param qty: 订单数量（股、张），默认1手/1张
        :param adjust_limit: 价格调整幅度，默认随机生成
        :param acc_id: 账号id
        :param acc_index: 账号index,默认第2个(融资融券账号)

        :return:
            ret_code_po：下单响应码
            ret_data_po：下单响应订单内容
            params：下单入参，字段
        '''
        if price == None or qty ==None or adjust_limit ==None:  #价格、数量、价格调整幅度为空时，需要程序实现数据填充
            ret_code_ms, ret_data_ms = self.quote_ctx.get_market_snapshot(code)
            if ret_code_ms == RET_OK:
                high_price_v = ret_data_ms['high_price'][0] #当天最高价
                low_price_v = ret_data_ms['low_price'][0]   #当天最低价
                lot_size_v = ret_data_ms['lot_size'][0]     #每手股数
                price_spread_v = ret_data_ms['price_spread'][0] #价差
                price_spread_num = 3
                if price == None:
                    if (trd_side == TrdSide.BUY and deal) or (trd_side == TrdSide.SELL and (not deal)):
                        price = high_price_v + price_spread_v*price_spread_num  #比最高价再+price_spread_num个价位，促成立刻买入成交;同理避免立刻卖出。
                    else:
                        price = low_price_v - price_spread_v*price_spread_num #比最低价-price_spread_num个价位，促成立刻卖出成交;同理避免立刻买入。
                if qty == None:
                    qty = lot_size_v
                if adjust_limit == None:
                    adjust_limit = random.random()
            else:
                return  ret_code_ms, ret_data_ms,None    #获取市场快照失败
        #入参
        param_dict = {}
        param_dict['price'] = price
        param_dict['qty'] = qty
        param_dict['code'] = code
        param_dict['trd_side'] = trd_side
        param_dict['order_type'] = order_type
        param_dict['adjust_limit'] = adjust_limit
        param_dict['trd_env'] = trd_env
        param_dict['acc_id'] = acc_id
        param_dict['acc_index'] = acc_index
        param_dict['place_order_time'] = time.time()    #调用place_order接口的时间戳,float
        #下单
        ret_code_po, ret_data_po = self.trade_ctx.place_order(round(price, 3), qty, code, trd_side, order_type,adjust_limit, trd_env, acc_id, acc_index)
        return ret_code_po,ret_data_po,param_dict

    def cancelAllOrderBuy(self, trd_env=TrdEnv.SIMULATE, acc_id=0, acc_index=1):
        '''
        撤单：所有“买入”等待成交或部分成交的订单
        :param trd_env:
        :param acc_id:
        :param acc_index:
        :return:
        '''
        ret_code, ret_data = self.trade_ctx.order_list_query(trd_env=trd_env,acc_id=acc_id, acc_index=acc_index)
        if len(ret_data) >0:
            for index in range(len(ret_data)):
                flag_isBuy = ret_data['trd_side'][index] == TrdSide.BUY
                flag_canCancel = (ret_data['order_status'][index] == OrderStatus.SUBMITTED) or (ret_data['order_status'][index] == OrderStatus.FILLED_PART)
                if flag_isBuy and flag_canCancel:
                    order_id_tmp = ret_data['order_id'][index]
                    #撤单
                    self.trade_ctx.modify_order(modify_order_op = ModifyOrderOp.CANCEL, order_id =order_id_tmp, qty = 0, price= 0,adjust_limit=0, trd_env=trd_env, acc_id=acc_id, acc_index=acc_index)

class TradeUSBase(unittest.TestCase):
    '''美股交易测试基类'''

    @classmethod
    def setUpClass(cls):
        #每次调用该类时触发一次
        global logger,trade_ctx,quote_ctx

        #实例化日志对象
        # logger = Logs.geLogger(cls.__name__)
        #实例化上下文对象
        trade_ctx = OpenUSTradeContext(host=host_local, port=port_trade)
        quote_ctx = OpenQuoteContext(host=host_local, port=port_quote)
        #解锁交易
        trade_ctx.unlock_trade(trade_pwd)

    def setUp(self):
        #每次调用def test()时触发一次
        self.trade_ctx = trade_ctx
        self.logger = logger
        self.quote_ctx = quote_ctx
        # self.quoteBase = QuotationBase()    #依赖行情测试基类的部分常用方法

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        quote_ctx.close()
        trade_ctx.close()

    def placeOrder(self, code, trd_side, order_type, deal ,trd_env=TrdEnv.SIMULATE, price = None,qty = None,adjust_limit = None,acc_id=0, acc_index=1):
        '''
        快速下单，必填code, trd_side, order_type并关注trd_env即可。
        :param code: 必填，股票代码
        :param trd_side: 必填，买卖方向
        :param order_type: 必填，订单类型
        :param deal：必填，bool,是否立刻成交,True-立刻成交
        :param trd_env: 环境，默认是模拟环境。
        :param price:  订单价格，默认偏离最高/最低价5个价位
        :param qty: 订单数量（股、张），默认1手/1张
        :param adjust_limit: 价格调整幅度，默认随机生成
        :param acc_id: 账号id
        :param acc_index: 账号index,默认第2个（融资融券账户）

        :return:
            ret_code_po：下单响应码
            ret_data_po：下单响应订单内容
            params：下单入参，字段
        '''
        if price == None or qty ==None or adjust_limit ==None:  #价格、数量、价格调整幅度为空时，需要程序实现数据填充
            ret_code_ms, ret_data_ms = self.quote_ctx.get_market_snapshot(code)
            if ret_code_ms == RET_OK:
                high_price_v = ret_data_ms['high_price'][0] #当天最高价
                low_price_v = ret_data_ms['low_price'][0]   #当天最低价
                lot_size_v = ret_data_ms['lot_size'][0]     #没手股数
                price_spread_v = ret_data_ms['price_spread'][0] #价差
                price_spread_num = 5
                if price == None:
                    if (trd_side == TrdSide.BUY and deal) or (trd_side == TrdSide.SELL and (not deal)):
                        price = high_price_v + price_spread_v * price_spread_num  # 比最高价再+price_spread_num个价位，促成立刻买入成交;同理避免立刻卖出。
                    else:
                        price = low_price_v - price_spread_v * price_spread_num  # 比最低价-price_spread_num个价位，促成立刻卖出成交;同理避免立刻买入。
                if qty == None:
                    qty = lot_size_v
                if adjust_limit == None:
                    adjust_limit = random.random()
            else:
                return  ret_code_ms, ret_data_ms,None    #获取市场快照失败
        #入参
        param_dict = {}
        param_dict['price'] = price
        param_dict['qty'] = qty
        param_dict['code'] = code
        param_dict['trd_side'] = trd_side
        param_dict['order_type'] = order_type
        param_dict['adjust_limit'] = adjust_limit
        param_dict['trd_env'] = trd_env
        param_dict['acc_id'] = acc_id
        param_dict['acc_index'] = acc_index
        param_dict['place_order_time'] = time.time()    #调用place_order接口的时间戳,float
        #下单
        ret_code_po, ret_data_po = self.trade_ctx.place_order(round(price, 3), qty, code, trd_side, order_type,adjust_limit, trd_env, acc_id, acc_index)
        return ret_code_po,ret_data_po,param_dict

    def cancelAllOrderBuy(self, trd_env=TrdEnv.SIMULATE, acc_id=0, acc_index=1):
        '''
        撤单：所有“买入”等待成交或部分成交的订单
        :param trd_env:
        :param acc_id:
        :param acc_index:
        :return:
        '''
        ret_code, ret_data = self.trade_ctx.order_list_query(trd_env=trd_env,acc_id=acc_id, acc_index=acc_index)
        if len(ret_data) >0:
            for index in range(len(ret_data)):
                flag_isBuy = ret_data['trd_side'][index] == TrdSide.BUY
                flag_canCancel = (ret_data['order_status'][index] == OrderStatus.SUBMITTED) or (ret_data['order_status'][index] == OrderStatus.FILLED_PART)
                if flag_isBuy and flag_canCancel:
                    order_id_tmp = ret_data['order_id'][index]
                    #撤单
                    self.trade_ctx.modify_order(modify_order_op = ModifyOrderOp.CANCEL, order_id =order_id_tmp, qty = 0, price= 0,adjust_limit=0, trd_env=trd_env, acc_id=acc_id, acc_index=acc_index)


class TradeHKCCBase(unittest.TestCase):
    '''A股通交易测试基类'''

    @classmethod
    def setUpClass(cls):
        #每次调用该类时触发一次
        global logger,trade_ctx,quote_ctx,trade_pwd
        #实例化日志对象
        # logger = Logs.geLogger(cls.__name__)
        #实例化上下文对象
        trade_ctx = OpenHKCCTradeContext(host=host_local, port=port_trade)
        quote_ctx = OpenQuoteContext(host=host_local, port=port_quote)
        #解锁交易
        trade_ctx.unlock_trade(trade_pwd)

    def setUp(self):
        #每次调用def test()时触发一次
        self.trade_ctx = trade_ctx
        self.logger = logger
        self.quote_ctx = quote_ctx
        # self.quoteBase = QuotationBase()    #依赖行情测试基类的部分常用方法

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        quote_ctx.close()
        trade_ctx.close()

    def placeOrder(self, code, trd_side, order_type, deal ,trd_env=TrdEnv.SIMULATE, price = None,qty = None,adjust_limit = None,acc_id=0, acc_index=0):
        '''
        快速下单，必填code, trd_side, order_type并关注trd_env即可。
        :param code: 必填，股票代码
        :param trd_side: 必填，买卖方向
        :param order_type: 必填，订单类型
        :param deal：必填，bool,是否立刻成交,True-立刻成交
        :param trd_env: 环境，默认是模拟环境。
        :param price:  订单价格，默认偏离最高/最低价5个价位
        :param qty: 订单数量（股、张），默认1手/1张
        :param adjust_limit: 价格调整幅度，默认随机生成
        :param acc_id: 账号id
        :param acc_index: 账号index,默认第1个

        :return:
            ret_code_po：下单响应码
            ret_data_po：下单响应订单内容
            params：下单入参，字段
        '''
        if price == None or qty ==None or adjust_limit ==None:  #价格、数量、价格调整幅度为空时，需要程序实现数据填充
            ret_code_ms, ret_data_ms = self.quote_ctx.get_market_snapshot(code)
            if ret_code_ms == RET_OK:
                high_price_v = ret_data_ms['high_price'][0] #当天最高价
                low_price_v = ret_data_ms['low_price'][0]   #当天最低价
                lot_size_v = ret_data_ms['lot_size'][0]     #没手股数
                price_spread_v = ret_data_ms['price_spread'][0] #价差
                price_spread_num = 5
                if price == None:
                    if (trd_side == TrdSide.BUY and deal) or (trd_side == TrdSide.SELL and (not deal)):
                        price = high_price_v + price_spread_v * price_spread_num  # 比最高价再+price_spread_num个价位，促成立刻买入成交;同理避免立刻卖出。
                    else:
                        price = low_price_v - price_spread_v * price_spread_num  # 比最低价-price_spread_num个价位，促成立刻卖出成交;同理避免立刻买入。
                if qty == None:
                    qty = lot_size_v  #evan说测试环境A股不能下100
                if adjust_limit == None:
                    adjust_limit = random.random()
            else:
                return  ret_code_ms, ret_data_ms,None    #获取市场快照失败
        #入参
        param_dict = {}
        param_dict['price'] = price
        param_dict['qty'] = qty
        param_dict['code'] = code
        param_dict['trd_side'] = trd_side
        param_dict['order_type'] = order_type
        param_dict['adjust_limit'] = adjust_limit
        param_dict['trd_env'] = trd_env
        param_dict['acc_id'] = acc_id
        param_dict['acc_index'] = acc_index
        param_dict['place_order_time'] = time.time()    #调用place_order接口的时间戳,float
        #下单
        ret_code_po, ret_data_po = self.trade_ctx.place_order(round(price, 2), qty, code, trd_side, order_type,adjust_limit, trd_env, acc_id, acc_index)
        return ret_code_po,ret_data_po,param_dict

    def cancelAllOrderBuy(self, trd_env=TrdEnv.SIMULATE, acc_id=0, acc_index=0):
        '''
        撤单：所有“买入”等待成交或部分成交的订单
        :param trd_env:
        :param acc_id:
        :param acc_index:
        :return:
        '''
        ret_code, ret_data = self.trade_ctx.order_list_query(trd_env=trd_env,acc_id=acc_id, acc_index=acc_index)
        if len(ret_data) >0:
            for index in range(len(ret_data)):
                flag_isBuy = ret_data['trd_side'][index] == TrdSide.BUY
                flag_canCancel = (ret_data['order_status'][index] == OrderStatus.SUBMITTED) or (ret_data['order_status'][index] == OrderStatus.FILLED_PART)
                if flag_isBuy and flag_canCancel:
                    order_id_tmp = ret_data['order_id'][index]
                    #撤单
                    self.trade_ctx.modify_order(modify_order_op = ModifyOrderOp.CANCEL, order_id =order_id_tmp, qty = 0, price= 0,adjust_limit=0, trd_env=trd_env, acc_id=acc_id, acc_index=acc_index)


class TradeCNBase(unittest.TestCase):
    '''A股模拟交易测试基类'''

    @classmethod
    def setUpClass(cls):
        #每次调用该类时触发一次
        global logger,trade_ctx,quote_ctx,trade_pwd
        #实例化日志对象
        # logger = Logs.geLogger(cls.__name__)
        #实例化上下文对象
        trade_ctx = OpenCNTradeContext(host=host_local, port=port_trade)
        quote_ctx = OpenQuoteContext(host=host_local, port=port_quote)
        # 解锁交易
        trade_ctx.unlock_trade(trade_pwd)

    def setUp(self):
        #每次调用def test()时触发一次
        self.trade_ctx = trade_ctx
        self.logger = logger
        self.quote_ctx = quote_ctx
        # self.quoteBase = QuotationBase()    #依赖行情测试基类的部分常用方法

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        quote_ctx.close()
        trade_ctx.close()

    def placeOrder(self, code, trd_side, order_type, deal ,trd_env=TrdEnv.SIMULATE, price = None,qty = None,adjust_limit = None,acc_id=0, acc_index=0):
        '''
        快速下单，必填code, trd_side, order_type并关注trd_env即可。
        :param code: 必填，股票代码
        :param trd_side: 必填，买卖方向
        :param order_type: 必填，订单类型
        :param deal：必填，bool,是否立刻成交,True-立刻成交
        :param trd_env: 环境，默认是模拟环境。
        :param price:  订单价格，默认偏离最高/最低价5个价位
        :param qty: 订单数量（股、张），默认1手/1张
        :param adjust_limit: 价格调整幅度，默认随机生成
        :param acc_id: 账号id
        :param acc_index: 账号index,默认第1个

        :return:
            ret_code_po：下单响应码
            ret_data_po：下单响应订单内容
            params：下单入参，字段
        '''
        if price == None or qty ==None or adjust_limit ==None:  #价格、数量、价格调整幅度为空时，需要程序实现数据填充
            ret_code_ms, ret_data_ms = self.quote_ctx.get_market_snapshot(code)
            if ret_code_ms == RET_OK:
                high_price_v = ret_data_ms['high_price'][0] #当天最高价
                low_price_v = ret_data_ms['low_price'][0]   #当天最低价
                lot_size_v = ret_data_ms['lot_size'][0]     #没手股数
                price_spread_v = ret_data_ms['price_spread'][0] #价差
                price_spread_num = 5
                if price == None:
                    if (trd_side == TrdSide.BUY and deal) or (trd_side == TrdSide.SELL and (not deal)):
                        price = high_price_v + price_spread_v * price_spread_num  # 比最高价再+price_spread_num个价位，促成立刻买入成交;同理避免立刻卖出。
                    else:
                        price = low_price_v - price_spread_v * price_spread_num  # 比最低价-price_spread_num个价位，促成立刻卖出成交;同理避免立刻买入。
                if qty == None:
                    qty = lot_size_v
                if adjust_limit == None:
                    adjust_limit = random.random()
            else:
                return  ret_code_ms, ret_data_ms,None    #获取市场快照失败
        #入参
        param_dict = {}
        param_dict['price'] = price
        param_dict['qty'] = qty
        param_dict['code'] = code
        param_dict['trd_side'] = trd_side
        param_dict['order_type'] = order_type
        param_dict['adjust_limit'] = adjust_limit
        param_dict['trd_env'] = trd_env
        param_dict['acc_id'] = acc_id
        param_dict['acc_index'] = acc_index
        param_dict['place_order_time'] = time.time()    #调用place_order接口的时间戳,float
        #下单
        ret_code_po, ret_data_po = self.trade_ctx.place_order(round(price, 2), qty, code, trd_side, order_type,adjust_limit, trd_env, acc_id, acc_index)
        return ret_code_po,ret_data_po,param_dict

    def cancelAllOrderBuy(self, trd_env=TrdEnv.SIMULATE, acc_id=0, acc_index=0):
        '''
        撤单：所有“买入”等待成交或部分成交的订单
        :param trd_env:
        :param acc_id:
        :param acc_index:
        :return:
        '''
        ret_code, ret_data = self.trade_ctx.order_list_query(trd_env=trd_env,acc_id=acc_id, acc_index=acc_index)
        if len(ret_data) >0:
            for index in range(len(ret_data)):
                flag_isBuy = ret_data['trd_side'][index] == TrdSide.BUY
                flag_canCancel = (ret_data['order_status'][index] == OrderStatus.SUBMITTED) or (ret_data['order_status'][index] == OrderStatus.FILLED_PART)
                if flag_isBuy and flag_canCancel:
                    order_id_tmp = ret_data['order_id'][index]
                    #撤单
                    self.trade_ctx.modify_order(modify_order_op = ModifyOrderOp.CANCEL, order_id =order_id_tmp, qty = 0, price= 0,adjust_limit=0, trd_env=trd_env, acc_id=acc_id, acc_index=acc_index)