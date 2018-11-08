行情协议
==========
	这里对FutuOpenD开放的行情协议接口作出归档说明。

.. note::

    *   为避免增删导致的版本兼容问题，所有enum枚举类型只用于值的定义，在protobuf结构体中声明类型时使用int32类型
    *   所有类型定义使用protobuf格式声明，不同语言对接时请自行通过相关工具转换成对应的头文件
    *   XXX.proto表示协议文件名, 点击超链接可打开github上的协议文件，每条协议内容以github上的为准，此文档更新可能存在滞后

--------------

`Qot_Sub.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_Sub.proto>`_ - 3001订阅或者反订阅
---------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Qot_Sub;

	import "Common.proto";
	import "Qot_Common.proto";

	message C2S
	{
		repeated Qot_Common.Security securityList = 1; //股票
		repeated int32 subTypeList = 2; //Qot_Common.SubType,订阅数据类型
		required bool isSubOrUnSub = 3; //ture表示订阅,false表示反订阅
		optional bool isRegOrUnRegPush = 4; //是否注册或反注册该连接上面行情的推送,该参数不指定不做注册反注册操作
		repeated int32 regPushRehabTypeList = 5; //Qot_Common.RehabType,复权类型,注册推送并且是K线类型才生效,其他订阅类型忽略该参数,注册K线推送时该参数不指定默认前复权
		optional bool isFirstPush = 6; //注册后如果本地已有数据是否首推一次已存在数据,该参数不指定则默认true
	}

	message S2C
	{
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;
				
		optional S2C s2c = 4;
	}
	
.. note::
	
	* 股票结构参考 `Security <base_define.html#security>`_
	* 订阅数据类型参考 `SubType <base_define.html#subtype>`_
	* 复权类型参考 `RehabType <base_define.html#rehabtype-k>`_
	* 为控制定阅产生推送数据流量，股票定阅总量有额度控制，订阅规则参考 `高频数据接口 <../api/Quote_API.html#id10>`_
	* 高频数据接口需要订阅之后才能使用，注册推送之后才可以收到数据更新推送
	
-------------------------------------

`Qot_RegQotPush.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_RegQotPush.proto>`_ - 3002注册行情推送
------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Qot_RegQotPush;

	import "Common.proto";
	import "Qot_Common.proto";

	message C2S
	{
		repeated Qot_Common.Security securityList = 1; //股票
		repeated int32 subTypeList = 2; //Qot_Common.SubType,要注册到该连接的订阅类型
		repeated int32 rehabTypeList = 3; //Qot_Common.RehabType,复权类型,注册K线类型才生效,其他订阅类型忽略该参数,注册K线时该参数不指定默认前复权
		required bool isRegOrUnReg = 4; //注册或取消
		optional bool isFirstPush = 5; //注册后如果本地已有数据是否首推一次已存在数据,该参数不指定则默认true
	}

	message S2C
	{
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;

		optional S2C s2c = 4;
	}
	
.. note::
	
	* 股票结构参考 `Security <base_define.html#security>`_
	* 订阅数据类型参考 `SubType <base_define.html#subtype>`_
	* 复权类型参考 `RehabType <base_define.html#rehabtype-k>`_
	* 行情需要订阅成功才能注册推送
	
-------------------------------------

`Qot_GetSubInfo.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_GetSubInfo.proto>`_ - 3003获取订阅信息
---------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Qot_GetSubInfo;

	import "Common.proto";
	import "Qot_Common.proto";

	message C2S
	{
		optional bool isReqAllConn = 1; //是否返回所有连接的订阅状态,不传或者传false只返回当前连接数据
	}

	message S2C
	{
		repeated Qot_Common.ConnSubInfo connSubInfoList = 1; //订阅订阅信息
		required int32 totalUsedQuota = 2; //FutuOpenD已使用的订阅额度
		required int32 remainQuota = 3; //FutuOpenD剩余订阅额度
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}
	
.. note::
	
	* 订阅信息结构参考 `ConnSubInfo <base_define.html#connsubinfo>`_
	
-------------------------------------

`Qot_GetBasicQot.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_GetBasicQot.proto>`_ - 3004获取股票基本行情
---------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Qot_GetBasicQot;

	import "Common.proto";
	import "Qot_Common.proto";

	message C2S
	{
		repeated Qot_Common.Security securityList = 1; //股票
	}

	message S2C
	{
		repeated Qot_Common.BasicQot basicQotList = 1; //股票基本报价
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}
	
