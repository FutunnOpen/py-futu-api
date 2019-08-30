# -*- coding: utf-8 -*-
"""
    Market quote and trade context setting
"""
from futu import *
from futu.common.constant import *


class SimpleFilter(object):
    """这里用simple替换掉协议里面的Base，以后有各种filter扩展"""
    stock_field = StockField.NONE  # StockField 简单属性
    filter_min = None  # 区间下限，闭区间
    filter_max = None  # 区间上限，闭区间
    sort = None  # SortDir 排序方向 SortDir
    is_no_filter = None  # 如果这个字段不需要筛选，但是需要返回这个字段的数据，指定该字段为ture。当该字段为true时，以上三个字段无效。

    def __init__(self):
        self.stock_field = StockField.NONE
        self.filter_min = None
        self.filter_max = None
        self.sort = None
        self.is_no_filter = None

    def fill_request_pb(self, filter_req):
        r, v = StockField.to_number(self.stock_field)
        if not r:
            return RET_ERROR, 'stock_field is wrong. must be StockField'
        filter_req.field = v
        """有了这个字段，别的字段都可以不要了"""
        if self.is_no_filter is False:
            filter_req.isNoFilter = False
            if self.filter_min is not None:
                filter_req.filterMin = self.filter_min
            if self.filter_max is not None:
                filter_req.filterMax = self.filter_max

        if self.sort is not None:
            r, v = SortDir.to_number(self.sort)
            if not r:
                raise Exception("sort is wrong. must be SortDir")
            filter_req.sortDir = v


class FilterStockData(object):
    stock_code = None
    stock_name = None
    # cur_price = None  # 最新价
    # cur_price_to_highest_52weeks_ratio = None  # (现价 - 52周最高) / 52周最高，对应pc端离52周高点百分比
    # cur_price_to_lowest_52weeks_ratio = None  # (现价 - 52周最低) / 52周最低，对应pc端离52周低点百分比
    # high_price_to_highest_52weeks_ratio = None  # (今日最高 - 52周最高) / 52周最高，对应pc端52周新高
    # low_price_to_lowest_52weeks_ratio = None  # (今日最低 - 52周最低) / 52周最低 对应pc端52周新低
    # volume_ratio = None  # 量比
    # bid_ask_ratio = None  # 委比
    # lot_price = None  # 每手价格
    # market_val = None  # 市值
    # pe_annual = None  # 年化(静态) 市盈率
    # pe_ttm = None  # 市盈率ttm
    # pb_rate = None  # 市净率

    def __init__(self, rsp_item):
        from futu.common.pb.Qot_StockFilter_pb2 import StockData
        if not isinstance(rsp_item, StockData):
            raise Exception("Response item need Qot_StockFilter_pb2")

        self.stock_code = merge_qot_mkt_stock_str(
            rsp_item.security.market, rsp_item.security.code)
        #  名称 type = string
        self.stock_name = rsp_item.name
        #  筛选后的简单属性数据 type = Qot_StockFilter.BaseData
        base_data_list = rsp_item.baseDataList

        ls = StockField.get_all_key_list()
        for key in ls:
            attr = key.lower()
            if attr not in self.__dict__:
                """增加一个属性"""
                self.__dict__[attr] = None

        for sub_item in base_data_list:
            ret, field = StockField.to_string(sub_item.field)
            if ret:
                key = field.lower()
                self.__dict__[key] = sub_item.value

    def __repr__(self):
        ls = StockField.get_all_key_list()
        s = ""
        for key in ls:
            attr = key.lower()
            if attr in self.__dict__:
                value = self.__dict__[attr]
                if value is not None:
                    s += (" {}:{} ".format(attr, value))
        return s
