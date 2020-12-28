# -*- coding: utf-8 -*-
import pandas as pd
from futu.common import RspHandlerBase
from futu.quote.quote_query import *


class StockQuoteHandlerBase(RspHandlerBase):
    """
    异步处理推送的订阅股票的报价。

    .. code:: python

        class StockQuoteTest(StockQuoteHandlerBase):
            def on_recv_rsp(self, rsp_str):
                ret_code, content = super(StockQuoteTest,self).on_recv_rsp(rsp_str)
                if ret_code != RET_OK:
                    print("StockQuoteTest: error, msg: %s" % content)
                    return RET_ERROR, content

                print("StockQuoteTest ", content) # StockQuoteTest自己的处理逻辑

                return RET_OK, content
    """
    @classmethod
    def parse_rsp_pb(cls, rsp_pb):
        ret_code, msg, quote_list = StockQuoteQuery.unpack_rsp(rsp_pb)
        if ret_code != RET_OK:
            return ret_code, msg
        else:
            return RET_OK, quote_list

    def on_recv_rsp(self, rsp_pb):
        """
        在收到实时报价推送后会回调到该函数，使用者需要在派生类中覆盖此方法

        注意该回调是在独立子线程中

        :param rsp_pb: 派生类中不需要直接处理该参数
        :return: 参见get_stock_quote的返回值
        """
        ret_code, content = self.parse_rsp_pb(rsp_pb)
        if ret_code != RET_OK:
            return ret_code, content
        else:
            col_list = [
                'code', 'data_date', 'data_time', 'last_price', 'open_price',
                'high_price', 'low_price', 'prev_close_price', 'volume',
                'turnover', 'turnover_rate', 'amplitude', 'suspension',
                'listing_date', 'price_spread', 'dark_status', 'sec_status', 'strike_price',
                'contract_size', 'open_interest', 'implied_volatility',
                'premium', 'delta', 'gamma', 'vega', 'theta', 'rho',
                'net_open_interest', 'expiry_date_distance', 'contract_nominal_value', 
                'owner_lot_multiplier', 'option_area_type', 'contract_multiplier',
                'last_settle_price', 'position', 'position_change', 'index_option_type'
            ]

            col_list.extend(row[0] for row in pb_field_map_PreAfterMarketData_pre)
            col_list.extend(row[0] for row in pb_field_map_PreAfterMarketData_after)

            quote_frame_table = pd.DataFrame(content, columns=col_list)

            return RET_OK, quote_frame_table


class OrderBookHandlerBase(RspHandlerBase):
    """
    异步处理推送的实时摆盘。

    .. code:: python

        class OrderBookTest(OrderBookHandlerBase):
            def on_recv_rsp(self, rsp_str):
                ret_code, data = super(OrderBookTest,self).on_recv_rsp(rsp_str)
                if ret_code != RET_OK:
                    print("OrderBookTest: error, msg: %s" % data)
                    return RET_ERROR, data

                print("OrderBookTest ", data) # OrderBookTest自己的处理逻辑

                return RET_OK, content
    """
    @classmethod
    def parse_rsp_pb(cls, rsp_pb):
        ret_code, msg, order_book = OrderBookQuery.unpack_rsp(rsp_pb)
        if ret_code != RET_OK:
            return ret_code, msg
        else:
            return RET_OK, order_book

    def on_recv_rsp(self, rsp_pb):
        """
        在收到实摆盘数据推送后会回调到该函数，使用者需要在派生类中覆盖此方法

        注意该回调是在独立子线程中

        :param rsp_pb: 派生类中不需要直接处理该参数
        :return: 参见get_order_book的返回值
        """
        ret_code, content = self.parse_rsp_pb(rsp_pb)
        if ret_code == RET_OK:
            self.on_recv_log(content)

        return ret_code, content


