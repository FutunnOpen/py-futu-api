基础API
========
 .. _ProtoFMT : #id2
 
------------------------------------

SysConfig - 系统配置
---------------------

..  py:class:: SysConfig

对python api系统参数进行配置

------------------------------------

set_client_info
~~~~~~~~~~~~~~~~~

..  py:function:: set_client_info(cls, client_id, client_ver)

  设置调用api的client信息, 非必调接口

  :param client_id: str, client的标识
  :param client_ver: int, client的版本号
  :return: None

  :example:

  .. code:: python

   from futu import *
   SysConfig.set_client_info("MyFutuAPI", 0)
   quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
   quote_ctx.close()
	
--------------------------------------------

set_proto_fmt
~~~~~~~~~~~~~~~~~

..  py:function:: set_proto_fmt(cls, proto_fmt)

  设置通讯协议body格式, 目前支持Protobuf | Json两种格式, 非必调接口

  :param proto_fmt: ProtoFMT_
  :return: None

  :example:

  .. code:: python

   from futu import *
   SysConfig.set_proto_fmt(ProtoFMT.Protobuf)
   quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
   quote_ctx.close()
         
--------------------------------------------
                 
enable_proto_encrypt
~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: enable_proto_encrypt(cls, is_encrypt)

  设置通讯协议是否加密, 网关客户端和api需配置相同的RSA私钥文件,在连接初始化成功后，网关会下发随机生成的AES 加密密钥

  :param is_encrypt: bool
  :return: None

  :example:

  .. code:: python

   from futu import *
   SysConfig.enable_proto_encrypt(True)
   SysConfig.set_init_rsa_file("conn_key.txt")   # rsa 私钥文件路径
   quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
   quote_ctx.close()

--------------------------------------------

set_init_rsa_file
~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: set_init_rsa_file(cls, file)

  设置RSA私钥文件, 要求1024位, 格式为PKCS#1

  :param file:  str, 文件路径
  :return: None

  :example:

  .. code:: python

   from futu import *
   SysConfig.enable_proto_encrypt(True)
   SysConfig.set_init_rsa_file("conn_key.txt")   # rsa 私钥文件路径
   quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
   quote_ctx.close()
   
   
--------------------------------------------

set_all_thread_daemon
~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: set_all_thread_daemon(cls, all_daemon)

  设置是否所有内部创建的线程都是daemon线程。在主线程退出后，如果其余线程都是daemon线程，则进程退出。否则进程仍会继续运行。如果不设置，默认内部会创建非daemon线程。默认情况下，行情和交易的context连接上FutuOpenD后，如果不调用close，即使主线程退出，进程也不会退出。因此，如果行情和交易的context设置了接收数据推送，并且也设置了daemon线程，则要自己保证主线程存活，否则进程将退出，也就不会再收到推送数据了。

  :param all_daemon:  bool, 是否所有内部线程都是daemon线程
  :return: None

  :example:

  .. code:: python

   from futu import *
   SysConfig.set_all_thread_daemon(True)
   quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
   # 不调用quote_ctx.close()，进程也会退出

--------------------------------------------


枚举常量
---------

ret_code - 接口返回值
~~~~~~~~~~~~~~~~~~~~~~

接口返回值定义

 ..  py:attribute:: RET_OK = 0
 
 ..  py:attribute:: RET_ERROR = -1

------------------------------------

ProtoFMT - 协议格式
~~~~~~~~~~~~~~~~~~~~~~

    协议格式类型
    
    ..  py:class:: ProtoFMT
    
     ..  py:attribute:: Protobuf
     
      google的protobuf格式
      
     ..  py:attribute:: Json
     
      json格式
      
------------------------------------

Market - 行情市场
~~~~~~~~~~~~~~~~~

标识不同的行情市场，股票名称的前缀复用该字符串,如 **'HK.00700'**, **'HK_FUTURE.999010'**

