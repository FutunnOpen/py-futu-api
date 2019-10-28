# -*- coding: utf-8 -*-
"""
    Market quote and trade context setting
"""
from futu import *
from futu.common.constant import *
from futu.common.utils import *

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
        filter_req.field = v - StockField.simple_enum_begin
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
        return RET_OK, ""

class AccumulateFilter(object):
    stock_field = StockField.NONE  # StockField 简单属性
    filter_min = None  # 区间下限，闭区间
    filter_max = None  # 区间上限，闭区间
    sort = None  # SortDir 排序方向 SortDir
    is_no_filter = None  # 如果这个字段不需要筛选，但是需要返回这个字段的数据，指定该字段为ture。当该字段为true时，以上三个字段无效。
    days = 1 #所筛选的数据的累计天数
    
    def __init__(self):
        self.stock_field = StockField.NONE
        self.filter_min = None
        self.filter_max = None
        self.sort = None
        self.is_no_filter = None
        self.days = 1

    def fill_request_pb(self, filter_req):
        r, v = StockField.to_number(self.stock_field)
        if not r:
            return RET_ERROR, 'stock_field is wrong. must be StockField'
        filter_req.field = v - StockField.acc_enum_begin
        filter_req.days = self.days
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
        return RET_OK, ""
            
class FinancialFilter(object):
    stock_field = StockField.NONE  # StockField 简单属性
    filter_min = None  # 区间下限，闭区间
    filter_max = None  # 区间上限，闭区间
    sort = None  # SortDir 排序方向 SortDir
    is_no_filter = None  # 如果这个字段不需要筛选，但是需要返回这个字段的数据，指定该字段为ture。当该字段为true时，以上三个字段无效。
    quarter = FinancialQuarter.ANNUAL #财报累积时间
    
    def __init__(self):
        self.stock_field = StockField.NONE
        self.filter_min = None
        self.filter_max = None
        self.sort = None
        self.is_no_filter = None
        self.quarter = FinancialQuarter.ANNUAL

    def fill_request_pb(self, filter_req):
        r, v = StockField.to_number(self.stock_field)
        if not r:
            return RET_ERROR, 'stock_field is wrong. must be StockField'
        filter_req.field = v - StockField.financial_enum_begin
        
        r, v = FinancialQuarter.to_number(self.quarter)
        if not r:
            return RET_ERROR, 'quarter is wrong. must be FinancialQuarter'    
        filter_req.quarter = v
        
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

        return RET_OK, ""

class FilterStockData(object):
    stock_code = None
    stock_name = None
	 # 以下是简单数据过滤所支持的字段
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
    # change_rate_5min = None # 五分钟价格涨跌幅
    # change_rate_begin_year = None  # 年初至今价格涨跌幅

    # 以下是累积数据过滤所支持的字段
    # change_rate = None # 涨跌幅
    # amplitude = None # 振幅
    # volume = None # 成交量
    # turnover = None # 成交额
    # turnover_rate = None # 换手率

    # 以下是财务数据过滤所支持的字段
    # net_profit = None # 净利润
    # net_profix_growth = None # 净利润增长率
    # sum_of_business = None # 营业收入
    # sum_of_business_growth = None # 营业同比增长率
    # net_profit_rate = None # 净利率
    # gross_profit_rate = None # 毛利率
    # debt_asset_rate = None # 资产负债率
    # return_on_equity_rate = None # 净资产收益率
    
    def __init__(self, rsp_item):
        from futu.common.pb.Qot_StockFilter_pb2 import StockData
        if not isinstance(rsp_item, StockData):
            raise Exception("Response item need Qot_StockFilter_pb2")

        self.stock_code = merge_qot_mkt_stock_str(rsp_item.security.market, rsp_item.security.code)
        #  名称 type = string
        self.stock_name = rsp_item.name
        
        # ls = StockField.get_all_key_list()
        # for key in ls:
        #     attr = key.lower()
        #     if attr not in self.__dict__:
        #         """增加一个属性"""
        #         self.__dict__[attr] = None

        #  筛选后的简单属性数据 type = Qot_StockFilter.BaseData
        base_data_list = rsp_item.baseDataList
        for sub_item in base_data_list:
            ret, field = StockField.to_string(sub_item.field + StockField.simple_enum_begin)
            if ret:
                self.__dict__[field.lower()] = sub_item.value
                
        #  筛选后的简单属性数据 type = Qot_StockFilter.AccumulateData
        base_data_list = rsp_item.accumulateDataList
        for sub_item in base_data_list:
            ret, field = StockField.to_string(sub_item.field + StockField.acc_enum_begin)
            if ret:
                self.__dict__[(field.lower(), sub_item.days)] = sub_item.value
                
        #  筛选后的简单属性数据 type = Qot_StockFilter.FinancialData
        base_data_list = rsp_item.financialDataList
        for sub_item in base_data_list:
            ret1, field = StockField.to_string(sub_item.field + StockField.financial_enum_begin)
            ret2, quarter = FinancialQuarter.to_string(sub_item.quarter)
            if ret1 and ret2:
                self.__dict__[(field.lower(), quarter.lower())] = sub_item.value

    def __repr__(self):
        ls = StockField.get_all_key_list()
        s = ""
        for key in self.__dict__:
            value = self.__dict__[key]
            if value is not None:
                if isinstance(key, tuple):
                    s += (" {}({}):{} ".format(key[0], key[1], value))
                else:
                    s += (" {}:{} ".format(key, value))
        return s