class CurKlineHandlerBase(RspHandlerBase):
    """
    异步处理推送的k线数据。

    .. code:: python

        class CurKlineTest(CurKlineHandlerBase):
            def on_recv_rsp(self, rsp_str):
                ret_code, data = super(CurKlineTest,self).on_recv_rsp(rsp_str)
                if ret_code != RET_OK:
                    print("CurKlineTest: error, msg: %s" % data)
                    return RET_ERROR, data

                print("CurKlineTest ", data) # CurKlineTest自己的处理逻辑

                return RET_OK, content
    """
    @classmethod
    def parse_rsp_pb(cls, rsp_pb):
        ret_code, msg, kline_list = CurKlinePush.unpack_rsp(rsp_pb)
        if ret_code != RET_OK:
            return ret_code, msg
        else:
            return RET_OK, kline_list

    def on_recv_rsp(self, rsp_pb):
        """
        在收到实时k线数据推送后会回调到该函数，使用者需要在派生类中覆盖此方法

        注意该回调是在独立子线程中

        :param rsp_pb: 派生类中不需要直接处理该参数
        :return: 参见get_cur_kline的返回值
        """
        ret_code, content = self.parse_rsp_pb(rsp_pb)
        if ret_code != RET_OK:
            return ret_code, content
        else:
            col_list = [
                'code', 'time_key', 'open', 'close', 'high', 'low', 'volume',
                'turnover', 'k_type', 'last_close'
            ]
            kline_frame_table = pd.DataFrame(content, columns=col_list)

            return RET_OK, kline_frame_table


class TickerHandlerBase(RspHandlerBase):
    """
    异步处理推送的逐笔数据。

    .. code:: python

        class TickerTest(TickerHandlerBase):
            def on_recv_rsp(self, rsp_str):
                ret_code, data = super(TickerTest,self).on_recv_rsp(rsp_str)
                if ret_code != RET_OK:
                    print("CurKlineTest: error, msg: %s" % data)
                    return RET_ERROR, data

                print("TickerTest ", data) # TickerTest自己的处理逻辑

                return RET_OK, content
    """
    @classmethod
    def parse_rsp_pb(cls, rsp_pb):
        ret_code, msg, ticker_list = TickerQuery.unpack_rsp(rsp_pb)
        if ret_code != RET_OK:
            return ret_code, msg
        else:
            return RET_OK, ticker_list

    def on_recv_rsp(self, rsp_pb):
        """
        在收到实时逐笔数据推送后会回调到该函数，使用者需要在派生类中覆盖此方法

        注意该回调是在独立子线程中

        :param rsp_pb: 派生类中不需要直接处理该参数
        :return: 参见get_rt_ticker的返回值
        """
        ret_code, content = self.parse_rsp_pb(rsp_pb)
        if ret_code != RET_OK:
            return ret_code, content
        else:
            self.on_recv_log(content)
            col_list = [
                'code', 'time', 'price', 'volume', 'turnover',
                "ticker_direction", 'sequence', 'type', 'push_data_type',
            ]
            ticker_frame_table = pd.DataFrame(content, columns=col_list)

            return RET_OK, ticker_frame_table


class RTDataHandlerBase(RspHandlerBase):
    """
    异步处理推送的分时数据。

    .. code:: python

        class RTDataTest(RTDataHandlerBase):
            def on_recv_rsp(self, rsp_str):
                ret_code, data = super(RTDataTest,self).on_recv_rsp(rsp_str)
                if ret_code != RET_OK:
                    print("RTDataTest: error, msg: %s" % data)
                    return RET_ERROR, data

                print("RTDataTest ", data) # RTDataTest自己的处理逻辑

                return RET_OK, content
    """
    @classmethod
    def parse_rsp_pb(cls, rsp_pb):
        ret_code, msg, rt_data_list = RtDataQuery.unpack_rsp(rsp_pb)
        if ret_code != RET_OK:
            return ret_code, msg
        else:
            return RET_OK, rt_data_list

    def on_recv_rsp(self, rsp_pb):
        """
        在收到实时逐笔数据推送后会回调到该函数，使用者需要在派生类中覆盖此方法

        注意该回调是在独立子线程中

        :param rsp_pb: 派生类中不需要直接处理该参数
        :return: 参见get_rt_data的返回值
        """
        ret_code, content = self.parse_rsp_pb(rsp_pb)
        if ret_code != RET_OK:
            return ret_code, content
        else:

            col_list = [
                'code', 'time', 'is_blank', 'opened_mins', 'cur_price',
                "last_close", 'avg_price', 'turnover', 'volume'
            ]
            rt_data_table = pd.DataFrame(content, columns=col_list)

            return RET_OK, rt_data_table


