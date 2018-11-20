========
行情API
========

 .. _Market: Base_API.html#market
 
 .. _MarketState: Base_API.html#marketstate
 
 .. _SecurityType: Base_API.html#securitytype
 
 .. _WrtType: Base_API.html#wrttype
 
 .. _SubType: Base_API.html#subtype
 
 .. _KLType: Base_API.html#kltype-k
 
 .. _KLDataStatus: Base_API.html#kldatastatus-k
 
 .. _AuType: Base_API.html#autype-k
 
 .. _KLNoDataMode: Base_API.html#klnodatamode-k
 
 .. _KL_FIELD : Base_API.html#kl-field-k
 
 .. _TickerDirect: Base_API.html#tickerdirect
 
 .. _Plate: Base_API.html#plate
  
 .. _StockHolder: Base_API.html#stockholder

 .. _OptionType: Base_API.html#optiontype

 .. _OptionCondType: Base_API.html#optioncondtype
 
 .. _SysNotifyType: Base_API.html#sysnotifytype
 
 .. _GtwEventType: Base_API.html#gtweventtype
 
 .. _SecurityReferenceType: Base_API.html#securityreferencetype
 
 .. _PushDataType: Base_API.html#pushdatatype
 
 .. _TickerType: Base_API.html#tickertype

 .. _DarkStatus: Base_API.html#darkstatus

一分钟上手
============

如下范例，创建api行情对象，调用get_market_snapshot获取港股腾讯00700的报价快照数据,最后关闭对象

.. code:: python

    from futu import *
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    print(quote_ctx.get_market_snapshot('HK.00700'))
    quote_ctx.close()
    
----------------------------


接口类对象
==========

OpenQuoteContext - 行情上下文对象类
-------------------------------------------


close
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: close

关闭上下文对象。默认情况下，futu-api内部创建的线程会阻止进程退出，只有当所有context都close后，进程才能正常退出。但通过SysConfig.set_all_thread_daemon可以设置所有内部线程为daemon线程，这时即使没有调用context的close，进程也可以正常退出。

.. code:: python

    from futu import *
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    quote_ctx.close()
    
    
start
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: start

启动异步接收推送数据


stop
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: stop

停止异步接收推送数据


set_handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: set_handler(self, handler)

 设置异步回调处理对象

 :param handler: 回调处理对象，必须是以下类的子类实例

            ===============================    =========================
             类名                                 说明
            ===============================    =========================
            SysNotifyHandlerBase				OpenD通知处理基类
            StockQuoteHandlerBase               报价处理基类
            OrderBookHandlerBase                摆盘处理基类
            CurKlineHandlerBase                 实时k线处理基类
            TickerHandlerBase                   逐笔处理基类
            RTDataHandlerBase                   分时数据处理基类
            BrokerHandlerBase                   经济队列处理基类
            ===============================    =========================
 :return ret: RET_OK: 设置成功

        其它: 设置失败

get_trading_days
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: get_trading_days(self, market, start=None, end=None)

 获取交易日

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
 :return: 成功时返回(RET_OK, data)，data是字符串数组；失败时返回(RET_ERROR, data)，其中data是错误描述字符串
        
 :Example:

 .. code:: python

    from futu import *
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    print(quote_ctx.get_trading_days(Market.HK, start='2018-01-01', end='2018-01-10'))
    quote_ctx.close()

get_stock_basicinfo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: get_stock_basicinfo(self, market, stock_type=SecurityType.STOCK, code_list=None)

 获取指定市场中特定类型的股票基本信息
 
 :param market: 市场类型 Market_
 :param stock_type: 股票类型，参见 SecurityType_，但不支持SecurityType.DRVT 
 :param code_list: 如果不为None，应该是股票code的iterable类型，将只返回指定的股票信息
 :return: (ret_code, content)

        ret_code 等于RET_OK时， content为Pandas.DataFrame数据, 否则为错误原因字符串, 数据列格式如下
        
        =================   ===========   ==============================================================================
        参数                  类型                        说明
        =================   ===========   ==============================================================================
        code                str            股票代码
        name                str            名字
        lot_size            int            每手数量
        stock_type          str            股票类型，参见 SecurityType_
        stock_child_type    str            窝轮子类型，参见 WrtType_
        stock_owner         str            涡轮所属正股的代码，或期权标的股的代码
        option_type         str            期权类型，查看 OptionType_
        strike_time         str            期权行权日（美股默认是美东时间，港股A股默认是北京时间）
        strike_price        float          期权行权价
        suspension          bool           期权是否停牌(True表示停牌)
        listing_date        str            上市时间
        stock_id            int            股票id
        delisting           bool           是否退市
        =================   ===========   ==============================================================================

 :Example:

 .. code-block:: python

    from futu import *
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    print(quote_ctx.get_stock_basicinfo(Market.HK, SecurityType.WARRANT))
    print(quote_ctx.get_stock_basicinfo(Market.US, SecurityType.STOCK, 'US.AAPL'))
    quote_ctx.close()
    
    