.. note::
	
	* 股票结构参考 `Security <base_define.html#security>`_
	* 基本报价结构参考 `BasicQot <base_define.html#basicqot>`_
	
-------------------------------------

`Qot_UpdateBasicQot.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_UpdateBasicQot.proto>`_ - 3005推送股票基本报价
-------------------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Qot_UpdateBasicQot;

	import "Common.proto";
	import "Qot_Common.proto";

	message S2C
	{
		repeated Qot_Common.BasicQot basicQotList = 1; //股票基本行情
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}
	
.. note::
	
	* 基本报价结构参考 `BasicQot <base_define.html#basicqot>`_
	
-------------------------------------

`Qot_GetKL.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_GetKL.proto>`_ - 3006获取K线
------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Qot_GetKL;

	import "Common.proto";
	import "Qot_Common.proto";

	message C2S
	{
		required int32 rehabType = 1; //Qot_Common.RehabType,复权类型
		required int32 klType = 2; //Qot_Common.KLType,K线类型
		required Qot_Common.Security security = 3; //股票
		required int32 reqNum = 4; //请求K线根数
	}

	message S2C
	{
		required Qot_Common.Security security = 1; //股票
		repeated Qot_Common.KLine klList = 2; //k线点
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;

		optional S2C s2c = 4;
	}
	
.. note::
	
	* 复权类型参考 `RehabType <base_define.html#rehabtype-k>`_
	* K线类型参考 `KLType <base_define.html#kltype-k>`_
	* 股票结构参考 `Security <base_define.html#security>`_
	* K线结构参考 `KLine <base_define.html#kline-k>`_
	* 请求K线目前最多最近1000根
	
-------------------------------------

`Qot_UpdateKL.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_UpdateKL.proto>`_ - 3007推送K线
-------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Qot_UpdateKL;

	import "Common.proto";
	import "Qot_Common.proto";

	message S2C
	{
		required int32 rehabType = 1; //Qot_Common.RehabType,复权类型
		required int32 klType = 2; //Qot_Common.KLType,K线类型
		required Qot_Common.Security security = 3; //股票
		repeated Qot_Common.KLine klList = 4; //推送的k线点
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}
	
.. note::
	
	* 复权类型参考 `RehabType <base_define.html#rehabtype-k>`_
	* K线类型参考 `KLType <base_define.html#kltype-k>`_
	* 股票结构参考 `Security <base_define.html#security>`_
	* K线结构参考 `KLine <base_define.html#kline-k>`_
	
-------------------------------------

`Qot_GetRT.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_GetRT.proto>`_ - 3008获取分时
------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Qot_GetRT;

	import "Common.proto";
	import "Qot_Common.proto";

	message C2S
	{
		required Qot_Common.Security security = 1; //股票
	}

	message S2C
	{
		required Qot_Common.Security security = 1; //股票
		repeated Qot_Common.TimeShare rtList = 2; //分时点
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}
	
.. note::
	
	* 股票结构参考 `Security <base_define.html#security>`_
	* 分时结构参考 `TimeShare <base_define.html#timeshare>`_
	
-------------------------------------

`Qot_UpdateRT.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_UpdateRT.proto>`_ - 3009推送分时
-------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Qot_UpdateRT;

	import "Common.proto";
	import "Qot_Common.proto";

	message S2C
	{
		required Qot_Common.Security security = 1;
		repeated Qot_Common.TimeShare rtList = 2; //推送的分时点
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}
	
.. note::
	
	* 股票结构参考 `Security <base_define.html#security>`_
	* 分时结构参考 `TimeShare <base_define.html#timeshare>`_
	
-------------------------------------

`Qot_GetTicker.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_GetTicker.proto>`_ - 3010获取逐笔
---------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Qot_GetTicker;

	import "Common.proto";
	import "Qot_Common.proto";

	message C2S
	{
		required Qot_Common.Security security = 1; //股票
		required int32 maxRetNum = 2; //最多返回的逐笔个数,实际返回数量不一定会返回这么多,最多返回1000个
	}

	message S2C
	{
		required Qot_Common.Security security = 1; //股票
		repeated Qot_Common.Ticker tickerList = 2; //逐笔
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;
		optional S2C s2c = 4;
	}
	
