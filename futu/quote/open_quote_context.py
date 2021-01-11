# -*- coding: utf-8 -*-
"""
    Market quote and trade context setting
"""

import datetime
import math
from collections import OrderedDict
import pandas as pd
from futu.common.open_context_base import OpenContextBase, ContextStatus
from futu.quote.quote_query import *
from futu.quote.quote_stockfilter_info import *
from futu.quote.quote_get_warrant import *

class SubRecord:
    def __init__(self):
        self.subMap = {}  # (subkey, is_orderbook_detail, extended_time) => code set

    def sub(self, code_list, subtype_list, is_orderbook_detail, extended_time):
        not_is_orderbook_detail = not is_orderbook_detail
        not_extended_time = not extended_time
        for subtype in subtype_list:
            old_subkey = (subtype, not_is_orderbook_detail, not_extended_time)
            old_code_set = self.subMap.get(old_subkey, set())
            new_subkey = (subtype, is_orderbook_detail, extended_time)
            new_code_set = self.subMap.get(new_subkey, set())
            for code in code_list:
                if code in old_code_set:
                    old_code_set.remove(code)
                new_code_set.add(code)
            if len(old_code_set) == 0 and old_subkey in self.subMap:
                del self.subMap[old_subkey]
            self.subMap[new_subkey] = new_code_set

    def unsub(self, code_list, subtype_list):
        for subtype in subtype_list:
            subkey1 = (subtype, True)
            code_set1 = self.subMap.get(subkey1, set())
            subkey2 = (subtype, False)
            code_set2 = self.subMap.get(subkey2, set())
            for code in code_list:
                code_set1.discard(code)
                code_set2.discard(code)
            if len(code_set1) == 0 and subkey1 in self.subMap:
                del self.subMap[subkey1]
            if len(code_set2) == 0 and subkey2 in self.subMap:
                del self.subMap[subkey2]

    def unsub_all(self):
        self.subMap = {}

    def get_sub_list(self):
        """

        :return: [(code_list, subtype_list, is_orderbook_detail, extended_time)]
        """
        other_sub_list = []
        sublist_detail_true = []
        sublist_extend_true = []
        sublist_extend_detail_true = []
        for subkey, code_set in self.subMap.items():
            if subkey[1] and subkey[2]:
                sublist_extend_detail_true.append((subkey, code_set))
            elif subkey[1]:
                sublist_detail_true.append((subkey, code_set))
            elif subkey[2]:
                sublist_extend_true.append((subkey, code_set))
            else:
                other_sub_list.append((subkey, code_set))

        result = self._merge_sub_list(other_sub_list)
        result.extend(self._merge_sub_list(sublist_detail_true))
        result.extend(self._merge_sub_list(sublist_extend_true))
        result.extend(self._merge_sub_list(sublist_extend_detail_true))
        return result

    def _merge_sub_list(self, orig_sub_list):
        """
        将原始的订阅列表合并为适合调用subscribe函数的参数的形式，并尽量合并code列表
        :param orig_sub_list: [(subkey, code_set)]
        :return: [(code_list, subtype_list, is_orderbook_detail, extended_time)]
        """
        if len(orig_sub_list) <= 1:
            return self._conv_sub_list(orig_sub_list)

        all_code_set_same = True
        _, first_code_set = orig_sub_list[0]
        for idx in range(1, len(orig_sub_list)):
            _, cur_code_set = orig_sub_list[idx]
            if first_code_set != cur_code_set:
                all_code_set_same = False
                break
        if all_code_set_same:
            code_list = list(first_code_set)
            subtype_list = [item[0][0] for item in orig_sub_list]
            is_orderbook_detail = orig_sub_list[0][0][1]
            extended_time = orig_sub_list[0][0][2]
            return [(code_list, subtype_list, is_orderbook_detail, extended_time)]
        else:
            return self._conv_sub_list(orig_sub_list)

    def _conv_sub_list(self, orig_sub_list):
        sub_list = []
        for subkey, code_set in orig_sub_list:
            sub_list.append((list(code_set), [subkey[0]], subkey[1], subkey[2]))
        return sub_list