get_multiple_history_kline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: get_multiple_history_kline(self, codelist, start=None, end=None, ktype=KLType.K_DAY, autype=AuType.QFQ)

 获取多只股票的本地历史k线数据

 :param codelist: 股票代码列表，list或str。例如：['HK.00700', 'HK.00001']，'HK.00700,SZ.399001'
 :param start: 起始时间，，例如'2017-06-20'
 :param end: 结束时间，例如'2017-07-20'
 :param ktype: k线类型，参见 KLType_
 :param autype: 复权类型，参见 AuType_
 :return: 成功时返回(RET_OK, [data])，data是DataFrame数据, 数据列格式如下

    =================   ===========   ==============================================================================
    参数                  类型                        说明
    =================   ===========   ==============================================================================
    code                str            股票代码
    time_key            str            k线时间（美股默认是美东时间，港股A股默认是北京时间）
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

	失败时返回(RET_ERROR, data)，其中data是错误描述字符串
	
 :Example:

 .. code-block:: python

    from futu import *
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    print(quote_ctx.get_multiple_history_kline(['HK.00700'], '2017-06-20', '2017-06-25', KL_FIELD.ALL, KLType.K_DAY, AuType.QFQ))
    quote_ctx.close()




request_history_kline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: request_history_kline(self, code, start=None, end=None, ktype=KLType.K_DAY, autype=AuType.QFQ, fields=[KL_FIELD.ALL], max_count=1000, page_req_key=None)

 获取k线，不需要事先下载k线数据。

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
			  
 :param ktype: k线类型， 参见 KLType_ 定义
 :param autype: 复权类型, 参见 AuType_ 定义
 :param fields: 需返回的字段列表，参见 KL_FIELD_ 定义 KL_FIELD.ALL  KL_FIELD.OPEN ....
 :param max_count: 本次请求最大返回的数据点个数，传None表示返回start和end之间所有的数据。
 :param page_req_key: 分页请求的key。如果start和end之间的数据点多于max_count，那么后续请求时，要传入上次调用返回的page_req_key。初始请求时应该传None。
 :return: (ret, data, page_req_key)

        ret == RET_OK 返回pd dataframe数据，data.DataFrame数据, 数据列格式如下。page_req_key在分页请求时（即max_count>0）可能返回，并且需要在后续的请求中传入。如果没有更多数据，page_req_key返回None。

        ret != RET_OK 返回错误字符串

    =================   ===========   ==============================================================================
    参数                  类型                        说明
    =================   ===========   ==============================================================================
    code                str            股票代码
    time_key            str            k线时间（美股默认是美东时间，港股A股默认是北京时间）
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

	
 :Example:

 .. code:: python

    from futu import *
    ret, data, page_req_key = quote_ctx.request_history_kline('HK.00700', start='2017-06-20', end='2018-06-22', max_count=50) #请求开头50个数据
    print(ret, data)
    ret, data, page_req_key = quote_ctx.request_history_kline('HK.00700', start='2017-06-20', end='2018-06-22', max_count=50, page_req_key=page_req_key) #请求下50个数据
    print(ret, data)
    quote_ctx.close()


get_autype_list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: get_autype_list(self, code_list)

 获取给定股票列表的复权因子

 :param code_list: 股票列表，例如['HK.00700']
 :return: (ret, data)

        ret == RET_OK 返回pd dataframe数据，data.DataFrame数据, 数据列格式如下

        ret != RET_OK 返回错误字符串

 =====================   ===========   ====================================================================================
 参数                      类型                        说明
 =====================   ===========   ====================================================================================
 code                    str            股票代码
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
 =====================   ===========   ====================================================================================
		
 :Example:

 .. code:: python

    from futu import *
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    print(quote_ctx.get_autype_list(["HK.00700"]))
    quote_ctx.close()

get_market_snapshot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: get_market_snapshot(self, code_list)

获取市场快照

 :param code_list: 股票列表，股票个数限制参考 `OpenAPI用户等级权限 <Quote_API.html#id12>`_
 :return: (ret, data)

        ret == RET_OK 返回pd dataframe数据，data.DataFrame数据, 数据列格式如下

        ret != RET_OK 返回错误字符串

 ============================   =============   ======================================================================
 参数                             类型                       说明
 ============================   =============   ======================================================================
 code                            str            股票代码
 update_time                     str            更新时间(yyyy-MM-dd HH:mm:ss)（美股默认是美东时间，港股A股默认是北京时间）
 last_price                      float          最新价格
 open_price                      float          今日开盘价
 high_price                      float          最高价格
 low_price                       float          最低价格
 prev_close_price                float          昨收盘价格
 volume                          int            成交数量
 turnover                        float          成交金额
 turnover_rate                   float          换手率
 suspension                      bool           是否停牌(True表示停牌)
 listing_date                    str            上市日期 (yyyy-MM-dd)
 equity_valid                    bool           是否正股（为true时以下正股相关字段才有合法数值）
 issued_shares                   int            发行股本
 total_market_val                float          总市值
 net_asset                       int            资产净值
 net_profit                      int            净利润
 earning_per_share               float          每股盈利
 outstanding_shares              int            流通股本
 net_asset_per_share             float          每股净资产
 circular_market_val             float          流通市值
 ey_ratio                        float          收益率（该字段为比例字段，默认不展示%）
 pe_ratio                        float          市盈率（该字段为比例字段，默认不展示%）
 pb_ratio                        float          市净率（该字段为比例字段，默认不展示%）
 pe_ttm_ratio                    float          市盈率TTM（该字段为比例字段，默认不展示%）
 stock_owner                     str            涡轮所属正股的代码或期权的标的股代码
 wrt_valid                       bool           是否是窝轮（为true时以下涡轮相关的字段才有合法数据）
 wrt_conversion_ratio            float          换股比率（该字段为比例字段，默认不展示%）
 wrt_type                        str            窝轮类型，参见 WrtType_
 wrt_strike_price                float          行使价格
 wrt_maturity_date               str            格式化窝轮到期时间
 wrt_end_trade                   str            格式化窝轮最后交易时间
 wrt_code                        str            窝轮对应的正股（此字段已废除,修改为stock_owner）
 wrt_recovery_price              float          窝轮回收价
 wrt_street_vol                  float          窝轮街货量
 wrt_issue_vol                   float          窝轮发行量
 wrt_street_ratio                float          窝轮街货占比（该字段为比例字段，默认不展示%）
 wrt_delta                       float          窝轮对冲值
 wrt_implied_volatility          float          窝轮引伸波幅
 wrt_premium                     float          窝轮溢价
 lot_size                        int            每手股数
 price_spread                    float          当前向上的摆盘价差,亦即摆盘数据的卖档的相邻档位的报价差
 option_valid                    bool           是否是期权（为true时以下期权相关的字段才有合法数值）
 option_type                     str            期权类型，参见 OptionType_
 strike_time                     str            期权行权日（美股默认是美东时间，港股A股默认是北京时间）
 option_strike_price             float          行权价
 option_contract_size            int            每份合约数
 option_open_interest            int            未平仓合约数
 option_implied_volatility       float          隐含波动率
 option_premium                  float          溢价
 option_delta                    float          希腊值 Delta
 option_gamma                    float          希腊值 Gamma
 option_vega                     float          希腊值 Vega
 option_theta                    float          希腊值 Theta
 option_rho                      float          希腊值 Rho
 ============================   =============   ======================================================================
        
 :Example:

 .. code:: python

    from futu import *
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    print(quote_ctx.get_market_snapshot(['US.AAPL', 'HK.00700']))
    quote_ctx.close()