..  py:class:: Market

 ..  py:attribute:: HK    
    
  港股
  
 ..  py:attribute:: US
    
  美股
  
 ..  py:attribute:: SH  
    
  沪市
  
 ..  py:attribute:: SZ
    
  深市
  
 ..  py:attribute:: HK_FUTURE  
    
  港股期货
  
 ..  py:attribute:: NONE
    
  未知

--------------------------------------

MarketState - 行情市场状态
~~~~~~~~~~~~~~~~~~~~~~~~~~~

行情市场状态定义

..  py:class:: MarketState

 ..  py:attribute:: NONE
 
  无交易,美股未开盘
  
 ..  py:attribute:: AUCTION
 
  竞价
  
 ..  py:attribute:: WAITING_OPEN
 
  早盘前等待开盘
  
 ..  py:attribute:: MORNING
 
  早盘
  
 ..  py:attribute:: REST
 
  午间休市
  
 ..  py:attribute:: AFTERNOON
 
  午盘
  
 ..  py:attribute:: CLOSED
 
  收盘
  
 ..  py:attribute:: PRE_MARKET_BEGIN
 
  盘前开始
  
 ..  py:attribute:: PRE_MARKET_END
 
  盘前结束
  
 ..  py:attribute:: AFTER_HOURS_BEGIN
 
  盘后开始
  
 ..  py:attribute:: AFTER_HOURS_END
 
  盘后结束
  
 ..  py:attribute:: AFTER_HOURS_END
 
  盘后结束
  
 ..  py:attribute:: NIGHT_OPEN
 
  夜市开盘
  
 ..  py:attribute:: NIGHT_END
 
  夜市收盘
  
 ..  py:attribute:: FUTURE_DAY_OPEN
 
  期指日市开盘
  
 ..  py:attribute:: FUTURE_DAY_BREAK
 
  期指日市休市
  
 ..  py:attribute:: FUTURE_DAY_CLOSE
 
  期指日市收盘
  
 ..  py:attribute:: FUTURE_DAY_WAIT_OPEN
 
  期指日市等待开盘
  
 ..  py:attribute:: HK_CAS
 
  港股盘后竞价
  
--------------------------------------

SecurityType - 证券类型
~~~~~~~~~~~~~~~~~~~~~~~~~~~
  
证券类型定义

..  py:class:: SecurityType

 ..  py:attribute:: STOCK
 
  股票
  
 ..  py:attribute:: IDX
 
  指数
  
 ..  py:attribute:: ETF
 
  交易所交易基金(Exchange Traded Funds)
  
 ..  py:attribute:: WARRANT
 
  港股涡轮牛熊证
  
 ..  py:attribute:: BOND
 
  债券

 ..  py:attribute:: DRVT
 
  期权
   
 ..  py:attribute:: NONE
 
  未知
  
--------------------------------------

WrtType - 港股窝轮类型
~~~~~~~~~~~~~~~~~~~~~~~~~~~
  
港股窝轮类型定义

..  py:class:: WrtType

 ..  py:attribute:: CALL
 
  认购
  
 ..  py:attribute:: PUT
 
  认沽
  
 ..  py:attribute:: BULL
 
  牛证
  
 ..  py:attribute:: BEAR
 
  熊证
  
 ..  py:attribute:: NONE
 
  未知
  
--------------------------------------

SubType - 实时数据定阅类型
~~~~~~~~~~~~~~~~~~~~~~~~~~~

实时数据定阅类型定义

