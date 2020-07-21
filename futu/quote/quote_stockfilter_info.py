# -*- coding: utf-8 -*-
"""
    Market quote and trade context setting
"""
from futu import *
from futu.common.constant import *
from futu.common.utils import *

class SimpleFilter(object):
    def __init__(self):
        self.stock_field = StockField.NONE # StockField 简单属性
        self.filter_min = None  # 区间下限，闭区间
        self.filter_max = None  # 区间上限，闭区间
        self.sort = None   # SortDir 排序方向 SortDir
        self.is_no_filter = None # 如果这个字段不需要筛选，指定该字段为ture。当该字段为true时，以上三个字段无效。

    def fill_request_pb(self, filter_req):
        r, v = StockField.to_number(self.stock_field)
        if not r:
            return RET_ERROR, 'stock_field is wrong. must be StockField'
        filter_req.fieldName = v - StockField.simple_enum_begin
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
                return RET_ERROR, 'sort is wrong. must be SortDir'
            filter_req.sortDir = v
        return RET_OK, ""

class AccumulateFilter(object):
    def __init__(self):
        self.stock_field = StockField.NONE   # StockField 累计属性
        self.filter_min = None  # 区间下限，闭区间
        self.filter_max = None  # 区间上限，闭区间
        self.sort = None  # SortDir 排序方向 SortDir
        self.is_no_filter = None  # 如果这个字段不需要筛选，指定该字段为ture。当该字段为true时，以上三个字段无效。
        self.days = 1  #所筛选的数据的累计天数

    def fill_request_pb(self, filter_req):
        r, v = StockField.to_number(self.stock_field)
        if not r:
            return RET_ERROR, 'stock_field is wrong. must be StockField'
        filter_req.fieldName = v - StockField.acc_enum_begin
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
                return RET_ERROR, 'sort is wrong. must be SortDir'
            filter_req.sortDir = v
        return RET_OK, ""
            
class FinancialFilter(object):
    def __init__(self):
        self.stock_field = StockField.NONE  # StockField 财务属性
        self.filter_min = None  # 区间下限，闭区间
        self.filter_max = None  # 区间上限，闭区间
        self.sort = None  # SortDir 排序方向 SortDir
        self.is_no_filter = None  # 如果这个字段不需要筛选，指定该字段为ture。当该字段为true时，以上三个字段无效。
        self.quarter = FinancialQuarter.ANNUAL #财报累积时间

    def fill_request_pb(self, filter_req):
        r, v = StockField.to_number(self.stock_field)
        if not r:
            return RET_ERROR, 'stock_field is wrong. must be StockField'
        filter_req.fieldName = v - StockField.financial_enum_begin

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
                return RET_ERROR, 'sort is wrong. must be SortDir'
            filter_req.sortDir = v

        return RET_OK, ""