get_rt_data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: get_rt_data(self, code)

 获取指定股票的分时数据

 :param code: 股票代码，例如，HK.00700，US.AAPL
 :return (ret, data): ret == RET_OK 返回pd Dataframe数据, 数据列格式如下

        ret != RET_OK 返回错误字符串

=====================   ===========   ===================================================================
参数                      类型                        说明
=====================   ===========   ===================================================================
code                    str            股票代码
time                    str            时间(yyyy-MM-dd HH:mm:ss)（美股默认是美东时间，港股A股默认是北京时间）
is_blank                bool           数据状态；正常数据为False，伪造数据为True
opened_mins             int            零点到当前多少分钟
cur_price               float          当前价格
last_close              float          昨天收盘的价格
avg_price               float          平均价格（对于期权，该字段为None）
volume                  float          成交量
turnover                float          成交金额
=====================   ===========   ===================================================================

 :Example:

 .. code:: python

    from futu import *
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    quote_ctx.subscribe(['HK.00700'], [SubType.RT_DATA])
    print(quote_ctx.get_rt_data('HK.00700'))
    quote_ctx.close()
	
get_plate_stock
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: get_plate_stock(self, plate_code)

 获取特定板块下的股票列表

 :param plate_code: 板块代码, string, 例如，”SH.BK0001”，”SH.BK0002”，先利用获取子版块列表函数获取子版块代码
 :return (ret, data): ret == RET_OK 返回pd dataframe数据，data.DataFrame数据, 数据列格式如下

        ret != RET_OK 返回错误字符串

        =====================   ===========   ==============================================================
        参数                      类型                        说明
        =====================   ===========   ==============================================================
        code                    str            股票代码
        lot_size                int            每手股数
        stock_name              str            股票名称
        stock_type              str            股票类型，参见 SecurityType_
        list_time               str            上市时间（美股默认是美东时间，港股A股默认是北京时间）
        stock_id                int            股票id
        =====================   ===========   ==============================================================

 :Example:

 .. code:: python

    from futu import *
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    print(quote_ctx.get_plate_stock('HK.BK1001'))
    quote_ctx.close()		
    
   
.. note::

    *   该接口也可用于获取指数成份股, 如获取上证指数成份股:
    
		 .. code:: python
		
		    from futu import *
		    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
		    print(quote_ctx.get_plate_stock('SH.000001'))
		    quote_ctx.close()		
			    
    *   部分常用的板块或指数代码如下:
    
        =====================  ==============================================================
            代码                      说明
        =====================  ==============================================================
        HK.999901                  恒指成份股
        HK.999902                  国指成份股
        HK.999910                  港股主板
        HK.999911                  港股创业板
        HK.BK1911                  主板H股
        HK.BK1912                  创业板H股
        HK.900075                  港股基金
        HK.BK1600                  富途热门(港)
        SH.3000000                 上海主板
        SH.BK0901                  上证B股
        SH.BK0902                  深证B股 
        SH.3000002				   沪深指数
        SH.3000005                 沪深全部A股
        SH.BK0600                  富途热门(沪深)
        SZ.3000001                 深证主板
        SZ.3000003                 中小企业板块
        SZ.3000004                 深证创业板
        US.BK2600                  富途热门(美)
        US.USAALL                  全部美股(正股)
        US.NYSE                    纽交所
        US.NASDAQ                  纳斯达克
        US.AMEX                    美交所
        US.RPCCS                   美中概股
        US.STARCS                  美明星股
        =====================  ==============================================================
   
        
get_plate_list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: get_plate_list(self, market, plate_class)

 获取板块集合下的子板块列表

 :param market: 市场标识，注意这里不区分沪，深,输入沪或者深都会返回沪深市场的子板块（这个是和客户端保持一致的）参见 Market_
 :param plate_class: 板块分类，参见 Plate_
 :return (ret, data): ret == RET_OK 返回pd Dataframe数据，数据列格式如下

        ret != RET_OK 返回错误字符串

        =====================   ===========   ==============================================================
        参数                      类型                        说明
        =====================   ===========   ==============================================================
        code                    str            股票代码
        plate_name              str            板块名字
        plate_id                str            板块id
        =====================   ===========   ==============================================================

 :Example:

 .. code:: python

    from futu import *
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    print(quote_ctx.get_plate_list(Market.HK, Plate.ALL))
    quote_ctx.close()
        