..  py:class:: SubType

 ..  py:attribute:: TICKER
 
  逐笔
  
 ..  py:attribute:: QUOTE
 
  报价
  
 ..  py:attribute:: ORDER_BOOK
 
  买卖摆盘
  
 ..  py:attribute:: K_1M
 
  1分钟K线
  
 ..  py:attribute:: K_5M
 
  5分钟K线
  
 ..  py:attribute:: K_15M
  
  15分钟K线
  
 ..  py:attribute:: K_30M
 
  30分钟K线
  
 ..  py:attribute:: K_60M
 
  60分钟K线
  
 ..  py:attribute:: K_DAY
 
  日K线
  
 ..  py:attribute:: K_WEEK
 
  周K线
  
 ..  py:attribute:: K_MON
 
  月K线
  
 ..  py:attribute:: RT_DATA
 
  分时
  
 ..  py:attribute:: BROKER
 
   买卖经纪
  
 ..  py:attribute:: ORDER_DETAIL
 
  委托摆盘明细
  

--------------------------------------

KLType - k线类型
~~~~~~~~~~~~~~~~~~~~~~~~~~~

k线类型定义

..  py:class:: KLType

 ..  py:attribute:: K_1M
 
  1分钟K线
  
 ..  py:attribute:: K_5M
 
  5分钟K线
  
 ..  py:attribute:: K_15M
 
  15分钟K线
  
 ..  py:attribute:: K_30M
 
  30分钟K线
  
 ..  py:attribute:: K_60M
 
  60分钟K线
  
 ..  py:attribute:: K_DAY
 
  日K线
  
 ..  py:attribute:: K_WEEK
 
  周K线
  
 ..  py:attribute:: K_MON
 
  月K线
  

--------------------------------------

KLDataStatus - k线数据状态
~~~~~~~~~~~~~~~~~~~~~~~~~~~

指定时间点取历史k线， 获得数据的实际状态

..  py:class:: KLDataStatus

 ..  py:attribute:: NONE
 
  无效数据
  
 ..  py:attribute:: CURRENT
 
  当前时间周期数据
  
 ..  py:attribute:: PREVIOUS
 
  前一时间周期数据
  
 ..  py:attribute:: BACK
 
  后一时间周期数据
  
  
--------------------------------------

AuType - K线复权类型
~~~~~~~~~~~~~~~~~~~~~~~~~~~

K线复权定义

..  py:class:: AuType

 ..  py:attribute:: QFQ
 
  前复权
  
 ..  py:attribute:: HFQ
 
  后复权
  
 ..  py:attribute:: NONE
 
  不复权
  

--------------------------------------

KLNoDataMode - K线数据取值模式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

指定时间为非交易日时，对应的k线数据取值模式

..  py:class:: KLNoDataMode

 ..  py:attribute:: NONE
 
  返回无数据
  
 ..  py:attribute:: FORWARD
 
  往前取数据
  
 ..  py:attribute:: BACKWARD
 
  往后取数据


--------------------------------------

KL_FIELD - K线数据字段
~~~~~~~~~~~~~~~~~~~~~~~~~~~

获取K线数据, 可指定需返回的字段

..  py:class:: KL_FIELD

 ..  py:attribute:: ALL
 
  所有字段
  
 ..  py:attribute:: DATE_TIME
 
  日期时间
  
 ..  py:attribute:: OPEN
 
  开盘价
  
 ..  py:attribute:: CLOSE
 
  收盘价
  
 ..  py:attribute:: HIGH
 
  最高价
  
 ..  py:attribute:: LOW
 
  最低价
  
 ..  py:attribute:: PE_RATIO
 
  市盈率
  
 ..  py:attribute:: TURNOVER_RATE
 
  换手率
  
 ..  py:attribute:: TRADE_VOL
 
  成交量
  
 ..  py:attribute:: TRADE_VAL
 
  成交额
  
 ..  py:attribute:: CHANGE_RATE
 
  涨跌比率
  
 ..  py:attribute:: LAST_CLOSE
 
  昨收价
  
  
--------------------------------------

TickerDirect - 逐笔方向
~~~~~~~~~~~~~~~~~~~~~~~~~~~

逐笔方向定义

..  py:class:: TickerDirect

 ..  py:attribute:: BUY
 
  买
  
 ..  py:attribute:: SELL
 
  卖
  
 ..  py:attribute:: NEUTRAL
 
  中性
  
  