class FilterStockData(object):
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
    # ps_ttm  # 市销率(ttm) 例如填写 [100, 500] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    # pcf_ttm  # 市现率(ttm) 例如填写 [100, 1000] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    # total_share  # 总股数 例如填写 [1000000000,1000000000] 值区间 (单位：股)
    # float_share  # 流通股数 例如填写 [1000000000,1000000000] 值区间 (单位：股)
    # float_market_val  # 流通市值 例如填写 [1000000000,1000000000] 值区间 (单位：元)

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
    #roic # 盈利能力属性投入资本回报率 例如填写 [1.0,10.0] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    # roa_ttm  # 资产回报率(ttm) 例如填写 [1.0,10.0] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%。仅适用于年报。）
    # ebit_ttm # 息税前利润(ttm) 例如填写 [1000000000,1000000000] 值区间（单位：元。仅适用于年报。）
    # ebitda  # 税息折旧及摊销前利润 例如填写 [1000000000,1000000000] 值区间（单位：元）
    # operating_margin_ttm  # 营业利润率(ttm) 例如填写 [1.0,10.0] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%。仅适用于年报。）
    # ebit_margin  # ebit利润率 例如填写 [1.0,10.0] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    # ebitda_margin  # ebitda利润率 例如填写 [1.0,10.0] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    # financial_cost_rate  # 财务成本率 例如填写 [1.0,10.0] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    # operating_profit_ttm  # 营业利润(ttm) 例如填写 [1000000000,1000000000] 值区间 （单位：元。仅适用于年报。）
    # shareholder_net_profit_ttm  # 归属于母公司的净利润 例如填写 [1000000000,1000000000] 值区间 （单位：元。仅适用于年报。）
    # net_profit_cash_cover_ttm  # 盈利中的现金收入比例 例如填写 [1.0,60.0] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%。仅适用于年报。）
    # current_ratio  # 偿债能力属性流动比率 例如填写 [100,250] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    # quick_ratio  # 速动比率 例如填写 [100,250] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    # current_asset_ratio  # 清债能力属性流动资产率 例如填写 [10,100] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    # current_debt_ratio  # 流动负债率 例如填写 [10,100] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    # equity_multiplier  # 权益乘数 例如填写 [100,180] 值区间
    # property_ratio  # 产权比率 例如填写 [50,100] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    # cash_and_cash_equivalents  # 现金和现金等价 例如填写 [1000000000,1000000000] 值区间（单位：元）
    # total_asset_turnover  # 运营能力属性总资产周转率 例如填写 [50,100] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    # fixed_asset_turnover  # 固定资产周转率 例如填写 [50,100] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    # inventory_turnover  # 存货周转率 例如填写 [50,100] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    # operating_cash_flow_ttm  # 经营活动现金流(ttm) 例如填写 [1000000000,1000000000] 值区间（单位：元。仅适用于年报。）
    # accounts_receivable  # 应收账款净额 例如填写 [1000000000,1000000000] 值区间 例如填写 [1000000000,1000000000] 值区间 （单位：元）
    # ebit_growth_rate  # 成长能力属性ebit同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    # operating_profit_growth_rate  # 营业利润同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    # total_assets_growth_rate  # 总资产同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    # profit_to_shareholders_growth_rate  # 归母净利润同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    # profit_before_tax_growth_rate  # 总利润同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    # eps_growth_rate  # eps同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    # roe_growth_rate  # roe同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    # roic_growth_rate  # roic同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    # nocf_growth_rate  # 经营现金流同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    # nocf_per_share_growth_rate  # 每股经营现金流同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    # operating_revenue_cash_cover  # 现金流属性经营现金收入比 例如填写 [10,100] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    # operating_profit_to_total_profit  # 营业利润占比 例如填写 [10,100] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    # basic_eps  # 市场表现属性基本每股收益 例如填写 [0.1,10] 值区间 (单位：元)
    # diluted_eps  # 稀释每股收益 例如填写 [0.1,10] 值区间 (单位：元)
    # nocf_per_share  # 每股经营现金净流量 例如填写 [0.1,10] 值区间 (单位：元)

    def __init__(self, rsp_item):
        self.stock_code = None
        self.stock_name = None

        from futu.common.pb.Qot_StockFilter_pb2 import StockData
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
            ret, field = StockField.to_string(sub_item.fieldName + StockField.simple_enum_begin)
            if ret:
                self.__dict__[field.lower()] = sub_item.value
                
        #  筛选后的累计属性数据 type = Qot_StockFilter.AccumulateData
        base_data_list = rsp_item.accumulateDataList
        for sub_item in base_data_list:
            ret, field = StockField.to_string(sub_item.fieldName + StockField.acc_enum_begin)
            if ret:
                self.__dict__[(field.lower(), sub_item.days)] = sub_item.value
                
        #  筛选后的财务属性数据 type = Qot_StockFilter.FinancialData
        base_data_list = rsp_item.financialDataList
        for sub_item in base_data_list:
            ret1, field = StockField.to_string(sub_item.fieldName + StockField.financial_enum_begin)
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