.. note::
	
	* 股票结构参考 `Security <base_define.html#security>`_
	* 逐笔结构参考 `Ticker <base_define.html#ticker>`_
	* 请求逐笔目前最多最近1000个
	
-------------------------------------

`Qot_UpdateTicker.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_UpdateTicker.proto>`_ - 3011推送逐笔
---------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Qot_UpdateTicker;

	import "Common.proto";
	import "Qot_Common.proto";

	message S2C
	{
		required Qot_Common.Security security = 1; //股票
		repeated Qot_Common.Ticker tickerList = 2; //逐笔
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}
	
.. note::
	
	* 股票结构参考 `Security <base_define.html#security>`_
	* 逐笔结构参考 `Ticker <base_define.html#ticker>`_
-------------------------------------

`Qot_GetOrderBook.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_GetOrderBook.proto>`_ - 3012获取买卖盘
---------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Qot_GetOrderBook;

	import "Common.proto";
	import "Qot_Common.proto";

	message C2S
	{
		required Qot_Common.Security security = 1; //股票
		required int32 num = 2; //请求的摆盘个数(1~10)
	}

	message S2C
	{
		required Qot_Common.Security security = 1; //股票
		repeated Qot_Common.OrderBook orderBookAskList = 2; //卖盘
		repeated Qot_Common.OrderBook orderBookBidList = 3; //买盘
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;
		optional S2C s2c = 4;
	}

.. note::

	* 股票结构参考 `Security <base_define.html#security>`_
	* 买卖盘结构参考 `OrderBook <base_define.html#orderbook>`_
	
-------------------------------------

`Qot_UpdateOrderBook.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_UpdateOrderBook.proto>`_ - 3013推送买卖盘
---------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Qot_UpdateOrderBook;

	import "Common.proto";
	import "Qot_Common.proto";

	message S2C
	{
		required Qot_Common.Security security = 1; //股票
		repeated Qot_Common.OrderBook orderBookAskList = 2; //卖盘
		repeated Qot_Common.OrderBook orderBookBidList = 3; //买盘
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}

.. note::

	* 股票结构参考 `Security <base_define.html#security>`_
	* 买卖盘结构参考 `OrderBook <base_define.html#orderbook>`_
	
-------------------------------------

`Qot_GetBroker.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_GetBroker.proto>`_ - 3014获取经纪队列
---------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Qot_GetBroker;

	import "Common.proto";
	import "Qot_Common.proto";

	message C2S
	{
		required Qot_Common.Security security = 1; //股票
	}

	message S2C
	{
		required Qot_Common.Security security = 1; //股票
		repeated Qot_Common.Broker brokerAskList = 2; //经纪Ask(卖)盘
		repeated Qot_Common.Broker brokerBidList = 3; //经纪Bid(买)盘
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;
		optional S2C s2c = 4;
	}
	
.. note::

	* 股票结构参考 `Security <base_define.html#security>`_
	* 经纪队列结构参考 `Broker <base_define.html#broker>`_
-------------------------------------

`Qot_UpdateBroker.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_UpdateBroker.proto>`_ - 3015推送经纪队列
---------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Qot_UpdateBroker;

	import "Common.proto";
	import "Qot_Common.proto";

	message S2C
	{
		required Qot_Common.Security security = 1; //股票
		repeated Qot_Common.Broker brokerAskList = 2; //经纪Ask(卖)盘
		repeated Qot_Common.Broker brokerBidList = 3; //经纪Bid(买)盘
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}
	
.. note::

	* 股票结构参考 `Security <base_define.html#security>`_
	* 经纪队列结构参考 `Broker <base_define.html#broker>`_	
-------------------------------------

`Qot_GetOrderDetail.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_GetDetail.proto>`_ - 3016获取委托明细
---------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Qot_GetOrderDetail;

	import "Common.proto";
	import "Qot_Common.proto";

	message C2S
	{
		required Qot_Common.Security security = 1; //股票
	}

	message S2C
	{
		required Qot_Common.Security security = 1; //股票
		repeated Qot_Common.OrderDetail orderDetailAsk = 2; //卖盘
		repeated Qot_Common.OrderDetail orderDetailBid = 3; //买盘
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;
		optional S2C s2c = 4;
	}
    