--------------------------------------

TickerType - 逐笔类型
~~~~~~~~~~~~~~~~~~~~~~~~~~~

逐笔类型定义

..  py:class:: TickerType

	..  py:attribute:: AUTO_MATCH

	自动对盘

	..  py:attribute:: LATE

	开市前成交盘

	..  py:attribute:: NON_AUTO_MATCH

	非自动对盘

	..  py:attribute:: INTER_AUTO_MATCH

	同一证券商自动对盘

	..  py:attribute:: INTER_NON_AUTO_MATCH

	同一证券商非自动对盘

	..  py:attribute:: ODD_LOT

	碎股交易

	..  py:attribute:: AUCTION

	竞价交易

	..  py:attribute:: BULK

	批量交易

	..  py:attribute:: CRASH

	现金交易

	..  py:attribute:: CROSS_MARKET

	跨市场交易

	..  py:attribute:: BULK_SOLD

	批量卖出

	..  py:attribute:: FREE_ON_BOARD

	离价交易

	..  py:attribute:: RULE127_OR_155

	第127条交易（纽交所规则）或第155条交易

	..  py:attribute:: DELAY

	延迟交易

	..  py:attribute:: MARKET_CENTER_CLOSE_PRICE

	中央收市价

	..  py:attribute:: NEXT_DAY

	隔日交易

	..  py:attribute:: MARKET_CENTER_OPENING

	中央开盘价交易

	..  py:attribute:: PRIOR_REFERENCE_PRICE

	前参考价

	..  py:attribute:: MARKET_CENTER_OPEN_PRICE

	中央开盘价

	..  py:attribute:: SELLER

	卖方

	..  py:attribute:: T

	T类交易(盘前和盘后交易)

	..  py:attribute:: EXTENDED_TRADING_HOURS

	延长交易时段

	..  py:attribute:: CONTINGENT

	合单交易

	..  py:attribute:: AVERAGE_PRICE

	平均价成交

	..  py:attribute:: OTC_SOLD

	场外售出

	..  py:attribute:: ODD_LOT_CROSS_MARKET

	碎股跨市场交易

	..  py:attribute:: DERIVATIVELY_PRICED

	衍生工具定价

	..  py:attribute:: REOPENINGP_RICED

	再开盘定价

	..  py:attribute:: CLOSING_PRICED

	收盘定价

	..  py:attribute:: COMPREHENSIVE_DELAY_PRICE

	综合延迟价格
  
--------------------------------------

DarkStatus - 暗盘状态
~~~~~~~~~~~~~~~~~~~~~~~~~~~

暗盘状态定义

..  py:class:: DarkStatus

 ..  py:attribute:: NONE
 
  无暗盘交易
  
 ..  py:attribute:: TRADING
 
  暗盘交易中
  
 ..  py:attribute:: END
 
  暗盘交易结束
  

--------------------------------------

Plate - 板块集合分类
~~~~~~~~~~~~~~~~~~~~~~~~~~~

板块集合分类定义

..  py:class:: Plate

 ..  py:attribute:: ALL
 
  所有板块
  
 ..  py:attribute:: INDUSTRY
 
  行业板块
  
 ..  py:attribute:: REGION
 
  地域板块
  
 ..  py:attribute:: CONCEPT
 
  概念板块
  

--------------------------------------

StockHolder - 持有者类别
~~~~~~~~~~~~~~~~~~~~~~~~~~~

持有者类别定义

..  py:class:: StockHolder

 ..  py:attribute:: INSTITUTE
 
  机构
  
 ..  py:attribute:: FUND
 
  基金
  
 ..  py:attribute:: EXECUTIVE
 
  高管
  
  
--------------------------------------

OptionType - 期权类型
~~~~~~~~~~~~~~~~~~~~~~~~~~~

期权类型定义

