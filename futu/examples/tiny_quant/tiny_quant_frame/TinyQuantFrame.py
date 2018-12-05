# encoding: UTF-8

"""

"""
import json
from .FutuMarketEvent import *
from .FutuDataEvent import *
from .event.eventEngine import *
import futu as ft
import os
import logging
import platform

__LogPathName__ = "com.futunn.FutuOpenD//Log"

def getJsonPath(name, moduleFile):
    """
    获取JSON配置文件的路径：
    1. 优先从当前工作目录查找JSON文件
    2. 若无法找到则前往模块所在目录查找
    """
    currentFolder = os.getcwd()
    currentJsonPath = os.path.join(currentFolder, name)
    if os.path.isfile(currentJsonPath):
        return currentJsonPath
    else:
        moduleFolder = os.path.abspath(os.path.dirname(moduleFile))
        moduleJsonPath = os.path.join(moduleFolder, '.', name)
        return moduleJsonPath



class TinyQuantFrame(object):
    """策略frame"""
    settingFileName = 'setting.json'
    settingfilePath = getJsonPath(settingFileName, __file__)
    _logger = None

    def __init__(self, tinyStrate):
        """frame settings"""
        self._api_ip = None
        self._api_port = None
        self._market = None
        self._env_type = None
        self._trade_password = None

        self._global_settings = {}
        self._is_init = False

        self.consoleHandler = None
        self.fileHandler = None

        self._tiny_strate = tinyStrate
        # self._logger = LogEngine()
        self._event_engine = EventEngine2()

        # 这里没有用None,因为None在 __loadSetting中当作错误参数检查用了
        self._quote_ctx = 0
        self._trade_ctx = 0
        self._check_market_event = 0
        self._futu_data_event = 0

        self._is_start = False
        self._is_init = self.__loadSetting()
        self.__init_log_engine()  # 初始化log
        if self._is_init:
            self._tiny_strate.init_strate(self._global_settings, self, self._event_engine)



    @property
    def today_date(self):
        """今天的日期，服务器数据"""
        return self._check_market_event.today_date

    def get_rt_tiny_quote(self, symbol):
        """得到股票的实时行情数据"""
        return self._futu_data_event.get_rt_tiny_quote(symbol)

    def get_kl_min1_am(self, symbol):
        """一分钟k线的array manager数据"""
        return self._futu_data_event.get_kl_min1_am(symbol)

    def get_kl_day_am(self, symbol):
        """日k线的array manager数据"""
        return self._futu_data_event.get_kl_day_am(symbol)

    def buy(self, price, volume, symbol, order_type=ft.OrderType.NORMAL, adjust_limit=0, acc_id=0):
        """买入"""
        ret, data = self._trade_ctx.place_order(price=price, qty=volume, code=symbol, trd_side=ft.TrdSide.BUY,
                                                order_type=order_type, adjust_limit=adjust_limit,
                                                trd_env=self._env_type, acc_id=acc_id)
        if ret != ft.RET_OK:
            return ret, data

        order_id = 0
        for ix, row in data.iterrows():
            order_id = str(row['order_id'])

        return ret, order_id

    def sell(self, price, volume, symbol, order_type=ft.OrderType.NORMAL, adjust_limit=0, acc_id=0):
        """卖出"""
        ret, data = self._trade_ctx.place_order(price=price, qty=volume, code=symbol, trd_side=ft.TrdSide.SELL,
                                                order_type=order_type, adjust_limit=adjust_limit,
                                                trd_env=self._env_type, acc_id=acc_id)
        if ret != ft.RET_OK:
            return ret, data
        order_id = 0
        for ix, row in data.iterrows():
            order_id = str(row['order_id'])

        return ret, order_id

    def cancel_order(self, order_id, acc_id=0):
        """取消订单"""
        ret, data = self._trade_ctx.modify_order(ft.ModifyOrderOp.CANCEL, order_id=order_id, qty=0, price=0,
                                                 adjust_limit=0, trd_env=self._env_type, acc_id=acc_id)

        # ret不为0时， data为错误字符串
        if ret == ft.RET_OK:
            return ret, ''
        else:
            return ret, data

    def get_tiny_trade_order(self, order_id, acc_id=0):
        """得到订单信息"""
        ret, data = self._trade_ctx.order_list_query(order_id=order_id, status_filter_list=[], code='', start='',
                                                     end='', trd_env=self._env_type, acc_id=acc_id)
        if ret != ft.RET_OK:
            return ret, data

        order = TinyTradeOrder()
        for ix, row in data.iterrows():
            if order_id != str(row['order_id']):
                continue
            order.symbol = row['code']
            order.order_id = order_id
            order.direction = row['trd_side']

            order.price = float(row['price'])
            order.total_volume = int(row['qty'])
            order.trade_volume = int(row['dealt_qty'])
            order.create_time = row['create_time']
            order.updated_time = row['updated_time']
            order.trade_avg_price = float(row['dealt_avg_price']) if row['dealt_avg_price'] else 0
            order.order_status = row['order_status']
            break
        return ret, order

    def get_tiny_position(self, symbol, acc_id=0):
        """得到股票持仓"""
        ret, data = self._trade_ctx.position_list_query(code=symbol, trd_env=self._env_type, acc_id=acc_id)
        if 0 != ret:
            return None

        for _, row in data.iterrows():
            if row['code'] != symbol:
                continue
            pos = TinyPosition()
            pos.symbol = symbol
            pos.position = row['qty']
            pos.frozen = pos.position - row['can_sell_qty']
            pos.price = row['cost_price']
            pos.market_value = row['market_val']
            return pos
        return None

    def writeCtaLog(self, content):
        self._logger.info(content)
        # log = VtLogData()
        # log.logContent = content
        # log.gatewayName = 'FUTU'
        # event = Event(type_=EVENT_TINY_LOG)
        # event.dict_['data'] = log
        # self._event_engine.put(event)

    #初始化log
    def __init_log_engine(self):
        if self._logger is None:
            self._logger = logging.getLogger('FTDemo')
            self.formatter = logging.Formatter('%(asctime)s  %(levelname)s: %(message)s')
            sys_str = platform.system()
            if sys_str == "Windows":
                self.log_path = os.path.join(os.getenv("appdata"), __LogPathName__)
            else:
                self.log_path = os.path.join(os.environ['HOME'], ("." + __LogPathName__))

            # 添加NullHandler防止无handler的错误输出
            null_handler = logging.NullHandler()
            self._logger.addHandler(null_handler)

            # 设置日志级别
            frame_setting = self._global_settings["frame"]
            level_dict = {
                "debug": logging.DEBUG,
                "info": logging.INFO,
                "warn": logging.WARN,
                "error": logging.ERROR,
                "critical": logging.CRITICAL
            }
            level = level_dict.get(frame_setting["logLevel"], logging.CRITICAL)
            self._logger.setLevel(level)

            # 设置输出
            if frame_setting['logConsole']:
                if not self.consoleHandler:
                    self.consoleHandler = logging.StreamHandler()
                    self.consoleHandler.setLevel(level)
                    self.consoleHandler.setFormatter(self.formatter)
                    self._logger.addHandler(self.consoleHandler)

            if frame_setting['logFile']:
                if not self.fileHandler:
                    filename = 'vt_' + datetime.now().strftime('%Y_%m_%d') + '.log'
                    filepath = os.path.join(self.log_path, filename)
                    self.fileHandler = logging.FileHandler(filepath)
                    self.fileHandler.setLevel(level)
                    self.fileHandler.setFormatter(self.formatter)
                    self._logger.addHandler(self.fileHandler)


    def __loadSetting(self):
        """读取策略配置"""
        with open(self.settingfilePath, 'rb') as f:
            df = f.read()
            f.close()
            if type(df) is not str:
                df = ft.str_utf8(df)
            self._global_settings = json.loads(df)
            if self._global_settings is None or 'frame' not in self._global_settings:
                raise Exception("setting.json - no frame config!'")

            # 设置frame参数
            frame_setting = self._global_settings['frame']
            d = self.__dict__
            for key in d.keys():
                if key in frame_setting.keys():
                    d[key] = frame_setting[key]

            # check paramlist
            # for key in d.keys():
            #     if d[key] is None:
            #         str_error = "setting.json - 'frame' config no key:'%s'" % key
            #         raise Exception(str_error)

            # check _env_type / market
            env_list = [ft.TrdEnv.REAL, ft.TrdEnv.SIMULATE]
            if self._env_type not in env_list:
                str_error = "setting.json - 'frame' config '_env_type' can only is '{}'".format(','.join(env_list))
                raise Exception(str_error)

            market_list = [ft.Market.HK, ft.Market.US]
            if self._market not in market_list:
                str_error = "setting.json - 'frame' config '_market' can only is '{}'".format(','.join(market_list))
                raise Exception(str_error)

        return True

    # def __initLogEngine(self):
    #     # 设置日志级别
    #     frame_setting = self._global_settings['frame']
    #     levelDict = {
    #         "debug": LogEngine.LEVEL_DEBUG,
    #         "info": LogEngine.LEVEL_INFO,
    #         "warn": LogEngine.LEVEL_WARN,
    #         "error": LogEngine.LEVEL_ERROR,
    #         "critical": LogEngine.LEVEL_CRITICAL,
    #     }
    #     level = levelDict.get(frame_setting["logLevel"], LogEngine.LEVEL_CRITICAL)
    #     self._logger.setLogLevel(level)
    #
    #     # 设置输出
    #     if frame_setting['logConsole']:
    #         self._logger.addConsoleHandler()
    #
    #     if frame_setting['logFile']:
    #         self._logger.addFileHandler()

        # log事件监听
        # self._event_engine.register(EVENT_TINY_LOG, self._logger.processLogEvent)
        # self._event_engine.register(EVENT_INI_FUTU_API, self._process_init_api)

    def _process_init_api(self):
        if type(self._quote_ctx) != int or type(self._trade_ctx) != int:
            return

        # 创建futu api对象
        if self._quote_ctx == 0:
            self._quote_ctx = ft.OpenQuoteContext(self._api_ip, self._api_port)
        if self._trade_ctx == 0:
            if self._market == MARKET_HK:
                self._trade_ctx = ft.OpenHKTradeContext(self._api_ip, self._api_port)
            elif self._market == MARKET_US:
                self._trade_ctx = ft.OpenUSTradeContext(self._api_ip, self._api_port)
            else:
                raise Exception("error param!")

        if self._env_type == ft.TrdEnv.REAL:
            ret, _ = self._trade_ctx.unlock_trade(self._trade_password)
            if 0 != ret:
                raise Exception("error param!")

        # 开始futu api异步数据推送
        self._quote_ctx.start()
        self._trade_ctx.start()

        # 市场状态检查
        self._check_market_event = FutuMarketEvent(self._market, self._quote_ctx, self._event_engine)

        #定阅行情数据
        self._futu_data_event = FutuDataEvent(self, self._quote_ctx, self._event_engine, self._tiny_strate.symbol_pools)

        # 启动事件
        self._tiny_strate.on_start()

    def run(self):
        # 启动事件引擎
        if self._is_init and not self._is_start:
            self._is_start = True
            self._process_init_api()
            #self._event_engine.put(Event(type_=EVENT_INI_FUTU_API))
            self._event_engine.start(timer=True)

    def stop(self):
        # 退出所有事件
        if self._quote_ctx != 0:
            self._quote_ctx.close()
            del self._quote_ctx
            self._quote_ctx = 0
        if self._trade_ctx != 0:
            self._trade_ctx.close()
            del self._trade_ctx
            self._trade_ctx = 0

        try:
            if self._is_init and self._is_start:
                #self._event_engine.unregister(EVENT_INI_FUTU_API, self._process_init_api)
                #self._event_engine.unregister(EVENT_TINY_LOG, self._logger.processLogEvent)
                self._is_start = False
                self._event_engine.stop()

        except Exception as err:
            print(err)

        del self._tiny_strate

        time.sleep(5)