.. note::

	* 股票结构参考 `Security <base_define.html#security>`_
	* 委托明细结构参考 `OrderDetail <base_define.html#orderdetail>`_
	
-------------------------------------

`Qot_UpdateDetail.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_UpdateDetail.proto>`_ - 3017推送委托明细
---------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Qot_UpdateOrderDetail;

	import "Common.proto";
	import "Qot_Common.proto";

	message S2C
	{
		required Qot_Common.Security security = 1; //股票
		repeated Qot_Common.OrderDetail orderDetailAsk = 2; //卖盘
		repeated Qot_Common.OrderDetail orderDetailBid = 3; //买盘
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}

.. note::

	* 股票结构参考 `Security <base_define.html#security>`_
	* 委托明细结构参考 `OrderDetail <base_define.html#orderdetail>`_
	
-------------------------------------

`Qot_GetHistoryKL.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_GetHistoryKL.proto>`_ - 3100获取单只股票一段历史K线
------------------------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Qot_GetHistoryKL;

	import "Common.proto";
	import "Qot_Common.proto";

	message C2S
	{
		required int32 rehabType = 1; //Qot_Common.RehabType,复权类型
		required int32 klType = 2; //Qot_Common.KLType,K线类型
		required Qot_Common.Security security = 3; //股票市场以及股票代码
		required string beginTime = 4; //开始时间字符串
		required string endTime = 5; //结束时间字符串
		optional int32 maxAckKLNum = 6; //最多返回多少根K线，如果未指定表示不限制
		optional int64 needKLFieldsFlag = 7; //指定返回K线结构体特定某几项数据，KLFields枚举值或组合，如果未指定返回全部字段
	}

	message S2C
	{
		required Qot_Common.Security security = 1;
		repeated Qot_Common.KLine klList = 2; //K线数据
		optional string nextKLTime = 3; //如请求不指定maxAckKLNum值，则不会返回该字段，该字段表示超过指定限制的下一K线时间字符串
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}

.. note::
	
	* 复权类型参考 `RehabType <base_define.html#rehabtype-k>`_
	* K线类型参考 `KLType <base_define.html#kltype-k>`_
	* 股票结构参考 `Security <base_define.html#security>`_
	* K线结构参考 `KLine <base_define.html#kline-k>`_
	* K线字段类型参考 `KLFields <base_define.html#klfields-k>`_
	
-------------------------------------

`Qot_GetHistoryKLPoints.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_GetHistoryKLPoints.proto>`_  - 3101获取多只股票多点历史K线
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


.. code-block:: protobuf

	syntax = "proto2";
	package Qot_GetHistoryKLPoints;

	import "Common.proto";
	import "Qot_Common.proto";

	 //当请求时间点数据为空时，如何返回数据
	enum NoDataMode
	{
		NoDataMode_Null = 0; //直接返回空数据
		NoDataMode_Forward = 1; //往前取值，返回前一个时间点数据
		NoDataMode_Backward = 2; //向后取值，返回后一个时间点数据
	}

	 //这个时间点返回数据的状态以及来源
	enum DataStatus
	{
		DataStatus_Null = 0; //空数据
		DataStatus_Current = 1; //当前时间点数据
		DataStatus_Previous = 2; //前一个时间点数据
		DataStatus_Back = 3; //后一个时间点数据
	}

	message C2S
	{
		required int32 rehabType = 1; //Qot_Common.RehabType,复权类型
		required int32 klType = 2; //Qot_Common.KLType,K线类型
		required int32 noDataMode = 3; //NoDataMode,当请求时间点数据为空时，如何返回数据
		repeated Qot_Common.Security securityList = 4; //股票市场以及股票代码
		repeated string timeList = 5; //时间字符串
		optional int32 maxReqSecurityNum = 6; //最多返回多少只股票的数据，如果未指定表示不限制
		optional int64 needKLFieldsFlag = 7; //指定返回K线结构体特定某几项数据，KLFields枚举值或组合，如果未指定返回全部字段
	}

	message HistoryPointsKL
	{
		required int32 status = 1; //DataStatus,数据状态
		required string reqTime = 2; //请求的时间
		required Qot_Common.KLine kl = 3; //K线数据
	}

	message SecurityHistoryKLPoints
	{
		required Qot_Common.Security security = 1; //股票	
		repeated HistoryPointsKL klList = 2; //K线数据
	}

	message S2C
	{
		repeated SecurityHistoryKLPoints klPointList = 1; //多只股票的多点历史K线点
		optional bool hasNext = 2; //如请求不指定maxReqSecurityNum值，则不会返回该字段，该字段表示请求是否还有超过指定限制的数据
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}