..  py:class:: OptionType

 ..  py:attribute:: ALL
 
  全部
  
 ..  py:attribute:: CALL
 
  涨
  
 ..  py:attribute:: PUT
 
  跌
  
--------------------------------------

PushDataType - 推送数据类型
~~~~~~~~~~~~~~~~~~~~~~~~~~~

推送数据类型定义

..  py:class:: PushDataType

 ..  py:attribute:: REALTIME
 
  实时推送数据
  
 ..  py:attribute:: BYDISCONN
 
  行情连接断开重连后，OpenD拉取补充断开期间的数据，最多50根
  
 ..  py:attribute:: CACHE
 
  非实时推送数据，非连接断开补充数据
  
--------------------------------------

OptionCondType - 价内价外
~~~~~~~~~~~~~~~~~~~~~~~~~~~

价内价外定义

..  py:class:: OptionType

 ..  py:attribute:: ALL
 
  全部
  
 ..  py:attribute:: WITHIN
 
  价内
  
 ..  py:attribute:: OUTSIDE
 
  价外
  
  
--------------------------------------

SysNotifyType - 系统异步通知类型
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

系统异步通知类型定义

..  py:class:: SysNotifyType

 ..  py:attribute:: NONE
 
  未知
  
 ..  py:attribute:: GTW_EVENT
 
  网关事件
  

--------------------------------------

GtwEventType - 网关异步通知类型
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

网关异步通知类型定义

..  py:class:: GtwEventType

 ..  py:attribute:: LocalCfgLoadFailed
 
  本地配置文件加载失败
  
 ..  py:attribute:: APISvrRunFailed
 
  网关监听服务运行失败
  
 ..  py:attribute:: ForceUpdate
 
  强制升级网关
  
 ..  py:attribute:: LoginFailed
 
  登录牛牛服务器失败
  
 ..  py:attribute:: UnAgreeDisclaimer
 
  未同意免责声明，无法加运行
  
 ..  py:attribute:: NetCfgMissing
 
  缺少网络连接配置
  
 ..  py:attribute:: KickedOut
 
  登录被踢下线
  
 ..  py:attribute:: LoginPwdChanged
 
  登陆密码变更
  
 ..  py:attribute:: BanLogin
 
  牛牛后台不允许该账号登陆
  
 ..  py:attribute:: NeedPicVerifyCode
 
  登录需要输入图形验证码
  
 ..  py:attribute:: NeedPhoneVerifyCode
 
  登录需要输入手机验证码
  
 ..  py:attribute:: AppDataNotExist
 
  程序打包数据丢失
  
 ..  py:attribute:: NessaryDataMissing
 
  必要的数据没同步成功
  
 ..  py:attribute:: TradePwdChanged
 
  交易密码变更通知
  
 ..  py:attribute:: EnableDeviceLock
 
  需启用设备锁
  
--------------------------------------  
  
SecurityReferenceType - 股票关联数据类型
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

股票关联数据类型

 ..  py:class:: SecurityReferenceType
 
  ..  py:attribute:: NONE
  
   未知
   
  ..  py:attribute:: WARRANT
  
   相关窝轮

--------------------------------------

TrdEnv - 交易环境类型
~~~~~~~~~~~~~~~~~~~~~~~~~~~

交易环境类型定义

..  py:class:: TrdEnv

 ..  py:attribute:: REAL
 
  真实环境
  
 ..  py:attribute:: SIMULATE
 
  模拟环境


--------------------------------------

TrdMarket - 交易市场类型
~~~~~~~~~~~~~~~~~~~~~~~~~~~

交易市场类型定义

..  py:class:: TrdMarket

 ..  py:attribute:: NONE
 
  未知
  
 ..  py:attribute:: HK
 
  港股交易
  
 ..  py:attribute:: US

  美股交易
  
 ..  py:attribute:: CN

  A股交易
  
 ..  py:attribute:: HKCC

  香港的A股通交易  
 

