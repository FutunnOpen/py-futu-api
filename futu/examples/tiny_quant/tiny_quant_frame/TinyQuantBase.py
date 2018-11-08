# encoding: UTF-8

'''
    用到的vnpy的相关接口
'''

from __future__ import division

import logging
from datetime import datetime
import time
import numpy as np
import talib

# from vnpy.event import *
# from vnpy.event.eventType import EVENT_TIMER
# from vnpy.trader.vtObject import VtBaseData
# from vnpy.trader.vtFunction import getJsonPath, getTempPath
# from vnpy.trader.language.chinese.constant import (EMPTY_STRING, EMPTY_UNICODE,
#                                     EMPTY_FLOAT, EMPTY_INT)


########################################################################
class VtBaseData(object):
    """回调函数推送数据的基础类，其他数据类继承于此"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.gatewayName = ""             # Gateway名称
        self.rawData = None                     # 原始数据


"""
    为了兼容python3.6且 且兼容vnpy外发的版本，
    暂时从vnpy dev分支copy部分实现类,
    后续直接从vnpy中导入
"""
########################################################################
# class VtLogData(VtBaseData):
#     """日志数据类"""
#
#     # ----------------------------------------------------------------------
#     def __init__(self):
#         """Constructor"""
#         super(VtLogData, self).__init__()
#
#         self.logTime = time.strftime('%X', time.localtime())  # 日志生成时间
#         self.logContent = EMPTY_UNICODE  # 日志信息
#         self.logLevel = logging.INFO

class ArrayManager(object):
    """
    K线序列管理工具，负责：
    1. K线时间序列的维护
    2. 常用技术指标的计算
    """

    # ----------------------------------------------------------------------
    def __init__(self, size=100):
        """Constructor"""
        self.count = 0  # 缓存计数
        self.size = size  # 缓存大小
        self.inited = False  # True if count>=size

        self.openArray = np.zeros(size)  # OHLC
        self.highArray = np.zeros(size)
        self.lowArray = np.zeros(size)
        self.closeArray = np.zeros(size)
        self.volumeArray = np.zeros(size)

    # ----------------------------------------------------------------------
    def updateBar(self, bar):
        """更新K线"""
        self.count += 1
        if not self.inited and self.count >= self.size:
            self.inited = True

        self.openArray[0:self.size - 1] = self.openArray[1:self.size]
        self.highArray[0:self.size - 1] = self.highArray[1:self.size]
        self.lowArray[0:self.size - 1] = self.lowArray[1:self.size]
        self.closeArray[0:self.size - 1] = self.closeArray[1:self.size]
        self.volumeArray[0:self.size - 1] = self.volumeArray[1:self.size]

        self.openArray[-1] = bar.open
        self.highArray[-1] = bar.high
        self.lowArray[-1] = bar.low
        self.closeArray[-1] = bar.close
        self.volumeArray[-1] = bar.volume

    # ----------------------------------------------------------------------
    @property
    def open(self):
        """获取开盘价序列"""
        return self.openArray

    # ----------------------------------------------------------------------
    @property
    def high(self):
        """获取最高价序列"""
        return self.highArray

    # ----------------------------------------------------------------------
    @property
    def low(self):
        """获取最低价序列"""
        return self.lowArray

    # ----------------------------------------------------------------------
    @property
    def close(self):
        """获取收盘价序列"""
        return self.closeArray

    # ----------------------------------------------------------------------
    @property
    def volume(self):
        """获取成交量序列"""
        return self.volumeArray

    # ----------------------------------------------------------------------
    def sma(self, n, array=False):
        """简单均线"""
        result = talib.SMA(self.close, n)
        if array:
            return result
        return result[-1]

    # ----------------------------------------------------------------------
    def std(self, n, array=False):
        """标准差"""
        result = talib.STDDEV(self.close, n)
        if array:
            return result
        return result[-1]

    # ----------------------------------------------------------------------
    def cci(self, n, array=False):
        """CCI指标"""
        result = talib.CCI(self.high, self.low, self.close, n)
        if array:
            return result
        return result[-1]

    # ----------------------------------------------------------------------
    def atr(self, n, array=False):
        """ATR指标"""
        result = talib.ATR(self.high, self.low, self.close, n)
        if array:
            return result
        return result[-1]

    # ----------------------------------------------------------------------
    def rsi(self, n, array=False):
        """RSI指标"""
        result = talib.RSI(self.close, n)
        if array:
            return result
        return result[-1]

    # ----------------------------------------------------------------------
    def macd(self, fastPeriod, slowPeriod, signalPeriod, array=False):
        """MACD指标"""
        macd, signal, hist = talib.MACD(self.close, fastPeriod,
                                        slowPeriod, signalPeriod)
        if array:
            return macd, signal, hist
        return macd[-1], signal[-1], hist[-1]

    # ----------------------------------------------------------------------
    def adx(self, n, array=False):
        """ADX指标"""
        result = talib.ADX(self.high, self.low, self.close, n)
        if array:
            return result
        return result[-1]

    # ----------------------------------------------------------------------
    def boll(self, n, dev, array=False):
        """布林通道"""
        mid = self.sma(n, array)
        std = self.std(n, array)

        up = mid + std * dev
        down = mid - std * dev

        return up, down

        # ----------------------------------------------------------------------

    def keltner(self, n, dev, array=False):
        """肯特纳通道"""
        mid = self.sma(n, array)
        atr = self.atr(n, array)

        up = mid + atr * dev
        down = mid - atr * dev

        return up, down

    # ----------------------------------------------------------------------
    def donchian(self, n, array=False):
        """唐奇安通道"""
        up = talib.MAX(self.high, n)
        down = talib.MIN(self.low, n)

        if array:
            return up, down
        return up[-1], down[-1]


########################################################################
# class LogEngine(object):
#     """日志引擎"""
#
#     # 日志级别
#     LEVEL_DEBUG = logging.DEBUG
#     LEVEL_INFO = logging.INFO
#     LEVEL_WARN = logging.WARN
#     LEVEL_ERROR = logging.ERROR
#     LEVEL_CRITICAL = logging.CRITICAL
#
#     # 单例对象
#     instance = None
#
#     # ----------------------------------------------------------------------
#     def __new__(cls, *args, **kwargs):
#         """创建对象，保证单例"""
#         if not cls.instance:
#             cls.instance = super(LogEngine, cls).__new__(cls, *args, **kwargs)
#         return cls.instance
#
#     # ----------------------------------------------------------------------
#     def __init__(self):
#         """Constructor"""
#         self.logger = logging.getLogger()
#         self.formatter = logging.Formatter('%(asctime)s  %(levelname)s: %(message)s')
#         self.level = self.LEVEL_CRITICAL
#
#         self.consoleHandler = None
#         self.fileHandler = None
#
#         # 添加NullHandler防止无handler的错误输出
#         nullHandler = logging.NullHandler()
#         self.logger.addHandler(nullHandler)
#
#         # 日志级别函数映射
#         self.levelFunctionDict = {
#             self.LEVEL_DEBUG: self.debug,
#             self.LEVEL_INFO: self.info,
#             self.LEVEL_WARN: self.warn,
#             self.LEVEL_ERROR: self.error,
#             self.LEVEL_CRITICAL: self.critical,
#         }
#
#     # ----------------------------------------------------------------------
#     def setLogLevel(self, level):
#         """设置日志级别"""
#         self.logger.setLevel(level)
#         self.level = level
#
#     # ----------------------------------------------------------------------
#     def addConsoleHandler(self):
#         """添加终端输出"""
#         if not self.consoleHandler:
#             self.consoleHandler = logging.StreamHandler()
#             self.consoleHandler.setLevel(self.level)
#             self.consoleHandler.setFormatter(self.formatter)
#             self.logger.addHandler(self.consoleHandler)
#
#     # ----------------------------------------------------------------------
#     def addFileHandler(self):
#         """添加文件输出"""
#         if not self.fileHandler:
#             filename = 'vt_' + datetime.now().strftime('%Y%m%d') + '.log'
#             filepath = getTempPath(filename)
#             self.fileHandler = logging.FileHandler(filepath)
#             self.fileHandler.setLevel(self.level)
#             self.fileHandler.setFormatter(self.formatter)
#             self.logger.addHandler(self.fileHandler)
#
#     # ----------------------------------------------------------------------
#     def debug(self, msg):
#         """开发时用"""
#         self.logger.debug(msg)
#
#     # ----------------------------------------------------------------------
#     def info(self, msg):
#         """正常输出"""
#         self.logger.info(msg)
#
#     # ----------------------------------------------------------------------
#     def warn(self, msg):
#         """警告信息"""
#         self.logger.warn(msg)
#
#     # ----------------------------------------------------------------------
#     def error(self, msg):
#         """报错输出"""
#         self.logger.error(msg)
#
#     # ----------------------------------------------------------------------
#     def exception(self, msg):
#         """报错输出+记录异常信息"""
#         self.logger.exception(msg)
#
#     # ----------------------------------------------------------------------
#     def critical(self, msg):
#         """影响程序运行的严重错误"""
#         self.logger.critical(msg)

    # ----------------------------------------------------------------------
    # def processLogEvent(self, event):
    #     """处理日志事件"""
    #     log = event.dict_['data']
    #     function = self.levelFunctionDict[log.logLevel]  # 获取日志级别对应的处理函数
    #     msg = '\t'.join([log.gatewayName, log.logContent])
    #     function(msg)