.. note::
	
	* 复权类型参考 `RehabType <base_define.html#rehabtype-k>`_
	* K线类型参考 `KLType <base_define.html#kltype-k>`_
	* 股票结构参考 `Security <base_define.html#security>`_
	* K线结构参考 `KLine <base_define.html#kline-k>`_
	* K线字段类型参考 `KLFields <base_define.html#klfields-k>`_
	* 目前限制最多5个时间点，股票个数不做限制，但不建议传入过多股票，查询耗时过多会导致协议返回超时。
	
-------------------------------------

`Qot_GetRehab.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_GetRehab.proto>`_ - 3102获取复权信息
---------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Qot_GetRehab;

	import "Common.proto";
	import "Qot_Common.proto";

	message C2S
	{
		repeated Qot_Common.Security securityList = 1; //股票
	}

	enum CompanyAct
	{
		CompanyAct_None = 0; //无
		CompanyAct_Split = 1; //拆股		
		CompanyAct_Join = 2; //合股
		CompanyAct_Bonus = 4; //送股
		CompanyAct_Transfer = 8; //转赠股
		CompanyAct_Allot = 16; //配股	
		CompanyAct_Add = 32; //增发股
		CompanyAct_Dividend = 64; //现金分红
		CompanyAct_SPDividend = 128; //特别股息	
	}

	message Rehab
	{
		required string time = 1; //时间字符串
		required int64 companyActFlag = 2; //公司行动组合,指定某些字段值是否有效
		required double fwdFactorA = 3; //前复权因子A
		required double fwdFactorB = 4; //前复权因子B
		required double bwdFactorA = 5; //后复权因子A
		required double bwdFactorB = 6; //后复权因子B
		optional int32 splitBase = 7; //拆股(eg.1拆5，Base为1，Ert为5)
		optional int32 splitErt = 8;	
		optional int32 joinBase = 9; //合股(eg.50合1，Base为50，Ert为1)
		optional int32 joinErt = 10;	
		optional int32 bonusBase = 11; //送股(eg.10送3, Base为10,Ert为3)
		optional int32 bonusErt = 12;	
		optional int32 transferBase = 13; //转赠股(eg.10转3, Base为10,Ert为3)
		optional int32 transferErt = 14;	
		optional int32 allotBase = 15; //配股(eg.10送2, 配股价为6.3元, Base为10, Ert为2, Price为6.3)
		optional int32 allotErt = 16;	
		optional double allotPrice = 17;	
		optional int32 addBase = 18; //增发股(eg.10送2, 增发股价为6.3元, Base为10, Ert为2, Price为6.3)
		optional int32 addErt = 19;	
		optional double addPrice = 20;	
		optional double dividend = 21; //现金分红(eg.每10股派现0.5元,则该字段值为0.05)
		optional double spDividend = 22; //特别股息(eg.每10股派特别股息0.5元,则该字段值为0.05)
	}

	message SecurityRehab
	{
		required Qot_Common.Security security = 1; //股票
		repeated Rehab rehabList = 2; //复权信息
	}

	message S2C
	{
		repeated SecurityRehab securityRehabList = 1; //多支股票的复权信息
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}

.. note::
	
	* 股票结构参考 `Security <base_define.html#security>`_

-------------------------------------