--------------------------------------

PositionSide - 持仓方向类型
~~~~~~~~~~~~~~~~~~~~~~~~~~~

持仓方向类型定义

..  py:class:: PositionSide

 ..  py:attribute:: NONE
 
  未知
  
 ..  py:attribute:: LONG
 
  多仓
  
 ..  py:attribute:: SHORT
 
  空仓
  

--------------------------------------


OrderType - 订单类型
~~~~~~~~~~~~~~~~~~~~~~~~~~~

订单类型定义

..  py:class:: OrderType

 ..  py:attribute:: NONE
 
  未知
  
 ..  py:attribute:: NORMAL
  
  普通订单(港股的增强限价单、A股限价委托、美股的限价单)
  
 ..  py:attribute:: MARKET
 
  市价，目前仅美股
  
 ..  py:attribute:: ABSOLUTE_LIMIT
 
  港股限价单(只有价格完全匹配才成交)
  
 ..  py:attribute:: AUCTION
 
  港股竞价单
  
 ..  py:attribute:: AUCTION_LIMIT
 
  港股竞价限价单
  
 ..  py:attribute:: SPECIAL_LIMIT
 
  港股特别限价(即市价IOC, 订单到达交易所后，或全部成交， 或部分成交再撤单， 或下单失败)
  

--------------------------------------


OrderStatus - 订单状态定义
~~~~~~~~~~~~~~~~~~~~~~~~~~~

订单状态定义

..  py:class:: OrderStatus

 ..  py:attribute:: NONE
 
  未知
  
 ..  py:attribute:: UNSUBMITTED
  
  未提交
  
 ..  py:attribute:: WAITING_SUBMIT
 
  等待提交
  
 ..  py:attribute:: SUBMITTING
 
  提交中
  
 ..  py:attribute:: SUBMIT_FAILED
 
  提交失败，下单失败
  
 ..  py:attribute:: SUBMITTED
 
  已提交，等待成交
  
 ..  py:attribute:: FILLED_PART
 
  部分成交
  
 ..  py:attribute:: FILLED_ALL
 
  全部已成
  
 ..  py:attribute:: CANCELLING_PART
 
  正在撤单部分(部分已成交，正在撤销剩余部分)
  
 ..  py:attribute:: CANCELLING_ALL
 
  正在撤单全部
  
 ..  py:attribute:: CANCELLED_PART
 
  部分成交，剩余部分已撤单
  
 ..  py:attribute:: CANCELLED_ALL
 
  全部已撤单，无成交
  
 ..  py:attribute:: FAILED
 
  下单失败，服务拒绝
  
 ..  py:attribute:: DISABLED
 
  已失效
  
 ..  py:attribute:: DELETED
 
  已删除(无成交的订单才能删除)
  
  

--------------------------------------


ModifyOrderOp - 修改订单操作类型
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

修改订单操作类型定义

..  py:class:: ModifyOrderOp

 ..  py:attribute:: NONE
 
  未知
  
 ..  py:attribute:: NORMAL
  
  修改订单的数量、价格
  
 ..  py:attribute:: CANCEL
 
  取消订单
  
 ..  py:attribute:: DISABLE
 
  使订单失效
  
 ..  py:attribute:: ENABLE
 
  使订单生效
  
 ..  py:attribute:: DELETE
 
  删除订单
  

--------------------------------------


TrdSide - 交易方向类型
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

交易方向类型定义(客户端下单只传Buy或Sell即可，SELL_SHORT / BUY_BACK 服务器可能会传回)

..  py:class:: TrdSide

 ..  py:attribute:: NONE
 
  未知
  
 ..  py:attribute:: BUY
  
  买
  
 ..  py:attribute:: SELL
 
  卖
  
 ..  py:attribute:: SELL_SHORT
 
  卖空
  
 ..  py:attribute:: BUY_BACK
 
  买回
  