class BrokerHandlerBase(RspHandlerBase):
    """
    异步处理推送的经纪数据。

    .. code:: python

        class BrokerTest(BrokerHandlerBase):
            def on_recv_rsp(self, rsp_str):
                ret_code, data = super(BrokerTest,self).on_recv_rsp(rsp_str)
                if ret_code != RET_OK:
                    print("BrokerTest: error, msg: %s" % data)
                    return RET_ERROR, data

                print("BrokerTest ", data) # BrokerTest自己的处理逻辑

                return RET_OK, content
    """
    @classmethod
    def parse_rsp_pb(cls, rsp_pb):
        ret_code, msg, (stock_code, bid_content,
                        ask_content) = BrokerQueueQuery.unpack_rsp(rsp_pb)
        if ret_code != RET_OK:
            return ret_code, msg
        else:
            return RET_OK, (stock_code, bid_content, ask_content)

    def on_recv_rsp(self, rsp_pb):
        """
        在收到实时经纪数据推送后会回调到该函数，使用者需要在派生类中覆盖此方法

        注意该回调是在独立子线程中

        :param rsp_pb: 派生类中不需要直接处理该参数
        :return: 成功时返回(RET_OK, stock_code, [bid_frame_table, ask_frame_table]), 相关frame table含义见 get_broker_queue_ 的返回值说明

                 失败时返回(RET_ERROR, ERR_MSG, None)
        """
        ret_code, content = self.parse_rsp_pb(rsp_pb)
        if ret_code != RET_OK:
            return ret_code, content, None
        else:
            self.on_recv_log(content)
            stock_code, bid_content, ask_content = content
            bid_list = [
                'code', 'bid_broker_id', 'bid_broker_name', 'bid_broker_pos', 'order_id', 'order_volume'
            ]
            ask_list = [
                'code', 'ask_broker_id', 'ask_broker_name', 'ask_broker_pos', 'order_id', 'order_volume'
            ]
            bid_frame_table = pd.DataFrame(bid_content, columns=bid_list)
            ask_frame_table = pd.DataFrame(ask_content, columns=ask_list)
            return ret_code, stock_code, [bid_frame_table, ask_frame_table]


class KeepAliveHandlerBase(RspHandlerBase):
    """Base class for handling KeepAlive"""

    @classmethod
    def parse_rsp_pb(cls, rsp_pb):
        ret_code, msg, alive_time = KeepAlive.unpack_rsp(rsp_pb)
        if ret_code != RET_OK:
            return ret_code, msg
        else:
            return RET_OK, alive_time

    def on_recv_rsp(self, rsp_pb):
        """receive response callback function"""

        ret_code, content = self.parse_rsp_pb(rsp_pb)

        return ret_code, content


class SysNotifyHandlerBase(RspHandlerBase):
    """sys notify"""

    @classmethod
    def parse_rsp_pb(cls, rsp_pb):
        ret_code, content = SysNotifyPush.unpack_rsp(rsp_pb)

        return ret_code, content

    def on_recv_rsp(self, rsp_pb):
        """receive response callback function"""
        ret_code, content = self.parse_rsp_pb(rsp_pb)

        return ret_code, content

#
# class OrderDetailHandlerBase(RspHandlerBase):
#     def __init__(self):
#         super(OrderDetailHandlerBase, self).__init__()
#
#     def on_recv_rsp(self, rsp_pb):
#         """receive response callback function"""
#         ret_code, msg, data = OrderDetail.unpack_rsp(rsp_pb)
#
#         if ret_code != RET_OK:
#             return ret_code, msg
#         else:
#             return ret_code, data

class PriceReminderHandlerBase(RspHandlerBase):
    """
    异步处理推送的订阅股票的报价。

    .. code:: python

        class PriceReminderTest(PriceReminderHandlerBase):
            def on_recv_rsp(self, rsp_str):
                ret_code, content = super(PriceReminderTest,self).on_recv_rsp(rsp_str)
                if ret_code != RET_OK:
                    print("PriceReminderTest: error, msg: %s" % content)
                    return RET_ERROR, content

                print("PriceReminderTest ", content) # PriceReminderTest自己的处理逻辑

                return RET_OK, content
    """
    @classmethod
    def parse_rsp_pb(cls, rsp_pb):
        ret_code, msg, data = UpdatePriceReminder.unpack_rsp(rsp_pb)
        if ret_code != RET_OK:
            return ret_code, msg
        else:
            return RET_OK, data

    def on_recv_rsp(self, rsp_pb):
        """
        在收到实时报价推送后会回调到该函数，使用者需要在派生类中覆盖此方法

        注意该回调是在独立子线程中

        :param rsp_pb: 派生类中不需要直接处理该参数
        :return: 参见get_stock_quote的返回值
        """
        ret_code, content = self.parse_rsp_pb(rsp_pb)
        return ret_code, content