`Qot_RequestHistoryKL.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_RequestHistoryKL.proto>`_ - 3103获取单只股票一段历史K线
------------------------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Qot_RequestHistoryKL;

	import "Common.proto";
	import "Qot_Common.proto";

	message C2S
	{
		required int32 rehabType = 1; //Qot_Common.RehabType,复权类型
		required int32 klType = 2; //Qot_Common.KLType,K线类型
		required Qot_Common.Security security = 3; //股票市场以及股票代码
		required string beginTime = 4; //开始时间字符串
		required string endTime = 5; //结束时间字符串
		optional int32 maxAckKLNum = 6; //最多返回多少根K线，如果未指定表示不限制
		optional int64 needKLFieldsFlag = 7; //指定返回K线结构体特定某几项数据，KLFields枚举值或组合，如果未指定返回全部字段
		optional bytes nextReqKey = 8; //分页请求key
	}

	message S2C
	{
		required Qot_Common.Security security = 1;
		repeated Qot_Common.KLine klList = 2; //K线数据
		optional bytes nextReqKey = 3; //分页请求key。一次请求没有返回所有数据时，下次请求带上这个key，会接着请求
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}

.. note::
	
	* 复权类型参考 `RehabType <base_define.html#rehabtype-k>`_
	* K线类型参考 `KLType <base_define.html#kltype-k>`_
	* 股票结构参考 `Security <base_define.html#security>`_
	* K线结构参考 `KLine <base_define.html#kline-k>`_
	* K线字段类型参考 `KLFields <base_define.html#klfields-k>`_
	* 请求最大个数参考OpenAPI用户等级权限
	* 分页请求的key。如果start和end之间的数据点多于max_count，那么后续请求时，要传入上次调用返回的page_req_key。初始请求时应该传None。
-------------------------------------

`Qot_GetTradeDate.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_GetTradeDate.proto>`_ - 3200获取市场交易日
------------------------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Qot_GetTradeDate;

	import "Common.proto";
	import "Qot_Common.proto";

	message C2S
	{
		required int32 market = 1; //Qot_Common.QotMarket,股票市场
		required string beginTime = 2; //开始时间字符串
		required string endTime = 3; //结束时间字符串
	}

	message TradeDate
	{
		required string time = 1; //时间字符串
	}

	message S2C
	{
		repeated TradeDate tradeDateList = 1; //交易日
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}

-------------------------------------

`Qot_GetStaticInfo.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_GetStaticInfo.proto>`_ - 3202获取股票静态信息
------------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Qot_GetStaticInfo;

	import "Common.proto";
	import "Qot_Common.proto";

	message C2S
	{
		optional int32 market = 1; //Qot_Common.QotMarket,股票市场
		optional int32 secType = 2; //Qot_Common.SecurityType,股票类型
		repeated Qot_Common.Security securityList = 3; //股票，若该字段存在，忽略其他字段，只返回该字段股票的静态信息
	}

	message S2C
	{
		repeated Qot_Common.SecurityStaticInfo staticInfoList = 1; //静态信息
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}
	
.. note::

	* 股票结构参考 `Security <base_define.html#security>`_
	* 市场类型参考 `QotMarket <base_define.html#qotmarket>`_
	* 股票静态信息结构参考 `SecurityStaticInfo <base_define.html#securitystaticbasic>`_
	
-------------------------------------