class OpenQuoteContext(OpenContextBase):
    """行情上下文对象类"""

    def __init__(self, host='127.0.0.1', port=11111, is_encrypt=None, is_async_connect=False):
        """
        初始化Context对象
        :param host: host地址
        :param port: 端口
        """
        self._ctx_subscribe = {}
        self._sub_record = SubRecord()
        super(OpenQuoteContext, self).__init__(
            host, port, is_async_connect, is_encrypt)

    def close(self):
        """
        关闭上下文对象。

        .. code:: python

            from futu import *
            quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
            quote_ctx.close()
        """
        super(OpenQuoteContext, self).close()

    def on_api_socket_reconnected(self):
        """for API socket reconnected"""
        # auto subscriber
        with self._lock:
            sub_list = self._sub_record.get_sub_list()

        ret_code = RET_OK
        ret_msg = ''
        for code_list, subtype_list, is_detailed_orderbook, extended_time in sub_list:
            ret_code, ret_msg = self._reconnect_subscribe(
                code_list, subtype_list, is_detailed_orderbook, extended_time)
            logger.debug("reconnect subscribe code_count={} ret_code={} ret_msg={} subtype_list={} code_list={} is_detailed_orderbook={} extended_time={}".format(
                len(code_list), ret_code, ret_msg, subtype_list, code_list, is_detailed_orderbook, extended_time))
            if ret_code != RET_OK:
                break

        # 重定阅失败，重连
        if ret_code != RET_OK:
            logger.error(
                "reconnect subscribe error, close connect and retry!!")
            self._status = ContextStatus.START
            self._wait_reconnect()
        return ret_code, ret_msg

    def get_trading_days(self, market, start=None, end=None):
        """获取交易日
        :param market: 市场类型，Market_
        :param start: 起始日期。例如'2018-01-01'。
        :param end: 结束日期。例如'2018-01-01'。
         start和end的组合如下：
         ==========    ==========    ========================================
         start类型      end类型       说明
         ==========    ==========    ========================================
         str            str           start和end分别为指定的日期
         None           str           start为end往前365天
         str            None          end为start往后365天
         None           None          end为当前日期，start为end往前365天
         ==========    ==========    ========================================
        :return: 成功时返回(RET_OK, data)，data是[{'trade_date_type': 0, 'time': '2018-01-05'}]数组；失败时返回(RET_ERROR, data)，其中data是错误描述字符串
        """
        if market is None or is_str(market) is False:
            error_str = ERROR_STR_PREFIX + "the type of market param is wrong"
            return RET_ERROR, error_str

        ret, msg, start, end = normalize_start_end_date(start, end, 365)
        if ret != RET_OK:
            return ret, msg

        query_processor = self._get_sync_query_processor(
            TradeDayQuery.pack_req, TradeDayQuery.unpack_rsp)

        # the keys of kargs should be corresponding to the actual function arguments
        kargs = {
            'market': market,
            'start_date': start,
            'end_date': end,
            'conn_id': self.get_sync_conn_id()
        }
        ret_code, msg, trade_day_list = query_processor(**kargs)

        if ret_code != RET_OK:
            return RET_ERROR, msg

        return RET_OK, trade_day_list

    def request_trading_days(self, market, start=None, end=None):
        """获取交易日
        :param market: 市场类型，TradeDateMarket_
        :param start: 起始日期。例如'2018-01-01'。
        :param end: 结束日期。例如'2018-01-01'。
         start和end的组合如下：
         ==========    ==========    ========================================
         start类型      end类型       说明
         ==========    ==========    ========================================
         str            str           start和end分别为指定的日期
         None           str           start为end往前365天
         str            None          end为start往后365天
         None           None          end为当前日期，start为end往前365天
         ==========    ==========    ========================================
        :return: 成功时返回(RET_OK, data)，data是[{'trade_date_type': 0, 'time': '2018-01-05'}]数组；失败时返回(RET_ERROR, data)，其中data是错误描述字符串
        """
        if market is None or is_str(market) is False:
            error_str = ERROR_STR_PREFIX + "the type of market param is wrong"
            return RET_ERROR, error_str

        ret, msg, start, end = normalize_start_end_date(start, end, 365)
        if ret != RET_OK:
            return ret, msg

        query_processor = self._get_sync_query_processor(
            RequestTradeDayQuery.pack_req, RequestTradeDayQuery.unpack_rsp)

        # the keys of kargs should be corresponding to the actual function arguments
        kargs = {
            'market': market,
            'start_date': start,
            'end_date': end,
            'conn_id': self.get_sync_conn_id()
        }
        ret_code, msg, trade_day_list = query_processor(**kargs)

        if ret_code != RET_OK:
            return RET_ERROR, msg

        return RET_OK, trade_day_list

    def get_stock_basicinfo(self, market, stock_type=SecurityType.STOCK, code_list=None):
        """
        获取指定市场中特定类型的股票基本信息
        :param market: 市场类型，futu.common.constant.Market
        :param stock_type: 股票类型， futu.common.constant.SecurityType
        :param code_list: 如果不为None，应该是股票code的iterable类型，将只返回指定的股票信息
        :return: (ret_code, content)
                ret_code 等于RET_OK时， content为Pandas.DataFrame数据, 否则为错误原因字符串, 数据列格式如下
            =================   ===========   ==========================================================================
            参数                  类型                        说明
            =================   ===========   ==========================================================================
            code                str            股票代码
            name                str            名字
            lot_size            int            每手数量
            stock_type          str            股票类型，参见SecurityType
            stock_child_type    str            窝轮子类型，参见WrtType
            stock_owner         str            所属正股的代码
            option_type         str            期权类型，Qot_Common.OptionType
            strike_time         str            行权日
            strike_price        float          行权价
            suspension          bool           是否停牌(True表示停牌)
            listing_date        str            上市时间
            stock_id            int            股票id
            delisting           bool           是否退市
            index_option_type   str            指数期权类型（期权特有字段）
            main_contract       bool           是否主连合约（期货特有字段）
            last_trade_time     string         最后交易时间（期货特有字段，非主连期货合约才有值）
            =================   ===========   ==========================================================================

        :example:

            .. code-block:: python

            from futu import *
            quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
            print(quote_ctx.get_stock_basicinfo(Market.HK, SecurityType.WARRANT))
            print(quote_ctx.get_stock_basicinfo(Market.US, SecurityType.DRVT, 'US.AAPL210115C185000'))
            quote_ctx.close()
        """
        if code_list is None:
            param_table = {'market': market, 'stock_type': stock_type}
            for x in param_table:
                param = param_table[x]
                if param is None or is_str(param) is False:
                    error_str = ERROR_STR_PREFIX + "the type of %s param is wrong" % x
                    return RET_ERROR, error_str
        else:
            if is_str(code_list):
                code_list = code_list.split(',')
            elif isinstance(code_list, list):
                pass
            else:
                return RET_ERROR, "code list must be like ['HK.00001', 'HK.00700'] or 'HK.00001,HK.00700'"

        code_list = unique_and_normalize_list(code_list)   # 去重

        query_processor = self._get_sync_query_processor(
            StockBasicInfoQuery.pack_req, StockBasicInfoQuery.unpack_rsp)
        kargs = {
            "market": market,
            'stock_type': stock_type,
            'code_list': code_list,
            'conn_id': self.get_sync_conn_id()
        }

        ret_code, msg, basic_info_list = query_processor(**kargs)
        if ret_code != RET_OK:
            return ret_code, msg

        col_list = [
            'code', 'name', 'lot_size', 'stock_type', 'stock_child_type', 'stock_owner',
            'option_type', 'strike_time', 'strike_price', 'suspension',
            'listing_date', 'stock_id', 'delisting', 'index_option_type',
            'main_contract', 'last_trade_time'
        ]

        basic_info_table = pd.DataFrame(basic_info_list, columns=col_list)

        return RET_OK, basic_info_table

    def request_history_kline(self,
                              code,
                              start=None,
                              end=None,
                              ktype=KLType.K_DAY,
                              autype=AuType.QFQ,
                              fields=[KL_FIELD.ALL],
                              max_count=1000,
                              page_req_key=None,
                              extended_time=False):
        """
        拉取历史k线，不需要先下载历史数据。

        :param code: 股票代码
        :param start: 开始时间，例如'2017-06-20'
        :param end:  结束时间，例如'2017-07-20'。
                  start和end的组合如下：
                     ==========    ==========    ========================================
                     start类型      end类型       说明
                     ==========    ==========    ========================================
                     str            str           start和end分别为指定的日期
                     None           str           start为end往前365天
                     str            None          end为start往后365天
                     None           None          end为当前日期，start为end往前365天
                     ==========    ==========    ========================================
        :param ktype: k线类型， 参见 KLType 定义
        :param autype: 复权类型, 参见 AuType 定义
        :param fields: 需返回的字段列表，参见 KL_FIELD 定义 KL_FIELD.ALL  KL_FIELD.OPEN ....
        :param max_count: 本次请求最大返回的数据点个数，传None表示返回start和end之间所有的数据。
        :param page_req_key: 分页请求的key。如果start和end之间的数据点多于max_count，那么后续请求时，要传入上次调用返回的page_req_key。初始请求时应该传None。
        :return: (ret, data, page_req_key)

                ret == RET_OK 返回pd dataframe数据，data.DataFrame数据, 数据列格式如下。page_req_key在分页请求时（即max_count>0）
                可能返回，并且需要在后续的请求中传入。如果没有更多数据，page_req_key返回None。

                ret != RET_OK 返回错误字符串

            =================   ===========   ==============================================================================
            参数                  类型                        说明
            =================   ===========   ==============================================================================
            code                str            股票代码
            time_key            str            k线时间
            open                float          开盘价
            close               float          收盘价
            high                float          最高价
            low                 float          最低价
            pe_ratio            float          市盈率（该字段为比例字段，默认不展示%）
            turnover_rate       float          换手率
            volume              int            成交量
            turnover            float          成交额
            change_rate         float          涨跌幅
            last_close          float          昨收价
            =================   ===========   ==============================================================================

        :note

        :example:

        .. code:: python

            from futu import *
            quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
            ret, data, page_req_key = quote_ctx.request_history_kline('HK.00700', start='2017-06-20', end='2018-06-22', max_count=50)
            print(ret, data)
            ret, data, page_req_key = quote_ctx.request_history_kline('HK.00700', start='2017-06-20', end='2018-06-22', max_count=50, page_req_key=page_req_key)
            print(ret, data)
            quote_ctx.close()
        """
        next_page_req_key = None
        ret, msg, req_start, end = normalize_start_end_date(start, end, 365)
        if ret != RET_OK:
            return ret, msg, next_page_req_key

        req_fields = unique_and_normalize_list(fields)
        if not fields:
            req_fields = copy(KL_FIELD.ALL_REAL)
        req_fields = KL_FIELD.normalize_field_list(req_fields)
        if not req_fields:
            error_str = ERROR_STR_PREFIX + "the type of fields param is wrong"
            return RET_ERROR, error_str, next_page_req_key

        if autype is None:
            autype = 'None'

        param_table = {'code': code, 'ktype': ktype, 'autype': autype}
        for x in param_table:
            param = param_table[x]
            if param is None or is_str(param) is False:
                error_str = ERROR_STR_PREFIX + "the type of %s param is wrong" % x
                return RET_ERROR, error_str, next_page_req_key

        max_kl_num = min(1000, max_count) if max_count is not None else 1000
        data_finish = False
        list_ret = []
        # 循环请求数据，避免一次性取太多超时
        while not data_finish:
            kargs = {
                "code": code,
                "start_date": req_start,
                "end_date": end,
                "ktype": ktype,
                "autype": autype,
                "fields": copy(req_fields),
                "max_num": max_kl_num,
                "conn_id": self.get_sync_conn_id(),
                "next_req_key": page_req_key,
                "extended_time": extended_time
            }
            query_processor = self._get_sync_query_processor(RequestHistoryKlineQuery.pack_req,
                                                             RequestHistoryKlineQuery.unpack_rsp)
            ret_code, msg, content = query_processor(**kargs)
            if ret_code != RET_OK:
                return ret_code, msg, next_page_req_key

            list_kline, has_next, page_req_key = content
            list_ret.extend(list_kline)
            next_page_req_key = page_req_key
            if max_count is not None:
                if max_count > len(list_ret) and has_next:
                    data_finish = False
                    max_kl_num = min(max_count - len(list_ret), 1000)
                else:
                    data_finish = True
            else:
                data_finish = not has_next

        # 表头列
        col_list = ['code']
        for field in req_fields:
            str_field = KL_FIELD.DICT_KL_FIELD_STR[field]
            if str_field not in col_list:
                col_list.append(str_field)

        kline_frame_table = pd.DataFrame(list_ret, columns=col_list)

        return RET_OK, kline_frame_table, next_page_req_key


    def get_market_snapshot(self, code_list):
        """
        获取市场快照

        :param code_list: 股票列表
        :return: (ret, data)

                ret == RET_OK 返回pd dataframe数据，data.DataFrame数据, 数据列格式如下

                ret != RET_OK 返回错误字符串

                =======================   =============   ==============================================================================
                参数                       类型                        说明
                =======================   =============   ==============================================================================
                code                       str            股票代码
                update_time                str            更新时间(yyyy-MM-dd HH:mm:ss)，（美股默认是美东时间，港股A股默认是北京时间）
                last_price                 float          最新价格
                open_price                 float          今日开盘价
                high_price                 float          最高价格
                low_price                  float          最低价格
                prev_close_price           float          昨收盘价格
                volume                     int            成交数量
                turnover                   float          成交金额
                turnover_rate              float          换手率
                suspension                 bool           是否停牌(True表示停牌)
                listing_date               str            上市日期 (yyyy-MM-dd)
                equity_valid               bool           是否正股（为true时以下正股相关字段才有合法数值）
                issued_shares              int            发行股本
                total_market_val           float          总市值
                net_asset                  int            资产净值
                net_profit                 int            净利润
                earning_per_share          float          每股盈利
                outstanding_shares         int            流通股本
                net_asset_per_share        float          每股净资产
                circular_market_val        float          流通市值
                ey_ratio                   float          收益率（该字段为比例字段，默认不展示%）
                pe_ratio                   float          市盈率（该字段为比例字段，默认不展示%）
                pb_ratio                   float          市净率（该字段为比例字段，默认不展示%）
                pe_ttm_ratio               float          市盈率TTM（该字段为比例字段，默认不展示%）
                dividend_ttm               float          股息TTM
                dividend_ratio_ttm         float          股息率TTM（该字段为百分比字段，默认不展示%）
                dividend_lfy               float          股息LFY，上一年度派息
                dividend_lfy_ratio         float          股息率LFY（该字段为百分比字段，默认不展示
                stock_owner                str            窝轮所属正股的代码或期权的标的股代码
                wrt_valid                  bool           是否是窝轮（为true时以下窝轮相关的字段才有合法数据）
                wrt_conversion_ratio       float          换股比率（该字段为比例字段，默认不展示%）
                wrt_type                   str            窝轮类型，参见WrtType
                wrt_strike_price           float          行使价格
                wrt_maturity_date          str            格式化窝轮到期时间
                wrt_end_trade              str            格式化窝轮最后交易时间
                wrt_code                   str            窝轮对应的正股（此字段已废除,修改为stock_owner）
                wrt_recovery_price         float          窝轮回收价
                wrt_street_vol             float          窝轮街货量
                wrt_issue_vol              float          窝轮发行量
                wrt_street_ratio           float          窝轮街货占比（该字段为比例字段，默认不展示%）
                wrt_delta                  float          窝轮对冲值
                wrt_implied_volatility     float          窝轮引伸波幅
                wrt_premium                float          窝轮溢价
                wrt_leverage               float          杠杆比率（倍）
                wrt_ipop                   float          价内/价外（该字段为百分比字段，默认不展示%）
                wrt_break_even_point       float          打和点
                wrt_conversion_price       float          换股价
                wrt_price_recovery_ratio   float          距收回价（该字段为百分比字段，默认不展示%）
                wrt_score                  float          综合评分
                wrt_upper_strike_price     float          上限价，仅界内证支持该字段
                wrt_lower_strike_price     float          下限价，仅界内证支持该字段
                wrt_inline_price_status    str            界内界外，仅界内证支持该字段，参见PriceType
                lot_size                   int            每手股数
                price_spread               float          当前摆盘价差亦即摆盘数据的买档或卖档的相邻档位的报价差
                ask_price                   float          卖价
                bid_price                   float          买价
                ask_vol                       float          卖量
                bid_vol                       float          买量
                enable_margin               bool              是否可融资，如果为true，后两个字段才有意义
                mortgage_ratio               float          股票抵押率（该字段为百分比字段，默认不展示%）
                long_margin_initial_ratio  float          融资初始保证金率（该字段为百分比字段，默认不展示%）
                enable_short_sell           bool              是否可卖空，如果为true，后三个字段才有意义
                short_sell_rate               float          卖空参考利率（该字段为百分比字段，默认不展示%）
                short_available_volume       int              剩余可卖空数量
                short_margin_initial_ratio float          卖空（融券）初始保证金率（该字段为百分比字段，默认不展示%
                amplitude                  float          振幅（该字段为百分比字段，默认不展示%）
                avg_price                  float          平均价
                bid_ask_ratio              float          委比（该字段为百分比字段，默认不展示%）
                volume_ratio               float          量比
                highest52weeks_price       float          52周最高价
                lowest52weeks_price        float          52周最低价
                highest_history_price      float          历史最高价
                lowest_history_price       float          历史最低价
                option_valid               bool           是否是期权（为true时以下期权相关的字段才有合法数值）
                option_type                str            期权类型，参见OptionType
                strike_time                str            行权日（美股默认是美东时间，港股A股默认是北京时间）
                option_strike_price        float          行权价
                option_contract_size       int            每份合约数
                option_open_interest       int            未平仓合约数
                option_implied_volatility  float          隐含波动率
                option_premium             float          溢价
                option_delta               float          希腊值 Delta
                option_gamma               float          希腊值 Gamma
                option_vega                float          希腊值 Vega
                option_theta               float          希腊值 Theta
                option_rho                 float          希腊值 Rho
                option_net_open_interest    int           净未平仓合约数
                option_expiry_date_distance  int          距离到期日天数
                option_contract_nominal_value  float      合约名义金额
                option_owner_lot_multiplier    float      相等正股手数，指数期权无该字段
                option_area_type           str            期权地区类型，见 OptionAreaType_
                option_contract_multiplier float          合约乘数，指数期权特有字段
                index_option_type          str            指数期权类型，见 IndexOptionType
                index_raise_count          int            指数类型上涨支数
                index_fall_count           int            指数类型下跌支数
                index_requal_count         int            指数类型平盘支数
                plate_raise_count          int            板块类型上涨支数
                plate_fall_count           int            板块类型下跌支数
                plate_equal_count          int            板块类型平盘支数
                after_volume               int            盘后成交量
                after_turnover             double         盘后成交额
                sec_status                 str            股票状态， 参见SecurityStatus
                future_valid               bool           是否期货
                future_last_settle_price   float          昨结
                future_position            float          持仓量
                future_position_change     float          日增仓
                future_main_contract       bool           是否主连合约
                future_last_trade_time     string         只有非主连期货合约才有该字段
                trust_valid                bool           是否基金
                trust_dividend_yield       float          股息率
                trust_aum                  float          资产规模
                trust_outstanding_units    int            总发行量
                trust_netAssetValue        float          单位净值
                trust_premium              float          溢价
                trust_assetClass           string         资产类别
                =======================   =============   ==============================================================================
        """
        code_list = unique_and_normalize_list(code_list)
        if not code_list:
            error_str = ERROR_STR_PREFIX + "the type of code param is wrong"
            return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            MarketSnapshotQuery.pack_req, MarketSnapshotQuery.unpack_rsp)
        kargs = {
            "stock_list": code_list,
            "conn_id": self.get_sync_conn_id()
        }

        ret_code, msg, snapshot_list = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg

        equity_col_list = ['issued_shares',
                           'total_market_val',
                           'net_asset',
                           'net_profit',
                           'earning_per_share',
                           'outstanding_shares',
                           'circular_market_val',
                           'net_asset_per_share',
                           'ey_ratio',
                           'pe_ratio',
                           'pb_ratio',
                           'pe_ttm_ratio',
                           'dividend_ttm',
                           'dividend_ratio_ttm',
                           'dividend_lfy',
                           'dividend_lfy_ratio'
                           ]
        wrt_col_list = ['wrt_conversion_ratio',
                        'wrt_type',
                        'wrt_strike_price',
                        'wrt_maturity_date',
                        'wrt_end_trade',
                        'wrt_recovery_price',
                        'wrt_street_vol',
                        'wrt_issue_vol',
                        'wrt_street_ratio',
                        'wrt_delta',
                        'wrt_implied_volatility',
                        'wrt_premium',
                        'wrt_leverage',
                        'wrt_ipop',
                        'wrt_break_even_point',
                        'wrt_conversion_price',
                        'wrt_price_recovery_ratio',
                        'wrt_score',
                        'wrt_upper_strike_price',
                        'wrt_lower_strike_price',
                        'wrt_inline_price_status',
                        'wrt_issuer_code'
                        ]
        option_col_list = ['option_type',
                           'strike_time',
                           'option_strike_price',
                           'option_contract_size',
                           'option_open_interest',
                           'option_implied_volatility',
                           'option_premium',
                           'option_delta',
                           'option_gamma',
                           'option_vega',
                           'option_theta',
                           'option_rho',
                           'option_net_open_interest',
                           'option_expiry_date_distance',
                           'option_contract_nominal_value',
                           'option_owner_lot_multiplier',
                           'option_area_type',
                           'option_contract_multiplier',
                           'index_option_type'
                           ]

        index_col_list = ['index_raise_count',
                          'index_fall_count',
                          'index_equal_count'
                          ]

        plate_col_list = ['plate_raise_count',
                          'plate_fall_count',
                          'plate_equal_count'
                          ]

        future_col_list = ['future_last_settle_price',
                           'future_position',
                           'future_position_change',
                           'future_main_contract',
                           'future_last_trade_time',
                         ]

        trust_col_list = ['trust_dividend_yield',
                          'trust_aum',
                          'trust_outstanding_units',
                          'trust_netAssetValue',
                          'trust_premium',
                          'trust_assetClass',
                        ]

        col_list = [
            'code',
            'update_time',
            'last_price',
            'open_price',
            'high_price',
            'low_price',
            'prev_close_price',
            'volume',
            'turnover',
            'turnover_rate',
            'suspension',
            'listing_date',
            'lot_size',
            'price_spread',
            'stock_owner',
            'ask_price',
            'bid_price',
            'ask_vol',
            'bid_vol',
            'enable_margin',
            'mortgage_ratio',
            'long_margin_initial_ratio',
            'enable_short_sell',
            'short_sell_rate',
            'short_available_volume',
            'short_margin_initial_ratio',
            'amplitude',
            'avg_price',
            'bid_ask_ratio',
            'volume_ratio',
            'highest52weeks_price',
            'lowest52weeks_price',
            'highest_history_price',
            'lowest_history_price',
            'close_price_5min',
            'after_volume',
            'after_turnover',
            'sec_status',
        ]

        col_dict = OrderedDict()
        col_dict.update((key, 1) for key in col_list)
        col_dict['equity_valid'] = 1
        col_dict.update((key, 1) for key in equity_col_list)
        col_dict['wrt_valid'] = 1
        col_dict.update((key, 1) for key in wrt_col_list)
        col_dict['option_valid'] = 1
        col_dict.update((key, 1) for key in option_col_list)
        col_dict['index_valid'] = 1
        col_dict.update((key, 1) for key in index_col_list)
        col_dict['plate_valid'] = 1
        col_dict.update((key, 1) for key in plate_col_list)
        col_dict['future_valid'] = 1
        col_dict.update((key, 1) for key in future_col_list)
        col_dict['trust_valid'] = 1
        col_dict.update((key, 1) for key in trust_col_list)

        col_dict.update((row[0], 1) for row in pb_field_map_PreAfterMarketData_pre)
        col_dict.update((row[0], 1) for row in pb_field_map_PreAfterMarketData_after)

        snapshot_frame_table = pd.DataFrame(snapshot_list, columns=col_dict.keys())

        return RET_OK, snapshot_frame_table

    def get_rt_data(self, code):
        """
        获取指定股票的分时数据

        :param code: 股票代码，例如，HK.00700，US.APPL
        :return: (ret, data)

                ret == RET_OK 返回pd dataframe数据，data.DataFrame数据, 数据列格式如下

                ret != RET_OK 返回错误字符串

                =====================   ===========   ==========================================================================
                参数                      类型                        说明
                =====================   ===========   ==========================================================================
                code                    str            股票代码
                time                    str            时间(yyyy-MM-dd HH:mm:ss)（美股默认是美东时间，港股A股默认是北京时间）
                is_blank                bool           数据状态；正常数据为False，伪造数据为True
                opened_mins             int            零点到当前多少分钟
                cur_price               float          当前价格
                last_close              float          昨天收盘的价格
                avg_price               float          平均价格
                volume                  float          成交量
                turnover                float          成交金额
                =====================   ===========   ==========================================================================
        """
        if code is None or is_str(code) is False:
            error_str = ERROR_STR_PREFIX + "the type of param in code is wrong"
            return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            RtDataQuery.pack_req, RtDataQuery.unpack_rsp)
        kargs = {
            "code": code,
            "conn_id": self.get_sync_conn_id()
        }

        ret_code, msg, rt_data_list = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg

        for x in rt_data_list:
            x['code'] = code

        col_list = [
            'code', 'time', 'is_blank', 'opened_mins', 'cur_price',
            'last_close', 'avg_price', 'volume', 'turnover'
        ]

        rt_data_table = pd.DataFrame(rt_data_list, columns=col_list)

        return RET_OK, rt_data_table

    def get_plate_list(self, market, plate_class):
        """
        获取板块集合下的子板块列表

        :param market: 市场标识，注意这里不区分沪，深,输入沪或者深都会返回沪深市场的子板块（这个是和客户端保持一致的）参见Market
        :param plate_class: 板块分类，参见Plate
        :return: ret == RET_OK 返回pd dataframe数据，data.DataFrame数据, 数据列格式如下

                ret != RET_OK 返回错误字符串

                =====================   ===========   ==============================================================
                参数                      类型                        说明
                =====================   ===========   ==============================================================
                code                    str            股票代码
                plate_name              str            板块名字
                plate_id                str            板块id
                =====================   ===========   ==============================================================
        """
        param_table = {'market': market, 'plate_class': plate_class}
        for x in param_table:
            param = param_table[x]
            if param is None or is_str(market) is False:
                error_str = ERROR_STR_PREFIX + "the type of market param is wrong"
                return RET_ERROR, error_str

        if not Market.if_has_key(market):
            error_str = ERROR_STR_PREFIX + "the value of market param is wrong "
            return RET_ERROR, error_str

        if not Plate.if_has_key(plate_class):
            error_str = ERROR_STR_PREFIX + "the class of plate is wrong"
            return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            SubplateQuery.pack_req, SubplateQuery.unpack_rsp)
        kargs = {
            'market': market,
            'plate_class': plate_class,
            'conn_id': self.get_sync_conn_id()
        }

        ret_code, msg, subplate_list = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg

        col_list = ['code', 'plate_name', 'plate_id']

        subplate_frame_table = pd.DataFrame(subplate_list, columns=col_list)

        return RET_OK, subplate_frame_table

    def get_plate_stock(self, plate_code, sort_field=SortField.CODE, ascend=True):
        """
        获取特定板块下的股票列表

        :param plate_code: 板块代码, string, 例如，”SH.BK0001”，”SH.BK0002”，先利用获取子版块列表函数获取子版块代码
        :param sort_field: 排序字段，string
        :param ascend: 排序方向，string，True升序，False降序
        :return: (ret, data)

                ret == RET_OK 返回pd dataframe数据，data.DataFrame数据, 数据列格式如下

                ret != RET_OK 返回错误字符串

                =====================   ===========   ==============================================================
                参数                      类型                        说明
                =====================   ===========   ==============================================================
                code                    str            股票代码
                lot_size                int            每手股数
                stock_name              str            股票名称
                stock_owner             str            所属正股的代码
                stock_child_type        str            股票子类型，参见WrtType
                stock_type              str            股票类型，参见SecurityType
                list_time               str            上市时间（美股默认是美东时间，港股A股默认是北京时间）
                stock_id                int            股票id
                main_contract           bool           是否主连合约（期货特有字段）
                last_trade_time         string         最后交易时间（期货特有字段，非主连期货合约才有值）
                =====================   ===========   ==============================================================
        """
        if plate_code is None or is_str(plate_code) is False:
            error_str = ERROR_STR_PREFIX + "the type of code is wrong"
            return RET_ERROR, error_str

        r, v = SortField.to_number(sort_field)
        if (not r):
            error_str = ERROR_STR_PREFIX + "the type of sort field is wrong"
            return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            PlateStockQuery.pack_req, PlateStockQuery.unpack_rsp)
        kargs = {
            "plate_code": plate_code,
            "sort_field": sort_field,
            "ascend": ascend,
            "conn_id": self.get_sync_conn_id()
        }

        ret_code, msg, plate_stock_list = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg

        col_list = [
            'code', 'lot_size', 'stock_name', 'stock_owner',
            'stock_child_type', 'stock_type', 'list_time', 'stock_id',
            'main_contract', 'last_trade_time'
        ]
        plate_stock_table = pd.DataFrame(plate_stock_list, columns=col_list)

        return RET_OK, plate_stock_table

    def get_broker_queue(self, code):
        """
        获取股票的经纪队列

        :param code: 股票代码
        :return: (ret, bid_frame_table, ask_frame_table)或(ret, err_message)

                ret == RET_OK 返回pd dataframe数据，数据列格式如下

                ret != RET_OK 后面两项为错误字符串

                bid_frame_table 经纪买盘数据

                =====================   ===========   ==============================================================
                参数                      类型                        说明
                =====================   ===========   ==============================================================
                code                    str             股票代码
                bid_broker_id           int             经纪买盘id
                bid_broker_name         str             经纪买盘名称
                bid_broker_pos          int             经纪档位
                order_id                int64           交易所订单id，与交易接口返回的订单id并不一样
                order_volume            int64           订单股数
                =====================   ===========   ==============================================================

                ask_frame_table 经纪卖盘数据

                =====================   ===========   ==============================================================
                参数                      类型                        说明
                =====================   ===========   ==============================================================
                code                    str             股票代码
                ask_broker_id           int             经纪卖盘id
                ask_broker_name         str             经纪卖盘名称
                ask_broker_pos          int             经纪档位
                order_id                int64           交易所订单id，与交易接口返回的订单id并不一样
                order_volume            int64           订单股数
                =====================   ===========   ==============================================================
        """
        if code is None or is_str(code) is False:
            error_str = ERROR_STR_PREFIX + "the type of param in code is wrong"
            return RET_ERROR, error_str, error_str

        query_processor = self._get_sync_query_processor(
            BrokerQueueQuery.pack_req, BrokerQueueQuery.unpack_rsp)
        kargs = {
            "code": code,
            "conn_id": self.get_sync_conn_id()
        }

        ret_code, ret_msg, content = query_processor(**kargs)
        if ret_code != RET_OK:
            return ret_code, ret_msg, ret_msg

        (_, bid_list, ask_list) = content
        col_bid_list = [
            'code', 'bid_broker_id', 'bid_broker_name', 'bid_broker_pos', 'order_id', 'order_volume'
        ]
        col_ask_list = [
            'code', 'ask_broker_id', 'ask_broker_name', 'ask_broker_pos', 'order_id', 'order_volume'
        ]

        bid_frame_table = pd.DataFrame(bid_list, columns=col_bid_list)
        ask_frame_table = pd.DataFrame(ask_list, columns=col_ask_list)
        return RET_OK, bid_frame_table, ask_frame_table

    def _check_subscribe_param(self, code_list, subtype_list):

        code_list = unique_and_normalize_list(code_list)
        subtype_list = unique_and_normalize_list(subtype_list)

        if len(code_list) == 0:
            msg = ERROR_STR_PREFIX + 'code_list is null'
            return RET_ERROR, msg, code_list, subtype_list

        if len(subtype_list) == 0:
            msg = ERROR_STR_PREFIX + 'subtype_list is null'
            return RET_ERROR, msg, code_list, subtype_list

        for subtype in subtype_list:
            if not SubType.if_has_key(subtype):
                msg = ERROR_STR_PREFIX + 'subtype is %s , which is wrong. (%s)' % (
                    subtype, SubType.get_all_keys())
                return RET_ERROR, msg, code_list, subtype_list

        for code in code_list:
            ret, msg = split_stock_str(code)
            if ret != RET_OK:
                return RET_ERROR, msg, code_list, subtype_list

        return RET_OK, "", code_list, subtype_list

    def subscribe(self, code_list, subtype_list, is_first_push=True, subscribe_push=True, is_detailed_orderbook=False, extended_time=False):
        """
        订阅注册需要的实时信息，指定股票和订阅的数据类型即可

        注意：len(code_list) * 订阅的K线类型的数量 <= 100

        :param code_list: 需要订阅的股票代码列表
        :param subtype_list: 需要订阅的数据类型列表，参见SubType
        :param is_first_push: 订阅成功后是否马上推送一次数据
        :param subscribe_push: 订阅后推送
        :param is_detailed_orderbook 是否订阅详细的摆盘订单明细，仅用于 SF 行情权限下订阅 ORDER_BOOK 类型
        :param extended_time - 是否允许美股盘前盘后数据（仅用于订阅美股实时K线、实时分时、实时逐笔），False不允许，True允许
        :return: (ret, err_message)

                ret == RET_OK err_message为None

                ret != RET_OK err_message为错误描述字符串
        :example:

        .. code:: python

        from futu import *
        quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
        print(quote_ctx.subscribe(['HK.00700'], [SubType.QUOTE)])
        quote_ctx.close()
        """
        return self._subscribe_impl(code_list, subtype_list, is_first_push, subscribe_push, is_detailed_orderbook, extended_time)

    def _subscribe_impl(self, code_list, subtype_list, is_first_push, subscribe_push=True, is_detailed_orderbook=False, extended_time=False):

        ret, msg, code_list, subtype_list = self._check_subscribe_param(
            code_list, subtype_list)
        if ret != RET_OK:
            return ret, msg

        kline_sub_count = 0
        for sub_type in subtype_list:
            if sub_type in KLINE_SUBTYPE_LIST:
                kline_sub_count += 1

        # if kline_sub_count * len(code_list) > MAX_KLINE_SUB_COUNT:
        #     return RET_ERROR, 'Too many subscription'

        query_processor = self._get_sync_query_processor(SubscriptionQuery.pack_subscribe_req,
                                                         SubscriptionQuery.unpack_subscribe_rsp)

        kargs = {
            'code_list': code_list,
            'subtype_list': subtype_list,
            'conn_id': self.get_sync_conn_id(),
            'is_first_push': is_first_push,
            'subscribe_push': subscribe_push,
            'is_detailed_orderbook': is_detailed_orderbook,
            'extended_time': extended_time
        }
        ret_code, msg, _ = query_processor(**kargs)

        if ret_code != RET_OK:
            return RET_ERROR, msg

        with self._lock:
            self._sub_record.sub(code_list, subtype_list, is_detailed_orderbook, extended_time)
        #
        # ret_code, msg, push_req_str = SubscriptionQuery.pack_push_req(
        #     code_list, subtype_list, self.get_async_conn_id(), is_first_push)
        #
        # if ret_code != RET_OK:
        #     return RET_ERROR, msg
        #
        # ret_code, msg = self._send_async_req(push_req_str)
        # if ret_code != RET_OK:
        #     return RET_ERROR, msg

        return RET_OK, None

    def _reconnect_subscribe(self, code_list, subtype_list, is_detailed_orderbook, extended_time):

        # 将k线定阅和其它定阅区分开来
        kline_sub_list = []
        other_sub_list = []
        for sub in subtype_list:
            if sub in KLINE_SUBTYPE_LIST:
                kline_sub_list.append(sub)
            else:
                other_sub_list.append(sub)

        # 连接断开时，可能会有大批股票需要重定阅，分次定阅，提高成功率
        kline_sub_one_size = 1
        if len(kline_sub_list) > 0:
            kline_sub_one_size = math.floor(100 / len(kline_sub_list))

        sub_info_list = [
            {"sub_list": kline_sub_list, "one_size":  kline_sub_one_size},
            {"sub_list": other_sub_list, "one_size": 100},
        ]

        ret_code = RET_OK
        ret_data = None

        for info in sub_info_list:
            sub_list = info["sub_list"]
            one_size = info["one_size"]
            all_count = len(code_list)
            start_idx = 0

            while start_idx < all_count and len(sub_list):
                sub_count = one_size if start_idx + \
                    one_size <= all_count else (all_count - start_idx)
                sub_codes = code_list[start_idx: start_idx + sub_count]
                start_idx += sub_count

                ret_code, ret_data = self._subscribe_impl(
                    sub_codes, sub_list, True, True, is_detailed_orderbook, extended_time)
                if ret_code != RET_OK:
                    break
            if ret_code != RET_OK:
                break

        return ret_code, ret_data

    def unsubscribe(self, code_list, subtype_list, unsubscribe_all=False):
        """
        取消订阅
        :param code_list: 取消订阅的股票代码列表
        :param subtype_list: 取消订阅的类型，参见SubType
        :return: (ret, err_message)

                ret == RET_OK err_message为None

                ret != RET_OK err_message为错误描述字符串
        """
        if not unsubscribe_all:
            ret, msg, code_list, subtype_list = self._check_subscribe_param(
                code_list, subtype_list)
            if ret != RET_OK:
                return ret, msg
        query_processor = self._get_sync_query_processor(SubscriptionQuery.pack_unsubscribe_req,
                                                         SubscriptionQuery.unpack_unsubscribe_rsp)

        kargs = {
            'code_list': code_list,
            'subtype_list': subtype_list,
            'unsubscribe_all': unsubscribe_all,
            "conn_id": self.get_sync_conn_id()
        }

        with self._lock:
            if unsubscribe_all:
                self._sub_record.unsub_all()
            else:
                self._sub_record.unsub(code_list, subtype_list)

        ret_code, msg, _ = query_processor(**kargs)

        if ret_code != RET_OK:
            return RET_ERROR, msg

        if unsubscribe_all:  # 反订阅全部别的参数不重要
            return RET_OK, None

        ret_code, msg, unpush_req_str = SubscriptionQuery.pack_unpush_req(
            code_list, subtype_list, self.get_async_conn_id())
        if ret_code != RET_OK:
            return RET_ERROR, msg

        ret_code, msg = self._send_async_req(unpush_req_str)
        if ret_code != RET_OK:
            return RET_ERROR, msg

        return RET_OK, None

    def unsubscribe_all(self):
        return self.unsubscribe(None, None, True)

    def query_subscription(self, is_all_conn=True):
        """
        查询已订阅的实时信息

        :param is_all_conn: 是否返回所有连接的订阅状态,不传或者传False只返回当前连接数据
        :return: (ret, data)

                ret != RET_OK 返回错误字符串

                ret == RET_OK 返回 定阅信息的字典数据 ，格式如下:

                {
                    'total_used': 4,    # 所有连接已使用的定阅额度

                    'own_used': 0,       # 当前连接已使用的定阅额度

                    'remain': 496,       #  剩余的定阅额度

                    'sub_list':          #  每种定阅类型对应的股票列表

                    {
                        'BROKER': ['HK.00700', 'HK.02318'],

                        'RT_DATA': ['HK.00700', 'HK.02318']
                    }
                }
        """
        is_all_conn = bool(is_all_conn)
        query_processor = self._get_sync_query_processor(
            SubscriptionQuery.pack_subscription_query_req,
            SubscriptionQuery.unpack_subscription_query_rsp)
        kargs = {
            "is_all_conn": is_all_conn,
            "conn_id": self.get_sync_conn_id()
        }

        ret_code, msg, sub_table = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg

        ret_dict = {}
        ret_dict['total_used'] = sub_table['total_used']
        ret_dict['remain'] = sub_table['remain']
        ret_dict['own_used'] = 0
        ret_dict['sub_list'] = {}
        for conn_sub in sub_table['conn_sub_list']:

            is_own_conn = conn_sub['is_own_conn']
            if is_own_conn:
                ret_dict['own_used'] = conn_sub['used']
            if not is_all_conn and not is_own_conn:
                continue

            for sub_info in conn_sub['sub_list']:
                subtype = sub_info['subtype']

                if subtype not in ret_dict['sub_list']:
                    ret_dict['sub_list'][subtype] = []
                code_list = ret_dict['sub_list'][subtype]

                for code in sub_info['code_list']:
                    if code not in code_list:
                        code_list.append(code)

        return RET_OK, ret_dict

    def get_stock_quote(self, code_list):
        """
        获取订阅股票报价的实时数据，有订阅要求限制。

        对于异步推送，参见StockQuoteHandlerBase

        :param code_list: 股票代码列表，必须确保code_list中的股票均订阅成功后才能够执行
        :return: (ret, data)

                ret == RET_OK 返回pd dataframe数据，数据列格式如下

                ret != RET_OK 返回错误字符串

                =====================   ===========   ==============================================================
                参数                      类型                        说明
                =====================   ===========   ==============================================================
                code                    str            股票代码
                data_date               str            日期
                data_time               str            时间（美股默认是美东时间，港股A股默认是北京时间）
                last_price              float          最新价格
                open_price              float          今日开盘价
                high_price              float          最高价格
                low_price               float          最低价格
                prev_close_price        float          昨收盘价格
                volume                  int            成交数量
                turnover                float          成交金额
                turnover_rate           float          换手率
                amplitude               int            振幅
                suspension              bool           是否停牌(True表示停牌)
                listing_date            str            上市日期 (yyyy-MM-dd)
                price_spread            float          当前价差，亦即摆盘数据的买档或卖档的相邻档位的报价差
                dark_status             str            暗盘交易状态，见DarkStatus
                sec_status              str            股票状态，见SecurityStatus
                strike_price            float          行权价
                contract_size           int            每份合约数
                open_interest           int            未平仓合约数
                implied_volatility      float          隐含波动率
                premium                 float          溢价
                delta                   float          希腊值 Delta
                gamma                   float          希腊值 Gamma
                vega                    float          希腊值 Vega
                theta                   float          希腊值 Theta
                rho                     float          希腊值 Rho
                net_open_interest       int            净未平仓合约数
                expiry_date_distance    int            距离到期日天数
                contract_nominal_value  float          合约名义金额
                owner_lot_multiplier    float          相等正股手数，指数期权无该字段
                option_area_type        str            期权地区类型，见 OptionAreaType_
                contract_multiplier     float          合约乘数，指数期权特有字段
                last_settle_price       float          昨结，期货特有字段
                position                float          持仓量，期货特有字段
                position_change         float          日增仓，期货特有字段
                index_option_type       str            指数期权的类型，仅在指数期权有效
                =====================   ===========   ==============================================================
        """
        code_list = unique_and_normalize_list(code_list)
        if not code_list:
            error_str = ERROR_STR_PREFIX + "the type of code_list param is wrong"
            return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            StockQuoteQuery.pack_req,
            StockQuoteQuery.unpack_rsp,
        )
        kargs = {
            "stock_list": code_list,
            "conn_id": self.get_sync_conn_id()
        }

        ret_code, msg, quote_list = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg

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

        quote_frame_table = pd.DataFrame(quote_list, columns=col_list)

        return RET_OK, quote_frame_table

    def get_rt_ticker(self, code, num=500):
        """
        获取指定股票的实时逐笔。取最近num个逐笔

        :param code: 股票代码
        :param num: 最近ticker个数(有最大个数限制，最近1000个）
        :return: (ret, data)

                ret == RET_OK 返回pd dataframe数据，数据列格式如下

                ret != RET_OK 返回错误字符串

                =====================   ===========   ==============================================================
                参数                      类型                        说明
                =====================   ===========   ==============================================================
                code                     str            股票代码
                sequence                 int            逐笔序号
                time                     str            成交时间（美股默认是美东时间，港股A股默认是北京时间）
                price                    float          成交价格
                volume                   int            成交数量（股数）
                turnover                 float          成交金额
                ticker_direction         str            逐笔方向
                type                    str             逐笔类型，参见TickerType
                =====================   ===========   ==============================================================
        """

        if code is None or is_str(code) is False:
            error_str = ERROR_STR_PREFIX + "the type of code param is wrong"
            return RET_ERROR, error_str

        if num is None or isinstance(num, int) is False:
            error_str = ERROR_STR_PREFIX + "the type of num param is wrong"
            return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            TickerQuery.pack_req,
            TickerQuery.unpack_rsp,
        )
        kargs = {
            "code": code,
            "num": num,
            "conn_id": self.get_sync_conn_id()
        }
        ret_code, msg, ticker_list = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg

        col_list = [
            'code', 'time', 'price', 'volume', 'turnover', "ticker_direction",
            'sequence', 'type'
        ]
        ticker_frame_table = pd.DataFrame(ticker_list, columns=col_list)

        return RET_OK, ticker_frame_table

    def get_cur_kline(self, code, num, ktype=SubType.K_DAY, autype=AuType.QFQ):
        """
        实时获取指定股票最近num个K线数据，最多1000根

        :param code: 股票代码
        :param num:  k线数据个数
        :param ktype: k线类型，参见KLType
        :param autype: 复权类型，参见AuType
        :return: (ret, data)

                ret == RET_OK 返回pd dataframe数据，数据列格式如下

                ret != RET_OK 返回错误字符串

                =====================   ===========   ==============================================================
                参数                      类型                        说明
                =====================   ===========   ==============================================================
                code                     str            股票代码
                time_key                 str            时间（美股默认是美东时间，港股A股默认是北京时间）
                open                     float          开盘价
                close                    float          收盘价
                high                     float          最高价
                low                      float          最低价
                volume                   int            成交量
                turnover                 float          成交额
                pe_ratio                 float          市盈率（该字段为比例字段，默认不展示%）
                turnover_rate            float          换手率
                =====================   ===========   ==============================================================
        """
        param_table = {'code': code, 'ktype': ktype}
        for x in param_table:
            param = param_table[x]
            if param is None or is_str(param) is False:
                error_str = ERROR_STR_PREFIX + "the type of %s param is wrong" % x
                return RET_ERROR, error_str

        if num is None or isinstance(num, int) is False:
            error_str = ERROR_STR_PREFIX + "the type of num param is wrong"
            return RET_ERROR, error_str

        if autype is not None and is_str(autype) is False:
            error_str = ERROR_STR_PREFIX + "the type of autype param is wrong"
            return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            CurKlineQuery.pack_req,
            CurKlineQuery.unpack_rsp,
        )

        kargs = {
            "code": code,
            "num": num,
            "ktype": ktype,
            "autype": autype,
            "conn_id": self.get_sync_conn_id()
        }
        ret_code, msg, kline_list = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg

        col_list = [
            'code', 'time_key', 'open', 'close', 'high', 'low', 'volume',
            'turnover', 'pe_ratio', 'turnover_rate', 'last_close'
        ]
        kline_frame_table = pd.DataFrame(kline_list, columns=col_list)

        return RET_OK, kline_frame_table

    def get_order_book(self, code, num = 10):
        """
        获取实时摆盘数据

        :param code: 股票代码
        :param num: 请求摆盘档数，LV2行情用户最多可以获取10档，SF行情用户最多可以获取40档
        :return: (ret, data)

                ret == RET_OK 返回字典，数据格式如下

                ret != RET_OK 返回错误字符串

                {‘code’: 股票代码
                ‘Ask’:[ (ask_price1, ask_volume1, order_num, {order_id1:order_volume1,…}), (ask_price2, ask_volume2, order_num, {order_id1:order_volume1,…}),…]
                ‘Bid’: [ (bid_price1, bid_volume1, order_num, {order_id1:order_volume1,…}), (bid_price2, bid_volume2, order_num, {order_id1:order_volume1,…}),…]
                }

                'Ask'：卖盘， 'Bid'买盘。每个元组的含义是(委托价格，委托数量，委托订单数)
        """
        if code is None or is_str(code) is False:
            error_str = ERROR_STR_PREFIX + "the type of code param is wrong"
            return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            OrderBookQuery.pack_req,
            OrderBookQuery.unpack_rsp,
        )

        kargs = {
            "code": code,
            "num": num,
            "conn_id": self.get_sync_conn_id()
        }
        ret_code, msg, orderbook = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg

        return RET_OK, orderbook

    def get_referencestock_list(self, code, reference_type):
        """
        获取证券的关联数据
        :param code: 证券id，str，例如HK.00700
        :param reference_type: 要获得的相关数据，参见SecurityReferenceType。例如WARRANT，表示获取正股相关的窝轮
        :return: (ret, data)

                ret == RET_OK 返回pd dataframe数据，数据列格式如下

                ret != RET_OK 返回错误字符串
                =======================   ===========   ==============================================================================
                参数                        类型                        说明
                =======================   ===========   ==============================================================================
                code                        str           证券代码
                lot_size                    int           每手数量
                stock_type                  str           证券类型，参见SecurityType
                stock_name                  str           证券名字
                list_time                   str           上市时间（美股默认是美东时间，港股A股默认是北京时间）
                wrt_valid                   bool          是否是窝轮，如果为True，下面wrt开头的字段有效
                wrt_type                    str           窝轮类型，参见WrtType
                wrt_code                    str           所属正股
                future_valid                bool          是否是期货，如果为True，下面future开头的字段有效
                future_main_contract        bool          是否主连合约（期货特有字段）
                future_last_trade_time      string        最后交易时间（期货特有字段，非主连期货合约才有值）
                =======================   ===========   ==============================================================================

        """
        if code is None or is_str(code) is False:
            error_str = ERROR_STR_PREFIX + "the type of code param is wrong"
            return RET_ERROR, error_str


        if reference_type is not None and not SecurityReferenceType.if_has_key(reference_type):
            error_str = ERROR_STR_PREFIX + "the type of reference_type param is wrong"
            return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            StockReferenceList.pack_req,
            StockReferenceList.unpack_rsp,
        )

        kargs = {
            "code": code,
            'ref_type': reference_type,
            "conn_id": self.get_sync_conn_id()
        }
        ret_code, msg, data_list = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg

        col_list = [
            'code', 'lot_size', 'stock_type', 'stock_name', 'list_time', 'wrt_valid', 'wrt_type', 'wrt_code',
            'future_valid','future_main_contract','future_last_trade_time'
        ]

        pd_frame = pd.DataFrame(data_list, columns=col_list)
        return RET_OK, pd_frame

    def get_owner_plate(self, code_list):
        """
        获取单支或多支股票的所属板块信息列表

        :param code_list: 股票代码列表，仅支持正股、指数。list或str。例如：['HK.00700', 'HK.00001']或者'HK.00700,HK.00001'。
        :return: (ret, data)

                ret == RET_OK 返回pd dataframe数据，data.DataFrame数据, 数据列格式如下

                ret != RET_OK 返回错误字符串

                =====================   ===========   ==============================================================
                参数                      类型                        说明
                =====================   ===========   ==============================================================
                code                    str            证券代码
                plate_code              str            板块代码
                plate_name              str            板块名字
                plate_type              str            板块类型（行业板块或概念板块），futu.common.constant.Plate
                =====================   ===========   ==============================================================
        """
        if is_str(code_list):
            code_list = code_list.split(',')
        elif isinstance(code_list, list):
            pass
        else:
            return RET_ERROR, "code list must be like ['HK.00001', 'HK.00700'] or 'HK.00001,HK.00700'"

        code_list = unique_and_normalize_list(code_list)
        if not code_list:
            error_str = ERROR_STR_PREFIX + "the type of code param is wrong"
            return RET_ERROR, error_str

        for code in code_list:
            if code is None or is_str(code) is False:
                error_str = ERROR_STR_PREFIX + "the type of param in code_list is wrong"
                return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            OwnerPlateQuery.pack_req, OwnerPlateQuery.unpack_rsp)
        kargs = {
            "code_list": code_list,
            "conn_id": self.get_sync_conn_id()
        }

        ret_code, msg, owner_plate_list = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg

        col_list = [
            'code', 'plate_code', 'plate_name', 'plate_type'
        ]

        owner_plate_table = pd.DataFrame(owner_plate_list, columns=col_list)

        return RET_OK, owner_plate_table

    def get_holding_change_list(self, code, holder_type, start=None, end=None):
        """
        获取大股东持股变动列表,只提供美股数据

        :param code: 股票代码. 例如：'US.AAPL'
        :param holder_type: 持有者类别，StockHolder_
        :param start: 开始时间. 例如：'2016-10-01'
        :param end: 结束时间，例如：'2017-10-01'。
            start与end的组合如下：
            ==========    ==========    ========================================
             start类型      end类型       说明
            ==========    ==========    ========================================
             str            str           start和end分别为指定的日期
             None           str           start为end往前365天
             str            None          end为start往后365天
             None           None          end为当前日期，start为end往前365天
            ==========    ==========    ========================================

        :return: (ret, data)

                ret == RET_OK 返回pd dataframe数据，data.DataFrame数据, 数据列格式如下

                ret != RET_OK 返回错误字符串

                =====================   ===========   ==============================================================
                参数                      类型                        说明
                =====================   ===========   ==============================================================
                holder_name             str            高管名称
                holding_qty             float          持股数
                holding_ratio           float          持股比例（该字段为比例字段，默认不展示%）
                change_qty              float          变动数
                change_ratio            float          变动比例（该字段为比例字段，默认不展示%）
                time                    str            发布时间（美股的时间默认是美东）
                =====================   ===========   ==============================================================
        """
        
        if code is None or is_str(code) is False:
            msg = ERROR_STR_PREFIX + "the type of code param is wrong"
            return RET_ERROR, msg

        r, holder_type_number = StockHolder.to_number(holder_type)
        if holder_type is None or not r:
            msg = ERROR_STR_PREFIX + "the type {0} is wrong".format(holder_type)
            return RET_ERROR, msg

        ret_code, msg, start, end = normalize_start_end_date(
            start, end, delta_days=365)
        if ret_code != RET_OK:
            return ret_code, msg

        query_processor = self._get_sync_query_processor(
            HoldingChangeList.pack_req, HoldingChangeList.unpack_rsp)
        kargs = {
            "code": code,
            "holder_type": holder_type_number,
            "conn_id": self.get_sync_conn_id(),
            "start_date": start,
            "end_date": end
        }

        ret_code, msg, owner_plate_list = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg

        col_list = [
            'holder_name', 'holding_qty', 'holding_ratio', 'change_qty', 'change_ratio', 'time'
        ]

        holding_change_list = pd.DataFrame(owner_plate_list, columns=col_list)

        return RET_OK, holding_change_list

    def get_option_chain(self, code, index_option_type=IndexOptionType.NORMAL, start=None, end=None, option_type=OptionType.ALL, option_cond_type=OptionCondType.ALL, data_filter = None):
        """
        通过标的股查询期权

        :param code: 股票代码,例如：'HK.02318'
        :param index_option_type: 指数期权类型，IndexOptionType
        :param start: 开始日期，该日期指到期日，例如'2017-08-01'
        :param end: 结束日期（包括这一天），该日期指到期日，例如'2017-08-30'。 注意，时间范围最多30天
                start和end的组合如下：
                ==========    ==========    ========================================
                 start类型      end类型       说明
                ==========    ==========    ========================================
                 str            str           start和end分别为指定的日期
                 None           str           start为end往前30天
                 str            None          end为start往后30天
                 None           None          start为当前日期，end往后30天
                ==========    ==========    ========================================
        :param option_type: 期权类型,默认全部，全部/看涨/看跌，futu.common.constant.OptionType
        :param option_cond_type: 默认全部，全部/价内/价外，futu.common.constant.OptionCondType
        :param data_filter: 数据筛选条件，默认不筛选，参考OptionDataFilter,
                OptionDataFilter字段如下：
                ============================    ==========    ========================================
                 字段                            类型           说明
                ============================    ==========    ========================================
                 implied_volatility_min         float          隐含波动率过滤起点 %
                 implied_volatility_max         float          隐含波动率过滤终点 %
                 delta_min                      float          希腊值 Delta过滤起点
                 delta_max                      float          希腊值 Delta过滤终点
                 gamma_min                      float          希腊值 Gamma过滤起点
                 gamma_max                      float          希腊值 Gamma过滤终点
                 vega_min                       float          希腊值 Vega过滤起点
                 vega_max                       float          希腊值 Vega过滤终点
                 theta_min                      float          希腊值 Theta过滤起点
                 theta_max                      float          希腊值 Theta过滤终点
                 rho_min                        float          希腊值 Rho过滤起点
                 rho_max                        float          希腊值 Rho过滤终点
                 net_open_interest_min          float          净未平仓合约数过滤起点
                 net_open_interest_max          float          净未平仓合约数过滤终点
                 open_interest_min              float          未平仓合约数过滤起点
                 open_interest_max              float          未平仓合约数过滤终点
                 vol_min                        float          成交量过滤起点
                 vol_max                        float          成交量过滤终点
                ============================    ==========    ========================================
        :return: (ret, data)

                ret == RET_OK 返回pd dataframe数据，数据列格式如下

                ret != RET_OK 返回错误字符串

                ==================   ===========   ==============================================================
                参数                      类型                        说明
                ==================   ===========   ==============================================================
                code                 str           股票代码
                name                 str           名字
                lot_size             int           每手数量
                stock_type           str           股票类型，参见SecurityType
                option_type          str           期权类型，Qot_Common.OptionType
                stock_owner          str           标的股
                strike_time          str           行权日（美股默认是美东时间，港股A股默认是北京时间）
                strike_price         float         行权价
                suspension           bool          是否停牌(True表示停牌)
                stock_id             int           股票id
                index_option_type    str           指数期权类型
                ==================   ===========   ==============================================================

        """

        if code is None or is_str(code) is False:
            error_str = ERROR_STR_PREFIX + "the type of code param is wrong"
            return RET_ERROR, error_str

        r, n = IndexOptionType.to_number(index_option_type)
        if r is False:
            msg = ERROR_STR_PREFIX + "the type of index_option_type param is wrong"
            return RET_ERROR, msg

        if data_filter is not None and not isinstance(data_filter, OptionDataFilter):
            msg = ERROR_STR_PREFIX + "the type of data_filter param is wrong"
            return RET_ERROR, msg

        if not OptionType.if_has_key(option_type):
            msg = ERROR_STR_PREFIX + "the type of option_type param is wrong"
            return RET_ERROR, msg

        if not OptionCondType.if_has_key(option_cond_type):
            msg = ERROR_STR_PREFIX + "the type of option_cond_type param is wrong"
            return RET_ERROR, msg

        ret_code, msg, start, end = normalize_start_end_date(
            start, end, delta_days=29, default_time_end='00:00:00', prefer_end_now=False)
        if ret_code != RET_OK:
            return ret_code, msg

        query_processor = self._get_sync_query_processor(
            OptionChain.pack_req, OptionChain.unpack_rsp)
        kargs = {
            "code": code,
            "index_option_type": index_option_type,
            "conn_id": self.get_sync_conn_id(),
            "start_date": start,
            "end_date": end,
            "option_cond_type": option_cond_type,
            "option_type": option_type,
            "data_filter": data_filter
        }

        ret_code, msg, option_chain_list = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg

        col_list = [
            'code', 'name', 'lot_size', 'stock_type',
            'option_type', 'stock_owner', 'strike_time', 'strike_price', 'suspension',
            'stock_id', 'index_option_type'
        ]

        option_chain = pd.DataFrame(option_chain_list, columns=col_list)

        option_chain.sort_values(
            by=["strike_time", "strike_price"], axis=0, ascending=True, inplace=True)
        option_chain.index = range(len(option_chain))

        return RET_OK, option_chain

    def get_order_detail(self, code):
        return RET_ERROR, "this service has been cancelled"

        """
        查询A股Level 2权限下提供的委托明细

        :param code: 股票代码,例如：'HK.02318'
        :return: (ret, data)

                ret == RET_OK data为1个dict，包含以下数据

                ret != RET_OK data为错误字符串

                {‘code’: 股票代码
                ‘Ask’:[ order_num, [order_volume1, order_volume2] ]
                ‘Bid’: [ order_num, [order_volume1, order_volume2] ]
                }

                'Ask'：卖盘， 'Bid'买盘。order_num指委托订单数量，order_volume是每笔委托的委托量，当前最多返回前50笔委托的委托数量。即order_num有可能多于后面的order_volume
        """

        if code is None or is_str(code) is False:
            error_str = ERROR_STR_PREFIX + "the type of code param is wrong"
            return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            OrderDetail.pack_req, OrderDetail.unpack_rsp)
        kargs = {
            "code": code,
            "conn_id": self.get_sync_conn_id()
        }

        ret_code, msg, order_detail = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg

        return RET_OK, order_detail

    def get_warrant(self, stock_owner='', req=None):
        """
        :param stock_owner:所属正股
        :param req:futu.quote.quote_get_warrant.Request
        """


        if (req is None) or (not isinstance(req, Request)):
            req = Request()

        if stock_owner is Market.HK:
            stock_owner = ''

        if stock_owner is not None:
            req.stock_owner = stock_owner

        r, v = SortField.to_number(req.sort_field)
        if not r:
            return RET_ERROR, 'sort_field is wrong. must be SortField'

        query_processor = self._get_sync_query_processor(
            QuoteWarrant.pack_req, QuoteWarrant.unpack_rsp)
        kargs = {
            "req": req,
            "conn_id": self.get_sync_conn_id()
        }
        ret_code, msg, content = query_processor(**kargs)
        if ret_code != RET_OK:
            return ret_code, msg
        else:
            warrant_data_list, last_page, all_count = content
            col_list = ['stock', 'name', 'stock_owner', 'type', 'issuer', 'maturity_time',
                        'list_time', 'last_trade_time', 'recovery_price', 'conversion_ratio',
                        'lot_size', 'strike_price', 'last_close_price', 'cur_price', 'price_change_val', 'change_rate',
                        'status', 'bid_price', 'ask_price', 'bid_vol', 'ask_vol', 'volume', 'turnover', 'score',
                        'premium', 'break_even_point', 'leverage', 'ipop', 'price_recovery_ratio', 'conversion_price',
                        'street_rate', 'street_vol', 'amplitude', 'issue_size', 'high_price', 'low_price',
                        'implied_volatility', 'delta', 'effective_leverage', 'list_timestamp',  'last_trade_timestamp',
                        'maturity_timestamp', 'upper_strike_price', 'lower_strike_price', 'inline_price_status']
            warrant_data_frame = pd.DataFrame(
                warrant_data_list, columns=col_list)
            # 1120400921001028854
            return ret_code, (warrant_data_frame, last_page, all_count)

    def get_history_kl_quota(self, get_detail=False):
        """拉取历史K线已经用掉的额度"""
        # self.get_login_user_id()
        query_processor = self._get_sync_query_processor(
            HistoryKLQuota.pack_req, HistoryKLQuota.unpack_rsp)
        kargs = {
            "get_detail": get_detail,
            "conn_id": self.get_sync_conn_id()
        }
        ret_code, msg, data = query_processor(**kargs)
        if ret_code != RET_OK:
            return ret_code, msg
        else:
            used_quota = data["used_quota"]
            remain_quota = data["remain_quota"]
            detail_list = data["detail_list"]
            return ret_code, (used_quota, remain_quota, detail_list)

    def get_rehab(self, code):
        """获取除权信息"""

        """
        获取给定股票列表的复权因子

        :param code_list: 股票列表，例如['HK.00700']
        :return: (ret, data)

                ret == RET_OK 返回pd dataframe数据，data.DataFrame数据, 数据列格式如下

                ret != RET_OK 返回错误字符串

                =====================   ===========   =================================================================================
                参数                      类型                        说明
                =====================   ===========   =================================================================================
                ex_div_date             str            除权除息日
                split_ratio             float          拆合股比例（该字段为比例字段，默认不展示%），例如，对于5股合1股为1/5，对于1股拆5股为5/1
                per_cash_div            float          每股派现
                per_share_div_ratio     float          每股送股比例（该字段为比例字段，默认不展示%）
                per_share_trans_ratio   float          每股转增股比例（该字段为比例字段，默认不展示%）
                allotment_ratio         float          每股配股比例（该字段为比例字段，默认不展示%）
                allotment_price         float          配股价
                stk_spo_ratio           float          增发比例（该字段为比例字段，默认不展示%）
                stk_spo_price           float          增发价格
                forward_adj_factorA     float          前复权因子A
                forward_adj_factorB     float          前复权因子B
                backward_adj_factorA    float          后复权因子A
                backward_adj_factorB    float          后复权因子B
                =====================   ===========   =================================================================================
        """
        query_processor = self._get_sync_query_processor(
            RequestRehab.pack_req, RequestRehab.unpack_rsp)
        kargs = {
            "stock": code,
            "conn_id": self.get_sync_conn_id()
        }
        ret_code, msg, data = query_processor(**kargs)
        if ret_code != RET_OK:
            return ret_code, msg
        else:
            col_list = [
                'ex_div_date', 'split_ratio', 'per_cash_div',
                'per_share_div_ratio', 'per_share_trans_ratio', 'allotment_ratio',
                'allotment_price', 'stk_spo_ratio', 'stk_spo_price',
                'forward_adj_factorA', 'forward_adj_factorB',
                'backward_adj_factorA', 'backward_adj_factorB'
            ]
            exr_frame_table = pd.DataFrame(data, columns=col_list)
            return ret_code, exr_frame_table

    def get_user_info(self, info_field=[]):
        """获取用户信息（内部保留函数）"""
        query_processor = self._get_sync_query_processor(
            GetUserInfo.pack_req, GetUserInfo.unpack_rsp)
        kargs = {
            "info_field": info_field,
            "conn_id": self.get_sync_conn_id()
        }
        ret_code, msg, data = query_processor(**kargs)
        if ret_code != RET_OK:
            return ret_code, msg
        else:
            return ret_code, data

    def get_capital_distribution(self, stock_code):
        """
        个股资金分布
        GetCapitalDistribution
        """
        if stock_code is None or is_str(stock_code) is False:
            error_str = ERROR_STR_PREFIX + 'the type of stock_code param is wrong'
            return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            GetCapitalDistributionQuery.pack_req,
            GetCapitalDistributionQuery.unpack,
        )

        kargs = {
            "code": stock_code,
            "conn_id": self.get_sync_conn_id()
        }
        ret_code, msg, ret = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg
        if isinstance(ret, dict):
            col_list = [
                'capital_in_big',
                'capital_in_mid',
                'capital_in_small',
                'capital_out_big',
                'capital_out_mid',
                'capital_out_small',
                'update_time',
            ]
            ret_frame = pd.DataFrame(ret, columns=col_list, index=[0])
            return RET_OK, ret_frame
        else:
            return RET_ERROR, "empty data"

    def get_capital_flow(self, stock_code):
        """
        个股资金流入流出
        GetCapitalFlow
        """
        if stock_code is None or is_str(stock_code) is False:
            error_str = ERROR_STR_PREFIX + 'the type of stock_code param is wrong'
            return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            GetCapitalFlowQuery.pack_req,
            GetCapitalFlowQuery.unpack,
        )

        kargs = {
            "code": stock_code,
            "conn_id": self.get_sync_conn_id()
        }
        ret_code, msg, ret = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg
        if isinstance(ret, list):
            col_list = [
                'last_valid_time',
                'in_flow',
                'capital_flow_item_time',
            ]
            ret_frame = pd.DataFrame(ret, columns=col_list)
            return RET_OK, ret_frame
        else:
            return RET_ERROR, "empty data"

    def verification(self, verification_type=VerificationType.NONE, verification_op=VerificationOp.NONE, code=""):
        """图形验证码下载之后会将其存至固定路径，请到该路径下查看验证码
        Windows平台：%appdata%/com.futunn.FutuOpenD/F3CNN/PicVerifyCode.png
        非Windows平台：~/.com.futunn.FutuOpenD/F3CNN/PicVerifyCode.png
        注意：只有最后一次请求验证码会生效，重复请求只有最后一次的验证码有效"""

        """required int32 type = 1; //验证码类型, VerificationType
        required int32 op = 2; //操作, VerificationOp
        optional string code = 3; //验证码，请求验证码时忽略该字段，输入时必填"""

        query_processor = self._get_sync_query_processor(
            Verification.pack_req, Verification.unpack_rsp)
        kargs = {
            "verification_type": verification_type,
            "verification_op": verification_op,
            "code": code,
            "conn_id": self.get_sync_conn_id()
        }
        ret_code, msg, data = query_processor(**kargs)
        if ret_code != RET_OK:
            return ret_code, msg
        else:
            return ret_code, data

    def get_delay_statistics(self, type_list, qot_push_stage, segment_list):
        """
        GetDelayStatistics
        qot_push_stage 行情推送统计的区间，行情推送统计时有效，QotPushStage
        type_list 统计数据类型，DelayStatisticsType [DelayStatisticsType.QOT_PUSH, DelayStatisticsType.REQ_REPLY]
        check segment_list 统计分段，默认100ms以下以2ms分段，100ms以上以500，1000，2000，-1分段，-1表示无穷大。
        """

        query_processor = self._get_sync_query_processor(
            GetDelayStatisticsQuery.pack_req,
            GetDelayStatisticsQuery.unpack,
        )

        kargs = {
            "type_list": type_list,
            "qot_push_stage": qot_push_stage,
            "segment_list": segment_list,
            "conn_id": self.get_sync_conn_id()
        }
        ret_code, msg, ret = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg
        if isinstance(ret, dict):
            ret_dic = dict()
            ret_dic["qot_push"] = ret["qot_push_all_statistics_list"]
            ret_dic["req_reply"] = ret["req_reply_statistics_list"]
            ret_dic["place_order"] = ret["place_order_statistics_list"]
            return RET_OK, ret_dic
        else:
            return RET_ERROR, "empty data"

    def modify_user_security(self, group_name, op, code_list):
        """
        ModifyUserSecurity
        修改用户自选股列表信息
        """
        if is_str(code_list):
            code_list = code_list.split(',')
        elif isinstance(code_list, list):
            pass
        else:
            return RET_ERROR, "code list must be like ['HK.00001', 'HK.00700'] or 'HK.00001,HK.00700'"
        code_list = unique_and_normalize_list(code_list)
        for code in code_list:
            if code is None or is_str(code) is False:
                error_str = ERROR_STR_PREFIX + "the type of param in code_list is wrong"
                return RET_ERROR, error_str

        ret, op_value = ModifyUserSecurityOp.to_number(op)
        if ret is not True:
            return RET_ERROR, op_value

        query_processor = self._get_sync_query_processor(
            ModifyUserSecurityQuery.pack_req,
            ModifyUserSecurityQuery.unpack,
        )

        kargs = {
            "group_name": group_name,
            "op": op_value,
            "code_list": code_list,
            "conn_id": self.get_sync_conn_id()
        }
        ret_code, msg, ret = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg
        else:
            return RET_OK, "success"

    def get_user_security(self, group_name):
        """
        GetUserSecurity
        """
        if not isinstance(group_name, str):
            return RET_ERROR, "group_name need str"

        query_processor = self._get_sync_query_processor(
            GetUserSecurityQuery.pack_req,
            GetUserSecurityQuery.unpack,
        )

        kargs = {
            "group_name": group_name,
            "conn_id": self.get_sync_conn_id()
        }
        ret_code, msg, ret = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg
        if isinstance(ret, list):
            col_list = [
                'code', 'name', 'lot_size', 'stock_type', 'stock_child_type', 'stock_owner',
                'option_type', 'strike_time', 'strike_price', 'suspension',
                'listing_date', 'stock_id', 'delisting',
                'main_contract', 'last_trade_time'
            ]
            ret_frame = pd.DataFrame(ret, columns=col_list)
            return RET_OK, ret_frame
        else:
            return RET_ERROR, "empty data"

    def get_stock_filter(self, market, filter_list=None, plate_code=None, begin=0, num=200):
        """
        Qot_StockFilter
        :param plate_code: 板块代码, string, 例如，”SH.BK0001”，”SH.BK0002”，先利用获取子版块列表函数获取子版块代码
        """
        if not Market.if_has_key(market):
            error_str = ERROR_STR_PREFIX + "the value of market param is wrong "
            return RET_ERROR, error_str

        if plate_code is not None and is_str(plate_code) is False:
            error_str = ERROR_STR_PREFIX + "the type of plate_code is wrong"
            return RET_ERROR, error_str

        """容错容错"""
        if filter_list is None:
            filter_list = []

        if filter_list is not None and (isinstance(filter_list, SimpleFilter) or isinstance(filter_list, AccumulateFilter) or isinstance(filter_list, FinancialFilter)):
            filter_list = [filter_list]
        if filter_list is not None and not isinstance(filter_list, list):
            error_str = ERROR_STR_PREFIX + "the type of filter_list is wrong"
            return RET_ERROR, error_str

        for filter in filter_list:
            if not (isinstance(filter, SimpleFilter) or isinstance(filter, AccumulateFilter) or isinstance(filter, FinancialFilter)):
                error_str = ERROR_STR_PREFIX + "the item of filter_list is wrong"
                return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            StockFilterQuery.pack_req,
            StockFilterQuery.unpack,
        )

        kargs = {
            "market": market,
            "filter_list": filter_list,
            "plate_code": plate_code,
            "begin": begin,
            "num": num,
            "conn_id": self.get_sync_conn_id()
        }
        ret_code, msg, ret = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg
        else:
            return RET_OK, ret

    def get_code_change(self, code_list=[], time_filter_list=[], type_list=[]):
        """
        股票更换代码或者中途并行交易临时代码信息

        :param code_list: 股票列表，例如['HK.00700']
        :param time_filter_list: 时间过滤列表, 例如[t1, t2], t1 = TimeFilter(type = TimeFilterType.PUBLIC, begin_time = "2019-12-31",end_time = "2019-12-30")
        :param type_list: 类型过滤列表，例如[CodeChangeType.GEM_TO_MAIN]
        :return: (ret, data)

                ret == RET_OK 返回pd dataframe数据，data.DataFrame数据, 数据列格式如下

                ret != RET_OK 返回错误字符串

                =====================   ===========   =================================================================================
                参数                      类型                        说明
                =====================   ===========   =================================================================================
                code_change_info_type   str            类型
                security                str            主代码，在创业板转主板中表示主板
                related_security        str            关联代码，在创业板转主板中表示创业板，在剩余事件中表示临时代码
                public_time             str            公布时间
                effective_time          str            生效时间
                end_time                str            结束时间，在创业板转主板事件不存在该字段，在剩余事件表示临时代码交易结束时间
                =====================   ===========   =================================================================================
        """
        time_filter_list = unique_and_normalize_list(time_filter_list)
        for time_filter in time_filter_list:
            r, n = TimeFilterType.to_number(time_filter.type)
            if time_filter.type is None or r is False:
                error_str = ERROR_STR_PREFIX + "the type of param in time_filter is wrong"
                return RET_ERROR, error_str

        if is_str(code_list):
            code_list = code_list.split(',')
        elif isinstance(code_list, list):
            pass
        else:
            return RET_ERROR, "code list must be like ['HK.00001', 'HK.00700'] or 'HK.00001,HK.00700'"
        code_list = unique_and_normalize_list(code_list)
        for code in code_list:
            if code is None or is_str(code) is False:
                error_str = ERROR_STR_PREFIX + "the type of param in code_list is wrong"
                return RET_ERROR, error_str

        if is_str(type_list):
            type_list = type_list.split(',')
        elif isinstance(type_list, list):
            pass
        else:
            return RET_ERROR, "code list must be like [CodeChangeType.CHANGE_LOT, CodeChangeType.GEMTOMAIN] or 'CodeChangeType.CHANGE_LOT,CodeChangeType.GEMTOMAIN'"
        type_list = unique_and_normalize_list(type_list)
        for type in type_list:
            r, n = CodeChangeType.to_number(type)
            if type is None or r is False:
                error_str = ERROR_STR_PREFIX + "the type of param in type_list is wrong"
                return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            GetCodeChangeQuery.pack_req,
            GetCodeChangeQuery.unpack,
        )

        kargs = {
            "code_list": code_list,
            "time_filter_list": time_filter_list,
            "type_list": type_list,
            "conn_id": self.get_sync_conn_id()
        }
        ret_code, msg, ret = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg
        if isinstance(ret, list):
            col_list = [
                'code_change_info_type',
                'code',
                'related_code',
                'public_time',
                'effective_time',
                'end_time',
            ]
            ret_frame = pd.DataFrame(ret, columns=col_list)
            return RET_OK, ret_frame
        else:
            return RET_ERROR, "empty data"

    def get_ipo_list(self, market):
        """
        获取某个市场的ipo列表
        :param market: str, see Market
        :return:
        """
        if not Market.if_has_key(market):
            error_str = ERROR_STR_PREFIX + "the value of market param is wrong "
            return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            GetIpoListQuery.pack_req,
            GetIpoListQuery.unpack,
        )

        kargs = {
            'conn_id': self.get_sync_conn_id(),
            'market': market
        }
        ret, msg, data = query_processor(**kargs)
        if ret != RET_OK:
            return ret, msg

        col_dict = OrderedDict()
        col_dict.update((row[0], True) for row in pb_field_map_BasicIpoData)
        col_dict.update((row[0], True) for row in pb_field_map_CNIpoExData)
        col_dict.update((row[0], True) for row in pb_field_map_HKIpoExData)
        col_dict.update((row[0], True) for row in pb_field_map_USIpoExData)

        return RET_OK, pd.DataFrame(data, columns=col_dict.keys())

    def get_future_info(self, code_list):
        """
         获取期货合约资料
        :param code_list: 期货
        :return: (ret, data)
        ret != RET_OK 返回错误字符串
        ret == RET_OK data为DataFrame类型，字段如下:
        =========================   ===========   =========================
        参数                         类型           说明
        =========================   ===========   =========================
        code                        str            股票代码
        name                        str            股票名称
        owner                       string         标的
        exchange                    string         交易所
        type                        string         合约类型
        size                        float          合约规模
        size_unit                   string         合约规模单位
        price_currency              string         报价货币
        price_unit                  string         报价单位
        min_change                  float          最小变动
        min_change_unit             string         最小变动的单位
        trade_time                  string         交易时间
        time_zone                   string         时区
        last_trade_time             string         最后交易时间
        exchange_format_url         string         交易所规格url
        =========================   ===========   =========================
        """
        if is_str(code_list):
            code_list = code_list.split(',')
        elif isinstance(code_list, list):
            pass
        else:
            return RET_ERROR, "code list must be like ['HK.00001', 'HK.00700'] or 'HK.00001,HK.00700'"
        code_list = unique_and_normalize_list(code_list)

        if not code_list:
            error_str = ERROR_STR_PREFIX + "the type of code param is wrong"
            return RET_ERROR, error_str

        for code in code_list:
            if code is None or is_str(code) is False:
                error_str = ERROR_STR_PREFIX + "the type of param in code_list is wrong"
                return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            GetFutureInfoQuery.pack_req,
            GetFutureInfoQuery.unpack,
        )

        kargs = {
            "code_list": code_list,
            "conn_id": self.get_sync_conn_id()
        }
        ret_code, msg, ret = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg
        else:
            col_list = [
                'code',
                'name',
                'owner',
                'exchange',
                'type',
                'size',
                'size_unit',
                'price_currency',
                'price_unit',
                'min_change',
                'min_change_unit',
                'trade_time',
                'time_zone',
                'last_trade_time',
                'exchange_format_url'
            ]
            ret_frame = pd.DataFrame(ret, columns=col_list)
            return RET_OK, ret_frame

    def set_price_reminder(self, code, op, key=None, reminder_type=None, reminder_freq=None, value=None, note=None):
        """
         新增、删除、修改、启用、禁用 某只股票的到价提醒，每只股票每种类型最多可设置10个提醒
         注意：
            1. API 中成交量设置统一以股为单位。但是牛牛客户端中，A 股是以为手为单位展示
            2. 到价提醒类型，存在最小精度，如下：
                TURNOVER_UP：成交额最小精度为 10 元（人民币元，港元，美元）。传入的数值会自动向下取整到最小精度的整数倍。
                    如果设置【00700成交额102元提醒】，设置后会得到【00700成交额100元提醒】；如果设置【00700 成交额 8 元提醒】，设置后会得到【00700 成交额 0 元提醒】
                VOLUME_UP：A 股成交量最小精度为 1000 股，其他市场股票成交量最小精度为 10 股。传入的数值会自动向下取整到最小精度的整数倍。
                BID_VOL_UP、ASK_VOL_UP：A 股的买一卖一量最小精度为 100 股。传入的数值会自动向下取整到最小精度的整数倍。
                其余到价提醒类型精度支持到小数点后 3 位
        :param code: 股票
        :param op：SetPriceReminderOp，操作类型
        :param key: int64，标识，新增的情况不需要填
        :param reminder_type: PriceReminderType，到价提醒的频率，删除、启用、禁用的情况下会忽略该入参
        :param reminder_freq: PriceReminderFreq，到价提醒的频率，删除、启用、禁用的情况下会忽略该入参
        :param value: float，提醒值，删除、启用、禁用的情况下会忽略该入参
        :param note: str，用户设置的备注，删除、启用、禁用的情况下会忽略该入参
        :return: (ret, data)
        ret != RET_OK 返回错误字符串
        ret == RET_OK data为key
        """
        if code is None or is_str(code) is False:
            error_str = ERROR_STR_PREFIX + 'the type of code param is wrong'
            return RET_ERROR, error_str

        r, v = SetPriceReminderOp.to_number(op)
        if r is False:
            error_str = ERROR_STR_PREFIX + "the type of param in op is wrong"
            return RET_ERROR, error_str

        if reminder_type is not None :
            r, v = PriceReminderType.to_number(reminder_type)
            if r is False:
                error_str = ERROR_STR_PREFIX + "the type of param in reminder_type is wrong"
                return RET_ERROR, error_str

        if reminder_freq is not None :
            r, v = PriceReminderFreq.to_number(reminder_freq)
            if r is False:
                error_str = ERROR_STR_PREFIX + "the type of param in reminder_freq is wrong"
                return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            SetPriceReminderQuery.pack_req,
            SetPriceReminderQuery.unpack,
        )

        kargs = {
            "code": code,
            "op": op,
            "key": key,
            "reminder_type": reminder_type,
            "reminder_freq": reminder_freq,
            "value": value,
            "note": note,
            "conn_id": self.get_sync_conn_id()
        }
        ret_code, msg, key = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg
        else:
            return RET_OK, key

    def get_price_reminder(self, code=None, market=None):
        """
         获取对某只股票(某个市场)设置的到价提醒列表
        :param code: 获取该股票的到价提醒，code和market二选一，都存在的情况下code优先
        :param market: 获取该市场的到价提醒，注意传入沪深都会认为是A股市场
        :return: (ret, data)
        ret != RET_OK 返回错误字符串
        ret == RET_OK data为DataFrame类型，字段如下:
        =========================   ==================   =========================
        参数                         类型                 说明
        =========================   ==================   =========================
        code                        str                  股票代码
        key                         int64                标识，用于修改到价提醒
        reminder_type               PriceReminderType    到价提醒的类型
        reminder_freq               PriceReminderFreq    到价提醒的频率
        value                       float                提醒值
        enable                      bool                 是否启用
        note                        string               备注，最多10个字符
        =========================   ==================   =========================
        """
        if code is not None and is_str(code) is False:
            error_str = ERROR_STR_PREFIX + 'the type of code param is wrong'
            return RET_ERROR, error_str

        if code is None and market is not None and not Market.if_has_key(market):
            error_str = ERROR_STR_PREFIX + "the type of param in market is wrong"
            return RET_ERROR, error_str

        if code is None and market is None:
            error_str = ERROR_STR_PREFIX + "must be use one of these params(code, market)"
            return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            GetPriceReminderQuery.pack_req,
            GetPriceReminderQuery.unpack,
        )

        kargs = {
                "code": code,
                "market": market,
                "conn_id": self.get_sync_conn_id()
        }
        ret_code, msg, ret = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg
        if isinstance(ret, list):
            col_list = [
                'code',
                'key',
                'reminder_type',
                'reminder_freq',
                'value',
                'enable',
                'note',
            ]
            ret_frame = pd.DataFrame(ret, columns=col_list)
            return RET_OK, ret_frame
        else:
            return RET_ERROR, "empty data"

    def get_user_security_group(self, group_type = UserSecurityGroupType.ALL):
        """
         获取自选股分组列表
        :param group_type: UserSecurityGroupType，分组类型
        :return: (ret, data)
        ret != RET_OK 返回错误字符串
        ret == RET_OK data为DataFrame类型，字段如下:
        =========================   ==================   ================================
        参数                         类型                 说明
        =========================   ==================   ================================
        group_name                   str                  分组名
        group_type                   str                  UserSecurityGroupType，分组类型
        =========================   ==================   ================================
        """
        r, v = UserSecurityGroupType.to_number(group_type)
        if r is False:
            error_str = ERROR_STR_PREFIX + "the type of param in group_type is wrong"
            return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            GetUserSecurityGroupQuery.pack_req,
            GetUserSecurityGroupQuery.unpack,
        )

        kargs = {
            "group_type": group_type,
            "conn_id": self.get_sync_conn_id()
        }
        ret_code, msg, ret = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg
        if isinstance(ret, list):
            col_list = [
                'group_name',
                'group_type'
            ]
            ret_frame = pd.DataFrame(ret, columns=col_list)
            return RET_OK, ret_frame
        else:
            return RET_ERROR, "empty data"

    def get_market_state(self, code_list):
        """
         获取股票对应市场的市场状态
        :param code_list 股票列表
        :return: (ret, data)
        ret != RET_OK 返回错误字符串
        ret == RET_OK data为DataFrame类型，字段如下:
        =========================   ==================   ================================
        参数                         类型                 说明
        =========================   ==================   ================================
        code                         str                  股票代码
        stock_name                   str                  股票名称
        market_state                 MarketState          市场状态
        =========================   ==================   ================================
        """
        if is_str(code_list):
            code_list = code_list.split(',')
        elif isinstance(code_list, list) and len(code_list) > 0:
            pass
        else:
            return RET_ERROR, "code list must be like ['HK.00001', 'HK.00700'] or 'HK.00001,HK.00700'"
        code_list = unique_and_normalize_list(code_list)
        for code in code_list:
            if code is None or is_str(code) is False:
                error_str = ERROR_STR_PREFIX + "the type of param in code_list is wrong"
                return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            GetMarketStateQuery.pack_req,
            GetMarketStateQuery.unpack,
        )

        kargs = {
            "code_list": code_list,
            "conn_id": self.get_sync_conn_id()
        }
        ret_code, msg, ret = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg
        if isinstance(ret, list):
            col_list = [
                'code',
                'stock_name',
                'market_state'
            ]
            ret_frame = pd.DataFrame(ret, columns=col_list)
            return RET_OK, ret_frame
        else:
            return RET_ERROR, "empty data"