get_broker_queue
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: get_broker_queue(self, code)

 获取股票的经纪队列

 :param code: 股票代码
 :return: (ret, bid_frame_table, ask_frame_table)或(ret, err_message)

        ret == RET_OK 返回pd dataframe数据，数据列格式如下

        ret != RET_OK 返回错误字符串

        bid_frame_table 经纪买盘数据
        
        =====================   ===========   ==============================================================
        参数                      类型                        说明
        =====================   ===========   ==============================================================
        code                    str             股票代码
        bid_broker_id           int             经纪买盘id
        bid_broker_name         str             经纪买盘名称
        bid_broker_pos          int             经纪档位
        =====================   ===========   ==============================================================

        ask_frame_table 经纪卖盘数据
        
        =====================   ===========   ==============================================================
        参数                      类型                        说明
        =====================   ===========   ==============================================================
        code                    str             股票代码
        ask_broker_id           int             经纪卖盘id
        ask_broker_name         str             经纪卖盘名称
        ask_broker_pos          int             经纪档位
        =====================   ===========   ==============================================================

 :Example:

 .. code:: python

    from futu import *
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    quote_ctx.subscribe(['HK.00700'], [SubType.BROKER])
    print(quote_ctx.get_broker_queue('HK.00700'))
    quote_ctx.close()
		
subscribe
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: subscribe(self, code_list, subtype_list, is_first_push=True)

 订阅注册需要的实时信息，指定股票和订阅的数据类型即可，港股订阅需要Lv2行情。 

 :param code_list: 需要订阅的股票代码列表
 :param subtype_list: 需要订阅的数据类型列表，参见 SubType_
 :param is_first_push: 订阅成功之后是否马上推送一次数据
 :return: (ret, err_message)

        ret == RET_OK err_message为None
        
        ret != RET_OK err_message为错误描述字符串
        
 :Example:

 .. code:: python

    from futu import *
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    print(quote_ctx.subscribe(['HK.00700'], [SubType.QUOTE]))
    quote_ctx.close()
		
		
unsubscribe
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: unsubscribe(self, code_list, subtype_list)

 取消订阅
 
 :param code_list: 取消订阅的股票代码列表
 :param subtype_list: 取消订阅的类型，参见 SubType_
 :return: (ret, err_message)
        
        ret == RET_OK err_message为None
        
        ret != RET_OK err_message为错误描述字符串
     
 :Example:

 .. code:: python

    from futu import *
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    print(quote_ctx.unsubscribe(['HK.00700'], [SubType.QUOTE]))
    quote_ctx.close()	 
        
query_subscription
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: query_subscription(self, is_all_conn=True)

 查询已订阅的实时信息

 :param is_all_conn: 是否返回所有连接的订阅状态,不传或者传False只返回当前连接数据
 :return: (ret, data)  
        
        ret != RET_OK 返回错误字符串
        
        ret == RET_OK 返回 定阅信息的字典数据 ，格式如下:
        
 .. code:: python

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

 :Example:

 .. code:: python

    from futu import *
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    print(quote_ctx.query_subscription())
    quote_ctx.close()
        
		