`Qot_GetSecuritySnapshot.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_GetSecuritySnapshot.proto>`_ - 3203获取股票快照
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
.. code-block:: protobuf

	syntax = "proto2";
	package Qot_GetSecuritySnapshot;

	import "Common.proto";
	import "Qot_Common.proto";

	message C2S
	{
		repeated Qot_Common.Security securityList = 1; //股票
	}

	 // 正股类型额外数据
	message EquitySnapshotExData
	{
		required int64 issuedShares = 1; // 发行股本,即总股本
		required double issuedMarketVal = 2; // 总市值 =总股本*当前价格
		required double netAsset = 3; // 资产净值
		required double netProfit = 4; // 盈利（亏损）
		required double earningsPershare = 5; // 每股盈利
		required int64 outstandingShares = 6; // 流通股本
		required double outstandingMarketVal = 7; // 流通市值 =流通股本*当前价格
		required double netAssetPershare = 8; // 每股净资产
		required double eyRate = 9; // 收益率
		required double peRate = 10; // 市盈率
		required double pbRate = 11; // 市净率
	}

	 // 涡轮类型额外数据
	message WarrantSnapshotExData
	{
		required double conversionRate = 1; //换股比率
		required int32 warrantType = 2; //Qot_Common.WarrantType,涡轮类型
		required double strikePrice = 3; //行使价
		required string maturityTime = 4; //到期日时间字符串
		required string endTradeTime = 5; //最后交易日时间字符串
		required Qot_Common.Security owner = 6; //所属正股 
		required double recoveryPrice = 7; //回收价
		required int64 streetVolumn = 8; //街货量
		required int64 issueVolumn = 9; //发行量
		required double streetRate = 10; //街货占比
		required double delta = 11; //对冲值
		required double impliedVolatility = 12; //引申波幅
		required double premium = 13; //溢价
	}

	 //基本快照数据
	message SnapshotBasicData
	{
		required Qot_Common.Security security = 1; //股票
		required int32 type = 2; //Qot_Common.SecurityType,股票类型
		required bool isSuspend = 3; //是否停牌
		required string listTime = 4; //上市时间字符串
		required int32 lotSize = 5; //每手数量
		required double priceSpread = 6; //向上价差
		required string updateTime = 7; //更新时间字符串
		required double highPrice = 8; //最新价
		required double openPrice = 9; //开盘价
		required double lowPrice = 10; //最低价
		required double lastClosePrice = 11; //昨收价
		required double curPrice = 12; //最新价
		required int64 volume = 13; //成交量
		required double turnover = 14; //成交额
		required double turnoverRate = 15; //换手率
	}

	message Snapshot
	{
		required SnapshotBasicData basic = 1; //快照基本数据
		optional EquitySnapshotExData equityExData = 2; //正股快照额外数据
		optional WarrantSnapshotExData warrantExData = 3; //窝轮快照额外数据
	}

	message S2C
	{
		repeated Snapshot snapshotList = 1; //股票快照
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}

.. note::

	* 股票结构参考 `Security <base_define.html#security>`_
	* 限频以及每次请求最大个数参考OpenAPI用户等级权限
	
-------------------------------------

`Qot_GetPlateSet.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_GetPlateSet.proto>`_ - 3204获取板块集合下的板块
-----------------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Qot_GetPlateSet;

	import "Common.proto";
	import "Qot_Common.proto";

	message C2S
	{
		required int32 market = 1; //Qot_Common.QotMarket,股票市场
		required int32 plateSetType = 2; //Qot_Common.PlateSetType,板块集合的类型
	}

	message S2C
	{
		repeated Qot_Common.PlateInfo plateInfoList = 1; //板块集合下的板块信息
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}
	
.. note::

	* 市场类型参考 `QotMarket <base_define.html#qotmarket>`_
	* 板块集合类型参考 `PlateSetType <base_define.html#platesettype>`_
	* 股票结构参考 `Security <base_define.html#security>`_
	* 板块信息结构参考  `PlateInfo <base_define.html#plateinfo>`_
	* 限频接口：30秒内最多10次	
	
-------------------------------------

`Qot_GetPlateSecurity.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_GetPlateSecurity.proto>`_ - 3205获取板块下的股票
------------------------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Qot_GetPlateSecurity;

	import "Common.proto";
	import "Qot_Common.proto";

	message C2S
	{
		required Qot_Common.Security plate = 1; //板块
	}

	message S2C
	{
		repeated Qot_Common.SecurityStaticInfo staticInfoList = 1; //板块下的股票静态信息
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}

.. note::
	
	* 股票结构参考 `Security <base_define.html#security>`_
	* 股票静态信息结构参考 `SecurityStaticInfo <base_define.html#securitystaticbasic>`_
	* 限频接口：30秒内最多10次
	
-------------------------------------

`Qot_GetReference.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_GetReference.proto>`_ - 3206 获取正股相关股票
---------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Qot_GetReference;

	import "Common.proto";
	import "Qot_Common.proto";

	enum ReferenceType
	{
		ReferenceType_Unknow = 0; 
		ReferenceType_Warrant = 1; //正股相关的窝轮
	}

	message C2S
	{
		required Qot_Common.Security security = 1; //股票
		required int32 referenceType = 2; // ReferenceType, 相关类型
	}

	message S2C
	{
		repeated Qot_Common.SecurityStaticInfo staticInfoList = 2; //相关股票列表
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}
	
.. note::
	
	* 股票结构参考 `Security <base_define.html#security>`_
	* 股票静态信息结构参考 `SecurityStaticInfo <base_define.html#securitystaticbasic>`_

-------------------------------------

