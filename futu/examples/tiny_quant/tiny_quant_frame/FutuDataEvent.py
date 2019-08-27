# encoding: UTF-8
'''

'''

import time
from copy import copy
from datetime import datetime, timedelta
from .TinyDefine import *
from .TinyQuantBase import *
import futu as ft
from .event.eventEngine import *

class FutuDataEvent(object):
    name = "FutuDataEvent"

    def __init__(self, quant_frame, quote_context, event_engine, symbol_pools):
        self._quant_frame = quant_frame
        self._quote_context = quote_context
        self._event_engine = event_engine
        self._symbol_pools = symbol_pools
        self._tick_dict = {}
        self._market_opened= False

        # 控制频率，1秒钟最多推送quote多少次
        self._push_event_freq = 10
        self._dict_last_push_time = {}

        # 记录当前股票池的实时行情数据
        self._rt_tiny_quote = {}

        self._sym_kline_am_dict = {}   # am = ArrayManager

        self._sym_kline_last_am_bar_dic = {} # 记录am 最后一个bar的数据
        self._sym_kline_last_event_bar_dic = {} # 记录最后一个事件推送的bar
        self._sym_kline_next_event_bar_dic = {} # 记录下一个准备推送的bar

        # 注册事件
        self._event_engine.register(EVENT_TINY_TICK, self._event_tiny_tick)
        self._event_engine.register(EVENT_CUR_KLINE_PUSH, self._event_cur_kline_push)
        self._event_engine.register(EVENT_BEFORE_TRADING, self.__event_before_trading)
        self._event_engine.register(EVENT_AFTER_TRADING, self.__event_after_trading)
        self._event_engine.register(EVENT_AFTER_TRADING_FINAL, self.__event_after_trading_final)

        class QuoteHandler(ft.StockQuoteHandlerBase):
            """报价处理器"""
            futu_data_event = self

            def on_recv_rsp(self, rsp_str):
                ret_code, content = super(QuoteHandler, self).on_recv_rsp(rsp_str)
                if ret_code != ft.RET_OK:
                    return ft.RET_ERROR, content
                self.futu_data_event.process_quote(content)
                return ft.RET_OK, content

        class OrderBookHandler(ft.OrderBookHandlerBase):
            """摆盘处理器"""
            futu_data_event = self

            def on_recv_rsp(self, rsp_str):
                ret_code, content = super(OrderBookHandler, self).on_recv_rsp(rsp_str)
                if ret_code != ft.RET_OK:
                    return ft.RET_ERROR, content
                self.futu_data_event.process_orderbook(content)
                return ft.RET_OK, content

        class CurKlineHandler(ft.CurKlineHandlerBase):
            """实时k线推送处理器"""
            futu_data_event = self

            def on_recv_rsp(self, rsp_str):
                ret_code, content = super(CurKlineHandler, self).on_recv_rsp(rsp_str)
                if ret_code != ft.RET_OK:
                    return ft.RET_ERROR, content
                self.futu_data_event.process_curkline(content)
                return ft.RET_OK, content

        # 设置回调处理对象
        self._quote_context.set_handler(QuoteHandler())
        self._quote_context.set_handler(OrderBookHandler())
        self._quote_context.set_handler(CurKlineHandler())

        # 定阅数据
        subtype_list = [ft.SubType.QUOTE, ft.SubType.ORDER_BOOK, ft.SubType.K_DAY, ft.SubType.K_1M]
        ret, data = self._quote_context.subscribe(symbol_pools, subtype_list)
        if ret != ft.RET_OK:
            raise Exception('订阅行情失败：{}'.format(data))

        # 启动时先构建一次数据
        self._rebuild_sym_kline_all()

    def get_rt_tiny_quote(self, symbol):
        """得到股票的实时行情数据"""
        if symbol in self._rt_tiny_quote:
            return self._rt_tiny_quote[symbol]
        return None

    def get_kl_min1_am(self, symbol):
        return self._get_kl_am(symbol, KTYPE_MIN1)

    def get_kl_day_am(self, symbol):
        return self._get_kl_am(symbol, KTYPE_DAY)

    def _get_kl_am(self, symbol, ktype):
        if symbol not in self._sym_kline_am_dict.keys():
            return None
        if ktype not in self._sym_kline_am_dict[symbol].keys():
            return None
        return self._sym_kline_am_dict[symbol][ktype]

    def _rebuild_sym_kline_am(self, symbol, ktype):
        # 构造k线数据
        kline_max_size = MAP_KLINE_SIZE[ktype]
        if symbol not in self._sym_kline_am_dict:
            self._sym_kline_am_dict[symbol] = {}
        self._sym_kline_am_dict[symbol][ktype] = ArrayManager(kline_max_size)

        if symbol not in self._sym_kline_last_am_bar_dic.keys():
            self._sym_kline_last_am_bar_dic[symbol] = {}
        self._sym_kline_last_am_bar_dic[symbol][ktype] = None
        last_am_bar = None
        #
        array_manager = self._sym_kline_am_dict[symbol][ktype]

        # 导入历史数据
        dt_now = datetime.now()
        # 历史日k取近365天的数据 , 其它k线类型取近3天的数据
        dt_start = dt_now - timedelta(days= 365 if ktype == KTYPE_DAY else 3)
        str_start = dt_start.strftime("%Y-%m-%d")
        str_end = dt_now.strftime("%Y-%m-%d")
        ret, data, page_req_key = self._quote_context.request_history_kline(code=symbol, start=str_start, end=str_end, ktype=ktype, autype=ft.AuType.QFQ)
        if ret == 0:
            # with GLOBAL.dt_lock:
            for ix, row in data.iterrows():
                bar = TinyBarData()
                bar.open = row['open']
                bar.close = row['close']
                bar.high = row['high']
                bar.low = row['low']
                bar.volume = row['volume']
                bar.symbol = symbol
                dt_bar = datetime.strptime(str(row['time_key']), "%Y-%m-%d %H:%M:%S")
                bar.datetime = dt_bar
                if not last_am_bar or dt_bar > last_am_bar.datetime:
                    array_manager.updateBar(bar)
                    last_am_bar = bar

        # 导入今天的最新数据
        ret, data = self._quote_context.get_cur_kline(code=symbol, num=1000, ktype=ktype, autype=ft.AuType.QFQ)
        if ret == 0:
            # with GLOBAL.dt_lock:
            for ix, row in data.iterrows():
                bar = TinyBarData()
                bar.open = row['open']
                bar.close = row['close']
                bar.high = row['high']
                bar.low = row['low']
                bar.volume = row['volume']
                bar.symbol = symbol
                dt_bar = datetime.strptime(str(row['time_key']), "%Y-%m-%d %H:%M:%S")
                bar.datetime = dt_bar
                if not last_am_bar or dt_bar > last_am_bar.datetime:
                    array_manager.updateBar(bar)
                    last_am_bar = bar

        # 记录最后一次导入的数据，在实时数据来到时，会依据时间判断是否推送
        self._sym_kline_last_am_bar_dic[symbol][ktype] = last_am_bar

    def log(self, content):
        content = self.name + ':' + content
        if self._quant_frame is not None:
            self._quant_frame.writeCtaLog(content)

    def _notify_new_tick_event(self, tick):
        """tick推送"""
        if tick.time is '':
            return
        event = Event(type_=EVENT_TINY_TICK)
        event.dict_['data'] = tick
        self._event_engine.put(event)

    def _notify_quote_change_event(self, tiny_quote):
        """推送"""
        if not self._market_opened:
            return

        event = Event(type_=EVENT_QUOTE_CHANGE)
        event.dict_['data'] = tiny_quote
        self._rt_tiny_quote[tiny_quote.symbol] = tiny_quote
        self._event_engine.put(event)

    def _event_tiny_tick(self, event):
        tick = event.dict_['data']
        t_now = time.time()
        t_last, count_last = 0, 0

        # 控制频率推送行情变化
        if tick.symbol in self._dict_last_push_time:
            t_last, count_last = self._dict_last_push_time[tick.symbol]

        if t_last != t_now or count_last + 1 <= self._push_event_freq:
            t_last = t_now
            count_last += 1
            self._dict_last_push_time[tick.symbol] = (t_last, count_last)
            self._notify_quote_change_event(tick)

    def _event_cur_kline_push(self, event):
        bars_data = event.dict_['bars_data']
        symbol = event.dict_['symbol']
        ktype = event.dict_['ktype']

        if symbol not in self._sym_kline_last_am_bar_dic.keys() or symbol not in self._sym_kline_am_dict.keys():
            return
        if ktype not in self._sym_kline_last_am_bar_dic[symbol].keys() or ktype not in self._sym_kline_am_dict[symbol].keys():
            return

        # 上一次新增的am数据
        last_am_bar = self._sym_kline_last_am_bar_dic[symbol][ktype]
        array_manager = self._sym_kline_am_dict[symbol][ktype]

        # 上一次推送的event bar数据
        if symbol not in self._sym_kline_last_event_bar_dic.keys():
            self._sym_kline_last_event_bar_dic[symbol] = {}
        if ktype not in self._sym_kline_last_event_bar_dic[symbol].keys():
            self._sym_kline_last_event_bar_dic[symbol][ktype] = None
        last_event_bar = self._sym_kline_last_event_bar_dic[symbol][ktype]

        # 下一步将要推送的event bar数据
        if symbol not in self._sym_kline_next_event_bar_dic.keys():
            self._sym_kline_next_event_bar_dic[symbol] = {}
        if ktype not in self._sym_kline_next_event_bar_dic[symbol].keys():
            self._sym_kline_next_event_bar_dic[symbol][ktype] = None
        next_event_bar = self._sym_kline_next_event_bar_dic[symbol][ktype]

        notify_bar = None

        for bar in bars_data:
            dt = bar.datetime
            # 更新am最后一个点数据
            if last_am_bar and last_am_bar.datetime == dt:
                # self.log("last_am_bar dt = %s vol=%s" % (last_am_bar.datetime.strftime("%H:%M:%S"), last_am_bar.volume))
                array_manager.openArray[-1] = bar.open
                array_manager.closeArray[-1] = bar.close
                array_manager.highArray[-1] = bar.high
                array_manager.lowArray[-1] = bar.low
                array_manager.volumeArray[-1] = bar.volume
                if not next_event_bar:
                    next_event_bar = bar
                # self.log("next_event_bar dt = %s vol=%s" % (next_event_bar.datetime.strftime("%H:%M:%S"), next_event_bar.volume))

            # 已经推送过的点，又来了一次新的点
            if last_event_bar and dt == last_event_bar.datetime:
                notify_bar = bar

            # 新的bar数据累积中
            elif not last_event_bar or dt > last_event_bar.datetime:
                # 之前记录的next_event_bar 推送
                if next_event_bar and dt > next_event_bar.datetime:
                    notify_bar = next_event_bar
                    next_event_bar = None

                    # 更新am数据
                    if not last_am_bar or notify_bar.datetime > last_am_bar.datetime:
                        array_manager.updateBar(notify_bar)
                        last_am_bar = notify_bar
                        self._sym_kline_last_am_bar_dic[symbol][ktype] = last_am_bar
                else:
                    # 记录将在下一次推送的bar
                    next_event_bar = bar
            else:
                continue # 已经存在的点，忽略

        if self._sym_kline_next_event_bar_dic[symbol][ktype] is not next_event_bar:
            self._sym_kline_next_event_bar_dic[symbol][ktype] = next_event_bar

        # 对外通知事件
        if notify_bar and self._market_opened:
            self._sym_kline_last_event_bar_dic[symbol][ktype] = notify_bar

            event = Event(type_=EVENT_CUR_KLINE_BAR)
            event.dict_['symbol'] = symbol
            event.dict_['data'] = notify_bar
            event.dict_['ktype'] = ktype
            self._event_engine.put(event)

    def _rebuild_sym_kline_all(self):
        for symbol  in  self._symbol_pools:
            for ktype in [KTYPE_DAY, KTYPE_MIN1]:
                self._rebuild_sym_kline_am(symbol, ktype)

    def __event_before_trading(self, event):
        self._rebuild_sym_kline_all()
        self._market_opened = True

    def __event_after_trading_final(self, event):
        self._market_opened = False
        self.__process_last_kl_push([KTYPE_DAY, KTYPE_MIN1, KTYPE_MIN5, KTYPE_MIN15, KTYPE_MIN30, KTYPE_MIN60])

    def __event_after_trading(self, event):
        self._market_opened = False

    def __process_last_kl_push(self, kl_types):
        # 收盘将没推送的数据点再推一次
        for symbol in self._sym_kline_next_event_bar_dic.keys():
            for ktype in self._sym_kline_next_event_bar_dic[symbol].keys():
                if ktype not in kl_types:
                    continue
                notify_bar = self._sym_kline_next_event_bar_dic[symbol][ktype]
                if not notify_bar:
                    continue
                self._sym_kline_next_event_bar_dic[symbol][ktype] = None

                array_manager = self._get_kl_am(symbol, ktype)
                if not array_manager:
                    continue

                last_am_bar = None
                if symbol in self._sym_kline_last_am_bar_dic.keys() and ktype in self._sym_kline_last_am_bar_dic[
                    symbol].keys():
                    last_am_bar = self._sym_kline_last_am_bar_dic[symbol][ktype]

                if last_am_bar.datetime != notify_bar.datetime:
                    array_manager.updateBar(notify_bar)

                # 对外通知事件
                event = Event(type_=EVENT_CUR_KLINE_BAR)
                event.dict_['symbol'] = symbol
                event.dict_['data'] = notify_bar
                event.dict_['ktype'] = ktype
                self._event_engine.put(event)

    def process_quote(self, data):
        """报价推送"""
        for ix, row in data.iterrows():
            symbol = row['code']

            tick = self._tick_dict.get(symbol, None)
            if not tick:
                tick = TinyQuoteData()
                tick.symbol = symbol
                self._tick_dict[symbol] = tick

            tick.date = row['data_date'].replace('-', '')
            tick.time = row['data_time']
            # with GLOBAL.dt_lock:
            if tick.date and tick.time:
                tick.datetime = datetime.strptime(' '.join([tick.date, tick.time]), '%Y%m%d %H:%M:%S')
            else:
                return

            tick.openPrice = row['open_price']
            tick.highPrice = row['high_price']
            tick.lowPrice = row['low_price']
            tick.preClosePrice = row['prev_close_price']
            # 1.25 新增摆盘价差，方便计算正确的订单提交价格 要求牛牛最低版本 v3.42.4961.125
            if 'price_spread' in row:
                tick.priceSpread = row['price_spread']

            tick.lastPrice = row['last_price']
            tick.volume = row['volume']

            new_tick = copy(tick)
            self._notify_new_tick_event(new_tick)

    def process_orderbook(self, data):
        """订单簿推送"""
        symbol = data['code']

        tick = self._tick_dict.get(symbol, None)
        if not tick:
            tick = TinyQuoteData()
            tick.symbol = symbol
            self._tick_dict[symbol] = tick

        d = tick.__dict__
        for i in range(5):
            bid_data = data['Bid'][i]
            ask_data = data['Ask'][i]
            n = i + 1

            d['bidPrice%s' % n] = bid_data[0]
            d['bidVolume%s' % n] = bid_data[1]
            d['askPrice%s' % n] = ask_data[0]
            d['askVolume%s' % n] = ask_data[1]

            new_tick = copy(tick)
        self._notify_new_tick_event(new_tick)

    def process_curkline(self, data):
        """k线实时数据推送"""
        # 每一次推送， 只会是同一个symbole + kltype
        bars_data = []
        symbol = ""
        ktype = ""
        for ix, row in data.iterrows():
            symbol = row['code']
            ktype = row['k_type']
            bar = TinyBarData()
            bar.open = row['open']
            bar.close = row['close']
            bar.high = row['high']
            bar.low = row['low']
            bar.volume = row['volume']
            bar.symbol = symbol
            # with GLOBAL.dt_lock:
            bar.datetime = datetime.strptime(str(row['time_key']), "%Y-%m-%d %H:%M:%S")

            bars_data.append(bar)
            # print('process_curkline - ktype=%s symbol=%s' % (ktype, symbol))

        if not bars_data or not symbol or not ktype:
            return

        """这个回调是在异步线程， 使用event抛到框架数据处理线程中"""
        event = Event(type_=EVENT_CUR_KLINE_PUSH)
        event.dict_['bars_data'] = bars_data
        event.dict_['symbol'] = symbol
        event.dict_['ktype'] = ktype
        self._event_engine.put(event)