get_global_state
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: get_global_state(self)

 获取全局状态

 :return: (ret, data)

		ret == RET_OK data为包含全局状态的字典，含义如下

		ret != RET_OK data为错误描述字符串

		=====================   ===========   ==============================================================
		key                      value类型                        说明
		=====================   ===========   ==============================================================
		market_sz               str            深圳市场状态，参见 MarketState_
		market_us               str            美国市场状态，参见 MarketState_
		market_sh               str            上海市场状态，参见 MarketState_
		market_hk               str            香港市场状态，参见 MarketState_
		market_hkfuture           str            香港期货市场状态，参见 MarketState_
		server_ver              str            FutuOpenD版本号
		trd_logined             str            '1'：已登录交易服务器，'0': 未登录交易服务器
		qot_logined             str            '1'：已登录行情服务器，'0': 未登录行情服务器
		timestamp               str            当前格林威治时间戳(秒）
		local_timestamp         float          FutuOpenD运行机器的当前时间戳(秒)
		=====================   ===========   ==============================================================
 
 :Example:

 .. code:: python

    from futu import *
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    print(quote_ctx.get_global_state())
    quote_ctx.close()

get_stock_quote
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: get_stock_quote(self, code_list)

 获取订阅股票报价的实时数据，有订阅要求限制

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
        price_spread            float          当前向上的价差，亦即摆盘数据的卖档的相邻档位的报价差
		dark_status             str            暗盘交易状态，见 DarkStatus_
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
        =====================   ===========   ==============================================================
		
 :Example:

 .. code:: python

    from futu import *
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    code_list = ['US.AAPL210115C185000']
    print(quote_ctx.subscribe(code_list, [SubType.QUOTE]))
    print(quote_ctx.get_stock_quote(code_list))
    quote_ctx.close()
        
get_rt_ticker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: get_rt_ticker(self, code, num=500)

 获取指定股票的实时逐笔。取最近num个逐笔

 :param code: 股票代码
 :param num: 最近ticker个数，最多可获取1000个
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
        type                     str            逐笔类型，参见 TickerType_
        =====================   ===========   ==============================================================

 :Example:

 .. code:: python

    from futu import *
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    quote_ctx.subscribe(['HK.00700'], [SubType.TICKER])
    print(quote_ctx.get_rt_ticker('HK.00700', 10))
    quote_ctx.close()

get_cur_kline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: get_cur_kline(self, code, num, ktype=SubType.K_DAY, autype=AuType.QFQ)

 实时获取指定股票最近num个K线数据

 :param code: 股票代码
 :param num:  k线数据个数，最多1000根
 :param ktype: k线类型，参见 KLType_
 :param autype: 复权类型，参见 AuType_
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
        last_close               float          昨收价
        =====================   ===========   ==============================================================
		
 :Example:

 .. code:: python

    from futu import *
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    quote_ctx.subscribe(['HK.00700'], [SubType.K_DAY])
    print(quote_ctx.get_cur_kline('HK.00700', 10, SubType.K_DAY, AuType.QFQ))
    quote_ctx.close()

.. note::

    * 市盈率,换手率字段只有日K及日K以上周期的正股才有数据。
	
get_order_book
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: get_order_book(self, code)

 获取实时摆盘数据

 :param code: 股票代码
 :return: (ret, data)

 ret == RET_OK 返回字典，数据格式如下::
 
  {
  'code': 股票代码
  'Ask':[ (ask_price1, ask_volume1，order_num), (ask_price2, ask_volume2, order_num),…]
  'Bid': [ (bid_price1, bid_volume1, order_num), (bid_price2, bid_volume2, order_num),…]
  }

 | 'Ask'：卖盘
 | 'Bid'买盘
 | 每个元组的含义是(委托价格，委托数量，委托订单数)

 ret != RET_OK 返回错误字符串
    
        
 :Example:

 .. code:: python

    from futu import *
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    quote_ctx.subscribe(['HK.00700'], [SubType.ORDER_BOOK])
    print(quote_ctx.get_order_book('HK.00700'))
    quote_ctx.close()


        
get_multi_points_history_kline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: get_multi_points_history_kline(self, code_list, dates, fields, ktype=KLType.K_DAY, autype=AuType.QFQ, no_data_mode=KLNoDataMode.FORWARD)

 从本地历史K线中获取多支股票多个时间点的指定数据列

 :param code_list: 单个或多个股票 'HK.00700'  or  ['HK.00700', 'HK.00001']
 :param dates: 单个或多个日期 '2017-01-01' or ['2017-01-01', '2017-01-02']，最多5个时间点
 :param fields: 单个或多个数据列 KL_FIELD.ALL or [KL_FIELD.DATE_TIME, KL_FIELD.OPEN]
 :param ktype: K线类型 KLType_
 :param autype: 复权类型 AuType_ 
 :param no_data_mode: 指定时间为非交易日时，对应的k线数据取值模式，参见 KLNoDataMode_
 :return: (ret, data)

        ret == RET_OK 返回pd dataframe数据，固定表头包括'code'(代码) 'time_point'(指定的日期) 'data_status' (KLDataStatus)。数据列格式如下

        ret != RET_OK 返回错误字符串

    =================   ===========   ==============================================================================
    参数                  类型                        说明
    =================   ===========   ==============================================================================
    code                str            股票代码
    time_point          str            请求的时间（美股默认是美东时间，港股A股默认是北京时间）
    data_status         str            数据点是否有效，参见 KLDataStatus_
    time_key            str            k线时间（美股默认是美东时间，港股A股默认是北京时间）
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
    
 :Example:

 .. code:: python

    from futu import *
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    print(quote_ctx.get_multi_points_history_kline(['HK.00700'], '2017-06-20', '2017-06-25', KL_FIELD.ALL, KLType.K_DAY, AuType.QFQ))
    quote_ctx.close()	
	
	
	
get_referencestock_list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: get_referencestock_list(self, code, reference_type)


 获取证券的关联数据
 
 :param code: 证券id，str，例如HK.00700
 :param reference_type: 要获得的相关数据，参见 SecurityReferenceType_ 。例如WARRANT，表示获取正股相关的涡轮
 :return: (ret, data)

		ret == RET_OK 返回pd dataframe数据，数据列格式如下

		ret != RET_OK 返回错误字符串
		
		=================   ===========   ==============================================================================
		参数                  类型                        说明
		=================   ===========   ==============================================================================
		code                str            证券代码
		lot_size            int            每手数量
		stock_type          str            证券类型，参见 SecurityType_
		stock_name          str            证券名字
		list_time           str            上市时间（美股默认是美东时间，港股A股默认是北京时间）
		wrt_valid           bool           是否是窝轮，如果为True，下面wrt开头的字段有效
		wrt_type            str            窝轮类型，参见 WrtType_
		wrt_code            str            所属正股
		=================   ===========   ==============================================================================
		
 :Example:

 .. code:: python

    from futu import *
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    print(quote_ctx.get_referencestock_list('HK.00700', SecurityReferenceType.WARRANT))
    quote_ctx.close()	


get_owner_plate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: get_owner_plate(self, code_list)

 获取单支或多支股票的所属板块信息列表

 :param code_list: 股票代码列表，仅支持正股、指数。list或str。例如：['HK.00700', 'HK.00001']或者'HK.00700,HK.00001'，最多可传入200只股票
 :return: (ret, data)

        ret == RET_OK 返回pd dataframe数据，data.DataFrame数据, 数据列格式如下

        ret != RET_OK 返回错误字符串

        =====================   ===========   ==============================================================
        参数                      类型                        说明
        =====================   ===========   ==============================================================
        code                    str            证券代码
        plate_code              str            板块代码
        plate_name              str            板块名字
        plate_type              str            板块类型（行业板块或概念板块），查看 Plate_
        =====================   ===========   ==============================================================

 :Example:

 .. code:: python

    from futu import *
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    code_list = ['HK.00700', 'HK.00001']
    print(quote_ctx.get_owner_plate(code_list))
    quote_ctx.close()

get_holding_change_list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: get_holding_change_list(self, code, holder_type, start, end=None)

 获取大股东持股变动列表,只提供美股数据,并最多只返回前100个

 :param code: 股票代码. 例如：'US.AAPL'
 :param holder_type: 持有者类别，查看 StockHolder_
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
        holding_qty             float         持股数
        holding_ratio           float         持股比例（该字段为比例字段，默认不展示%）
        change_qty              float         变动数
        change_ratio            float         变动比例（该字段为比例字段，默认不展示%）
        time                    str           发布时间（美股的时间默认是美东）
        =====================   ===========   ==============================================================

 :Example:

 .. code:: python

    from futu import *
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    print(quote_ctx.get_holding_change_list('US.AAPL', StockHolder.INSTITUTE, '2016-10-01'))
    quote_ctx.close()

get_order_detail
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: get_order_detail(self, code)

 查询A股Level 2权限下提供的委托明细

 :param code: 股票代码,例如：'SZ.000001'
 :return: (ret, data)

          ret == RET_OK data为1个dict，包含以下数据::
		
           {
            "code": 股票代码,
            "Ask": [ order_num, [order_volume1, order_volume2, ...] ]
            "Bid": [ order_num, [order_volume1, order_volume2, ...] ]
           }

          | "Ask": 卖盘 
          | "Bid": 买盘
          | order_num：委托订单数量
          | order_volume：是每笔委托的委托量，当前最多返回前50笔委托的委托数量。即order_num有可能多于后面的order_volume

          ret != RET_OK data为错误字符串
        
 :Example:

 .. code:: python

    from futu import *
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    quote_ctx.subscribe('SZ.000001', SubType.ORDER_DETAIL)
    print(quote_ctx.get_order_detail('SZ.000001')
    quote_ctx.close()

	
get_option_chain
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: get_option_chain(self, code, start, end=None, option_type=OptionType.ALL, option_cond_type=OptionCondType.ALL)

 通过标的股查询期权

 :param code: 股票代码,例如：'HK.02318'
 :param start: 开始日期，该日期指到期日，例如'2017-08-01'
 :param end: 结束日期（包括这一天），该日期指到期日，例如'2017-08-30'。 注意，时间范围最多30天。
             start和end的组合如下：
			 
                ==========    ==========    ========================================
                 start类型      end类型       说明
                ==========    ==========    ========================================
                 str            str           start和end分别为指定的日期
                 None           str           start为end往前30天
                 str            None          end为start往后30天
                 None           None          start为当前日期，end往后30天
                ==========    ==========    ========================================
				
 :param option_type: 期权类型,,默认全部,全部/看涨/看跌，查看 OptionType_
 :param option_cond_type: 默认全部,全部/价内/价外，查看 OptionCondType_
 :return: (ret, data)

        ret == RET_OK 返回pd dataframe数据，数据列格式如下

        ret != RET_OK 返回错误字符串

        ==================   ===========   ==============================================================
        参数                      类型                        说明
        ==================   ===========   ==============================================================
        code                 str           股票代码
        name                 str           名字
        lot_size             int           每手数量
        stock_type           str           股票类型，参见 SecurityType_
        option_type          str           期权类型，查看 OptionType_
        stock_owner          str           标的股
        strike_time          str           行权日（美股默认是美东时间，港股A股默认是北京时间）
        strike_price         float         行权价
        suspension           bool          是否停牌(True表示停牌)
        stock_id             int           股票id
        ==================   ===========   ==============================================================

 :Example:

 .. code:: python

    from futu import *
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    print(quote_ctx.get_option_chain('US.AAPL', '2018-08-01', '2018-08-18', OptionType.ALL, OptionCondType.OUTSIDE))
    quote_ctx.close()

---------------------------------------------------------------------    


SysNotifyHandlerBase - OpenD通知回调处理类
-------------------------------------------

通知OpenD一些重要消息，类似连接断开等。

.. code:: python
    
    from futu import *
	
    class SysNotifyTest(SysNotifyHandlerBase):
        def on_recv_rsp(self, rsp_str):
            ret_code, data = super(SysNotifyTest, self).on_recv_rsp(rsp_pb)
            notify_type, sub_type, msg = data
            if ret_code != RET_OK:
                logger.debug("SysNotifyTest: error, msg: %s" % msg)
                return RET_ERROR, data
            print(msg)
            return RET_OK, data
			
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    handler = SysNotifyTest()
    quote_ctx.set_handler(handler)
                
-------------------------------------------

on_recv_rsp
~~~~~~~~~~~

..  py:function:: on_recv_rsp(self, rsp_pb)

 在收到OpenD通知推送后会回调到该函数，使用者需要在派生类中覆盖此方法

 注意该回调是在独立子线程中

 :param rsp_pb: 派生类中不需要直接处理该参数
 :return: ret_code, notify_type, sub_type, msg
 
==================   ===========   ===========
参数                 类型          说明
==================   ===========   ===========
notify_type          int           通知类型
sub_type             int           消息类型
msg              	 str           消息描述
==================   ===========   ===========
  
----------------------------

StockQuoteHandlerBase - 实时报价回调处理类
-------------------------------------------

异步处理推送的订阅股票的报价。

.. code:: python
    
    import time
    from futu import *
	
    class StockQuoteTest(StockQuoteHandlerBase):
        def on_recv_rsp(self, rsp_str):
            ret_code, data = super(StockQuoteTest,self).on_recv_rsp(rsp_str)
            if ret_code != RET_OK:
                print("StockQuoteTest: error, msg: %s" % data)
                return RET_ERROR, data

            print("StockQuoteTest ", data) # StockQuoteTest自己的处理逻辑

            return RET_OK, data
			
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    handler = StockQuoteTest()
    quote_ctx.set_handler(handler)
    quote_ctx.subscribe(['HK.00700'], [SubType.QUOTE])
    time.sleep(15)  
    quote_ctx.close()	
                
-------------------------------------------

on_recv_rsp
~~~~~~~~~~~

..  py:function:: on_recv_rsp(self, rsp_pb)

 在收到实时报价推送后会回调到该函数，使用者需要在派生类中覆盖此方法

 注意该回调是在独立子线程中

 :param rsp_pb: 派生类中不需要直接处理该参数
 :return: 参见 get_stock_quote_ 的返回值
    
----------------------------

OrderBookHandlerBase - 实时摆盘回调处理类
-------------------------------------------

异步处理推送的实时摆盘。

.. code:: python
    
    import time
    from futu import *
	
    class OrderBookTest(OrderBookHandlerBase):
        def on_recv_rsp(self, rsp_str):
            ret_code, data = super(OrderBookTest,self).on_recv_rsp(rsp_str)
            if ret_code != RET_OK:
                print("OrderBookTest: error, msg: %s" % data)
                return RET_ERROR, data

            print("OrderBookTest ", data) # OrderBookTest自己的处理逻辑

            return RET_OK, data
			
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    handler = OrderBookTest()
    quote_ctx.set_handler(handler)
    quote_ctx.subscribe(['HK.00700'], [SubType.ORDER_BOOK])
    time.sleep(15)  
    quote_ctx.close()
            
-------------------------------------------

on_recv_rsp
~~~~~~~~~~~

..  py:function:: on_recv_rsp(self, rsp_pb)


 在收到实摆盘数据推送后会回调到该函数，使用者需要在派生类中覆盖此方法

 注意该回调是在独立子线程中

 :param rsp_pb: 派生类中不需要直接处理该参数
 :return: 参见 get_order_book_ 的返回值
    
----------------------------

CurKlineHandlerBase - 实时k线推送回调处理类
-------------------------------------------

异步处理推送的k线数据。

.. code:: python

    import time
    from futu import *

    class CurKlineTest(CurKlineHandlerBase):
        def on_recv_rsp(self, rsp_str):
            ret_code, data = super(CurKlineTest,self).on_recv_rsp(rsp_str)
            if ret_code != RET_OK:
                print("CurKlineTest: error, msg: %s" % data)
                return RET_ERROR, data

            print("CurKlineTest ", data) # CurKlineTest自己的处理逻辑

            return RET_OK, data

    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    handler = CurKlineTest()
    quote_ctx.set_handler(handler)
    quote_ctx.subscribe(['HK.00700'], [SubType.K_1M])
    time.sleep(15)  
    quote_ctx.close()			

-------------------------------------------

on_recv_rsp
~~~~~~~~~~~

..  py:function:: on_recv_rsp(self, rsp_pb)


 在收到实时k线数据推送后会回调到该函数，使用者需要在派生类中覆盖此方法

 注意该回调是在独立子线程中

 :param rsp_pb: 派生类中不需要直接处理该参数
 :return: 参见 get_cur_kline_ 的返回值，推送回调比 get_cur_kline_ 少了市盈率和换手率字段
    
----------------------------

TickerHandlerBase - 实时逐笔推送回调处理类
-------------------------------------------

异步处理推送的逐笔数据。

.. code:: python
    
	import time
	from futu import *
	
	class TickerTest(TickerHandlerBase):
		def on_recv_rsp(self, rsp_str):
			ret_code, data = super(TickerTest,self).on_recv_rsp(rsp_str)
			if ret_code != RET_OK:
				print("CurKlineTest: error, msg: %s" % data)
				return RET_ERROR, data

			print("TickerTest ", data) # TickerTest自己的处理逻辑

			return RET_OK, data
                
	quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
	handler = TickerTest()
	quote_ctx.set_handler(handler)
	quote_ctx.subscribe(['HK.00700'], [SubType.TICKER])
	time.sleep(15)  
	quote_ctx.close()
	
.. note::

    * 行情连接断开重连后，OpenD拉取断开期间的逐笔数据（最多50根）并推送，可通过push_data_type字段区分

-------------------------------------------

on_recv_rsp
~~~~~~~~~~~

..  py:function:: on_recv_rsp(self, rsp_pb)


 在收到实时逐笔数据推送后会回调到该函数，使用者需要在派生类中覆盖此方法

 注意该回调是在独立子线程中

 :param rsp_pb: 派生类中不需要直接处理该参数
 :return: 参见 get_rt_ticker_ 的返回值，回调比get_rt_ticker多返回一个字段：push_data_type，该字段指明数据来源，参见 PushDataType_

----------------------------

RTDataHandlerBase - 实时分时推送回调处理类
-------------------------------------------

异步处理推送的分时数据。

.. code:: python
    
	import time
	from futu import *
	
	class RTDataTest(RTDataHandlerBase):
		def on_recv_rsp(self, rsp_str):
			ret_code, data = super(RTDataTest,self).on_recv_rsp(rsp_str)
			if ret_code != RET_OK:
				print("RTDataTest: error, msg: %s" % data)
				return RET_ERROR, data

			print("RTDataTest ", data) # RTDataTest自己的处理逻辑

			return RET_OK, data
                
	quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
	handler = RTDataTest()
	quote_ctx.set_handler(handler)
	quote_ctx.subscribe(['HK.00700'], [SubType.RT_DATA])
	time.sleep(15)  
	quote_ctx.close()
	
-------------------------------------------

on_recv_rsp
~~~~~~~~~~~

..  py:function:: on_recv_rsp(self, rsp_pb)


 在收到实时逐笔数据推送后会回调到该函数，使用者需要在派生类中覆盖此方法

 注意该回调是在独立子线程中

 :param rsp_pb: 派生类中不需要直接处理该参数
 :return: 参见 get_rt_data_ 的返回值

----------------------------

BrokerHandlerBase - 实时经纪推送回调处理类
-------------------------------------------

异步处理推送的经纪数据。

.. code:: python
    
    class BrokerTest(BrokerHandlerBase):
        def on_recv_rsp(self, rsp_str):
            ret_code, err_or_stock_code, data = super(BrokerTest, self).on_recv_rsp(rsp_str)
            if ret_code != RET_OK:
                print("BrokerTest: error, msg: {}".format(err_or_stock_code))
                return RET_ERROR, data

            print("BrokerTest: stock: {} data: {} ".format(err_or_stock_code, data))  # BrokerTest自己的处理逻辑

            return RET_OK, data


    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    handler = BrokerTest()
    quote_ctx.set_handler(handler)
    quote_ctx.subscribe(['HK.00700'], [SubType.BROKER])
    time.sleep(15)
    quote_ctx.close()
	
-------------------------------------------

on_recv_rsp
~~~~~~~~~~~

..  py:function:: on_recv_rsp(self, rsp_pb)


 在收到实时经纪数据推送后会回调到该函数，使用者需要在派生类中覆盖此方法

 注意该回调是在独立子线程中

 :param rsp_pb: 派生类中不需要直接处理该参数
 :return: 成功时返回(RET_OK, stock_code, [bid_frame_table, ask_frame_table]), 相关frame table含义见 get_broker_queue_ 的返回值说明

          失败时返回(RET_ERROR, ERR_MSG, None)

----------------------------    

OrderDetailHandlerBase - A股委托明细推送回调处理类
--------------------------------------------------

异步处理推送的A股委托明细数据。

.. code:: python
    
    class OrderDetailTest(OrderDetailHandlerBase):
        def on_recv_rsp(self, rsp_str):
            ret_code, err_or_stock_code, data = super(OrderDetailTest, self).on_recv_rsp(rsp_str)
            if ret_code != RET_OK:
                print("OrderDetailTest: error, msg: {}".format(err_or_stock_code))
                return RET_ERROR, data

            print("OrderDetailTest: stock: {} data: {} ".format(err_or_stock_code, data))  # OrderDetailTest

            return RET_OK, data


    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    handler = OrderDetailTest()
    quote_ctx.set_handler(handler)
    quote_ctx.subscribe(['SZ.000001'], [SubType.ORDER_DETAIL])
    time.sleep(15)
    quote_ctx.close()
	
-------------------------------------------

on_recv_rsp
~~~~~~~~~~~

..  py:function:: on_recv_rsp(self, rsp_pb)


 在收到委托明细数据推送后会回调到该函数，使用者需要在派生类中覆盖此方法

 注意该回调是在独立子线程中

 :param rsp_pb: 派生类中不需要直接处理该参数
 :return: 参见 get_order_detail_ 的返回值说明

----------------------------    


接口入参限制
============ 

 ===============================        =====================================================
 接口名称                               入参限制
 ===============================        =====================================================
 get_market_snapshot                    参考 `OpenAPI用户等级权限 <Quote_API.html#id12>`_
 get_rt_ticker				            可获取逐笔最多最近1000个
 get_cur_kline				            可获取K线最多最近1000根
 get_multi_points_history_kline         时间点最多5个
 get_owner_plate                        传入股票最多200个
 ===============================        =====================================================

----------------------------

接口限频
========

低频数据接口
------------

低频数据接口是指不需要订阅就可以请求数据的接口， api的请求到达网关客户端后， 会转发请求到futu后台服务器，为控制流量，会对请求频率加以控制，
目前的频率限制是以连续30秒内，限制请求次数，有限制的接口以及限制次数如下:

 ==========================        ==================================================
 接口名称                          连续30秒内次数限制
 ==========================        ==================================================
 get_market_snapshot               参考 `OpenAPI用户等级权限 <Quote_API.html#id12>`_
 get_plate_list                    10
 get_plate_stock                   10
 get_option_chain                  10
 get_holding_change_list           10
 get_owner_plate                   10
 request_history_kline             10
 ==========================        ==================================================

---------------------------------------------------------------------

高频数据接口
------------

为控制订阅产生推送数据流量，股票订阅总量有额度控制，规则如下:

1.使用高频数据接口前，需要订阅（调用subscribe），订阅有额度限制：订阅类型数量*股票数量不可超过订阅额度。
 
2.用户总额度与用户等级相关，参考 `OpenAPI用户等级权限 <Quote_API.html#id12>`_。

3.订阅至少一分钟才可以反订阅。

---------------------------------------------------------------------

OpenAPI用户等级权限
----------------------
 
 用户净资产大于10000港币为二级用户，小于10000港币为三级用户。一级用户需要与富途联系获取。

 ======================================        =========================        =========================        =========================
 协议限制                                      三级用户                         二级用户                         一级用户
 ======================================        =========================        =========================        =========================
 订阅额度                                      100                              300                              1000
 30秒内快照请求次数                            10                               20                               30 
 快照每次请求股票数                            200                              300                              400
 30天内非本地历史K线最多可请求股票数           100                              300                              1000                                                                  
 ======================================        =========================        =========================        =========================