`Qot_GetOwnerPlate.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_GetOwnerPlate.proto>`_ - 3207获取股票所属板块
------------------------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Qot_GetOwnerPlate;

	import "Common.proto";
	import "Qot_Common.proto";

	message C2S
	{
		repeated Qot_Common.Security securityList = 1; //股票
	}

	message SecurityOwnerPlate
	{
		required Qot_Common.Security security = 1; //股票
		repeated Qot_Common.PlateInfo plateInfoList = 2; //所属板块
	}

	message S2C
	{
		repeated SecurityOwnerPlate ownerPlateList = 1; //所属板块信息
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}


.. note::
	
	* 股票结构参考 `Security <base_define.html#security>`_
	* 板块信息结构参考  `PlateInfo <base_define.html#plateinfo>`_
	* 限频接口：30秒内最多10次	
	* 最多可传入200只股票
	* 仅支持正股和指数

-------------------------------------

`Qot_GetHoldingChangeList.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_GetHoldingChangeList.proto>`_ - 3208获取持股变化列表
------------------------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Qot_GetHoldingChangeList;

	import "Common.proto";
	import "Qot_Common.proto";

	message C2S
	{
		required Qot_Common.Security security = 1; //股票
		required int32 holderCategory = 2; //Qot_Common.HolderCategory 持有者类别
		//以下是发布时间筛选，不传返回所有数据，传了返回发布时间属于开始时间到结束时间段内的数据
		optional string beginTime = 3; //开始时间，严格按YYYY-MM-DD HH:MM:SS或YYYY-MM-DD HH:MM:SS.MS格式传
		optional string endTime = 4; //结束时间，严格按YYYY-MM-DD HH:MM:SS或YYYY-MM-DD HH:MM:SS.MS格式传
	}

	message S2C
	{
		required Qot_Common.Security security = 1; //股票
		repeated Qot_Common.ShareHoldingChange holdingChangeList = 2; //对应类别的持股变化列表（最多返回前100大股东的变化）
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;
		optional S2C s2c = 4;
	}

.. note::
	
	* 股票结构参考 `Security <base_define.html#security>`_
	* 持有者类别枚举参考  `HolderCategory <base_define.html#holdercategory>`_
	* 持股变化列表结构参考  `ShareHoldingChange <base_define.html#shareholdingchange>`_
	* 限频接口：30秒内最多10次	
	* 最多返回前100大股东的变化
	* 目前仅支持美股

`Qot_GetOptionChain.proto <https://github.com/FutunnOpen/futuquant/blob/master/futuquant/common/pb/Qot_GetOptionChain.proto>`_ - 3209获取期权链
------------------------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Qot_GetOptionChain;

	import "Common.proto";
	import "Qot_Common.proto";

	enum OptionCondType
	{
		OptionCondType_Unknow = 0;
		OptionCondType_WithIn = 1; //价内
		OptionCondType_Outside = 2; //价外
	}

	message C2S
	{
		required Qot_Common.Security owner = 1; //期权标的股
		optional int32 type = 2; //Qot_Common.OptionType,期权类型,可选字段,不指定则表示都返回
		optional int32 condition = 3; //OptionCondType,价内价外,可选字段,不指定则表示都返回
		required string beginTime = 4; //期权到期日开始时间
		required string endTime = 5; //期权到期日结束时间,时间跨度最多一个月
	}

	message OptionItem
	{
		optional Qot_Common.SecurityStaticInfo call = 1; //看涨,不一定有该字段,由请求条件决定
		optional Qot_Common.SecurityStaticInfo put = 2; //看跌,不一定有该字段,由请求条件决定
	}

	message OptionChain
	{
		required string strikeTime = 1; //行权日
		repeated OptionItem option = 2; //期权信息
	}

	message S2C
	{
		repeated OptionChain optionChain = 1; //期权链
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		required int32 retType = 1 [default = -400]; //RetType,返回结果
		optional string retMsg = 2;
		optional int32 errCode = 3;
		optional S2C s2c = 4;
	}

.. note::
	
	* 股票结构参考 `Security <base_define.html#security>`_
	* 期权类型参考 `OptionType <base_define.html#optiontype>`_
	* 股票静态信息结构参考 `SecurityStaticInfo <base_define.html#securitystaticbasic>`_
	* 限频接口：30秒内最多10次
	* 目前仅支持美股












