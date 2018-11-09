交易协议
==========
	这里对FutuOpenD开放的交易协议接口作出归档说明。

.. note::

    *   为避免增删导致的版本兼容问题，所有enum枚举类型只用于值的定义，在protobuf结构体中声明类型时使用int32类型
    *   所有类型定义使用protobuf格式声明，不同语言对接时请自行通过相关工具转换成对应的头文件
    *   XXX.proto表示协议文件名, 点击超链接可打开github上的协议文件，每条协议内容以github上的为准，此文档更新可能存在滞后
    *   **要实现交易功能，必须先执行“Trd_GetAccList.proto - 2001获取交易账户列表”，然后再执行“Trd_UnlockTrade.proto - 2005解锁对应账户交易功能”才能进行后续交易功能调用**

--------------

`Trd_GetAccList.proto <https://github.com/FutunnOpen/py-futu-api/tree/master/futu/common/pb/Trd_GetAccList.proto>`_ - 2001获取交易账户列表
-----------------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf
	
	syntax = "proto2";
	package Trd_GetAccList;

	import "Common.proto";
	import "Trd_Common.proto";

	message C2S
	{
		required uint64 userID = 1; //需要跟FutuOpenD登陆的牛牛用户ID一致，否则会返回失败
	}

	message S2C
	{
		repeated Trd_Common.TrdAcc accList = 1; //交易业务账户列表
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		//以下3个字段每条协议都有，注释说明在InitConnect.proto中
		required int32 retType = 1 [default = -400];
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}
 
.. note::

	* 业务账户结构参考 `TrdAcc <base_define.html#trdacc>`_
	
-------------------------------------

`Trd_UnlockTrade.proto <https://github.com/FutunnOpen/py-futu-api/tree/master/futu/common/pb/Trd_UnlockTrade.proto>`_ - 2005解锁或锁定交易
-----------------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Trd_UnlockTrade;

	import "Common.proto";

	message C2S
	{
		required bool unlock = 1; //true解锁交易，false锁定交易
		optional string pwdMD5 = 2; //交易密码的MD5转16进制(全小写)，解锁交易必须要填密码，锁定交易不需要验证密码，可不填
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
		//以下3个字段每条协议都有，注释说明在InitConnect.proto中
		required int32 retType = 1 [default = -400];
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}
	
.. note::

	* 除2001协议外，所有交易协议请求都需要FutuOpenD先解锁交易
	* 密码MD5方式获取请参考 `FutuOpenD配置 <../setup/FutuOpenDGuide.html#id6>`_ 内的login_pwd_md5字段
	* 解锁或锁定交易针对与FutuOpenD，只要有一个连接解锁，其他连接都可以调用交易接口
	* 强烈建议有实盘交易的用户使用加密通道，参考 `加密通信流程 <intro.html#id10>`_ 
	* 限频接口：30秒内最多10次
	
-------------------------------------


`Trd_SubAccPush.proto <https://github.com/FutunnOpen/py-futu-api/tree/master/futu/common/pb/Trd_SubAccPush.proto>`_ - 2008订阅接收交易账户的推送数据
-----------------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Trd_SubAccPush;

	import "Common.proto";

	message C2S
	{
		repeated uint64 accIDList = 1; //要接收推送数据的业务账号列表，全量非增量，即使用者请每次传需要接收推送数据的所有业务账号
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
		//以下3个字段每条协议都有，注释说明在InitConnect.proto中
		required int32 retType = 1 [default = -400];
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}
	
.. note::

	* 指定发送该协议的连接接收交易数据（订单状态，成交状态等）推送

-------------------------------------

`Trd_GetFunds.proto <https://github.com/FutunnOpen/py-futu-api/tree/master/futu/common/pb/Trd_GetFunds.proto>`_ - 2101获取账户资金
-----------------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Trd_GetFunds;

	import "Common.proto";
	import "Trd_Common.proto";

	message C2S
	{
		required Trd_Common.TrdHeader header = 1; //交易公共参数头
	}

	message S2C
	{
		required Trd_Common.TrdHeader header = 1; //交易公共参数头
		optional Trd_Common.Funds funds = 2; //账户资金
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		//以下3个字段每条协议都有，注释说明在InitConnect.proto中
		required int32 retType = 1 [default = -400];
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}

.. note::

	* 交易公共参数头结构参考 `TrdHeader <base_define.html#trdheader>`_
	* 账户资金结构参考 `Funds <base_define.html#funds>`_
	
-------------------------------------

`Trd_GetPositionList.proto <https://github.com/FutunnOpen/py-futu-api/tree/master/futu/common/pb/Trd_GetPositionList.proto>`_ - 2102获取持仓列表
-----------------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Trd_GetPositionList;

	import "Common.proto";
	import "Trd_Common.proto";

	message C2S
	{
		required Trd_Common.TrdHeader header = 1; //交易公共参数头
		optional Trd_Common.TrdFilterConditions filterConditions = 2; //过滤条件
		optional double filterPLRatioMin = 3; //过滤盈亏比例下限，高于此比例的会返回，如0.1，返回盈亏比例大于10%的持仓
		optional double filterPLRatioMax = 4; //过滤盈亏比例上限，低于此比例的会返回，如0.2，返回盈亏比例小于20%的持仓
	}

	message S2C
	{
		required Trd_Common.TrdHeader header = 1; //交易公共参数头
		repeated Trd_Common.Position positionList = 2; //持仓列表
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		//以下3个字段每条协议都有，注释说明在InitConnect.proto中
		required int32 retType = 1 [default = -400];
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}

.. note::

	* 交易公共参数头结构参考 `TrdHeader <base_define.html#trdheader>`_
	* 持仓资金结构参考 `Position <base_define.html#position>`_
	* 过滤条件结构参考 `TrdFilterConditions <base_define.html#trdfilterconditions>`_
	
-------------------------------------

`Trd_GetMaxTrdQtys.proto <https://github.com/FutunnOpen/py-futu-api/tree/master/futu/common/pb/Trd_GetMaxTrdQtys.proto>`_ - 2111获取最大交易数量
-----------------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Trd_GetMaxTrdQtys;

	import "Common.proto";
	import "Trd_Common.proto";

	message C2S
	{
		required Trd_Common.TrdHeader header = 1; //交易公共参数头
		required int32 orderType = 2; //订单类型, 参见Trd_Common.OrderType的枚举定义
		required string code = 3; //代码，港股必须是5位数字，A股必须是6位数字，美股没限制
		required double price = 4; //价格，3位精度。如果是竞价、市价单，请也填入一个当前价格，服务器才好计算
		optional uint64 orderID = 5; //订单号，新下订单不需要，如果是修改订单就需要把原订单号带上才行，因为改单的最大买卖数量会包含原订单数量。
		//为保证与下单的价格同步，也提供调整价格选项，对港、A股有意义，因为港股有价位，A股2位精度，美股可不传
		optional bool adjustPrice = 6; //是否调整价格，如果价格不合法，是否调整到合法价位，true调整，false不调整
		optional double adjustSideAndLimit = 7; //调整方向和调整幅度百分比限制，正数代表向上调整，负数代表向下调整，具体值代表调整幅度限制，如：0.015代表向上调整且幅度不超过1.5%；-0.01代表向下调整且幅度不超过1%
	}

	message S2C
	{
		required Trd_Common.TrdHeader header = 1; //交易公共参数头
		optional Trd_Common.MaxTrdQtys maxTrdQtys = 2; //最大可交易数量结构
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		//以下3个字段每条协议都有，注释说明在InitConnect.proto中
		required int32 retType = 1 [default = -400];
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}

.. note::

	* 交易公共参数头结构参考 `TrdHeader <base_define.html#trdheader>`_
	* 最大可交易数量结构参考 `MaxTrdQtys <base_define.html#MaxTrdQtys>`_
	
-------------------------------------

`Trd_GetOrderList.proto <https://github.com/FutunnOpen/py-futu-api/tree/master/futu/common/pb/Trd_GetOrderList.proto>`_ - 2201获取订单列表
-----------------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Trd_GetOrderList;

	import "Common.proto";
	import "Trd_Common.proto";

	message C2S
	{
		required Trd_Common.TrdHeader header = 1; //交易公共参数头
		optional Trd_Common.TrdFilterConditions filterConditions = 2; //过滤条件
		repeated int32 filterStatusList = 3; //需要过滤的订单状态列表
	}

	message S2C
	{
		required Trd_Common.TrdHeader header = 1; //交易公共参数头
		repeated Trd_Common.Order orderList = 2; //订单列表
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		//以下3个字段每条协议都有，注释说明在InitConnect.proto中
		required int32 retType = 1 [default = -400];
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}
	
.. note::

	* 交易公共参数头结构参考 `TrdHeader <base_define.html#trdheader>`_
	* 订单结构参考 `Order <base_define.html#order>`_
	* 过滤条件结构参考 `TrdFilterConditions <base_define.html#trdfilterconditions>`_
	
-------------------------------------

`Trd_PlaceOrder.proto <https://github.com/FutunnOpen/py-futu-api/tree/master/futu/common/pb/Trd_PlaceOrder.proto>`_ - 2202下单
-----------------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Trd_PlaceOrder;

	import "Common.proto";
	import "Trd_Common.proto";

	message C2S
	{
		required Common.PacketID packetID = 1; //交易写操作防重放攻击
		required Trd_Common.TrdHeader header = 2; //交易公共参数头
		required int32 trdSide = 3; //交易方向, 参见Trd_Common.TrdSide的枚举定义
		required int32 orderType = 4; //订单类型, 参见Trd_Common.OrderType的枚举定义
		required string code = 5; //代码，港股必须是5位数字，A股必须是6位数字，美股没限制
		required double qty = 6; //数量，2位精度，期权单位是"张"
		optional double price = 7; //价格，3位精度
		//以下为调整价格使用，对港、A股有意义，因为港股有价位，A股2位精度，美股可不传
		optional bool adjustPrice = 8; //是否调整价格，如果价格不合法，是否调整到合法价位，true调整，false不调整
		optional double adjustSideAndLimit = 9; //调整方向和调整幅度百分比限制，正数代表向上调整，负数代表向下调整，具体值代表调整幅度限制，如：0.015代表向上调整且幅度不超过1.5%；-0.01代表向下调整且幅度不超过1%
	}

	message S2C
	{
		required Trd_Common.TrdHeader header = 1; //交易公共参数头
		optional uint64 orderID = 2; //订单号
	}

	message Request
	{
		required C2S c2s = 1;
	}

	//如果下单返回的retMsg没用描述清楚错误，可再查看errCode了解详情，errCode一些取值和对应的错误描述如下:
	//2: 需要升级到保证金账户
	//3: 需要对交易期权的风险确认才能交易交易期权
	//7: 开户时选择了不希望交易衍生品
	//8: 需要对交易股权的风险确认才能交易交易股权
	//9: 需要对交易低价股的风险确认才能交易交易低价股
	//11: 需要对暗盘交易的风险确认才能进行暗盘交易
	message Response
	{
		//以下3个字段每条协议都有，注释说明在InitConnect.proto中
		required int32 retType = 1 [default = -400];
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}
	
.. note::

	* 请求包标识结构参考 `PacketID <base_define.html#packetid>`_
	* 交易公共参数头结构参考 `TrdHeader <base_define.html#trdheader>`_
	* 交易方向枚举参考 `TrdSide <base_define.html#trdside>`_
	* 订单类型枚举参考 `OrderType <base_define.html#ordertype>`_
	* 限频接口：30秒内最多30次
	
	* 如果下单返回的retMsg没用描述清楚错误，可再查看errCode了解详情，errCode一些取值和对应的错误描述如下:
	* 2: 需要升级到保证金账户
	* 3: 需要对交易期权的风险确认才能交易交易期权
	* 7: 开户时选择了不希望交易衍生品
	* 8: 需要对交易股权的风险确认才能交易交易股权
	* 9: 需要对交易低价股的风险确认才能交易交易低价股
	* 11: 需要对暗盘交易的风险确认才能进行暗盘交易
	
-------------------------------------

`Trd_ModifyOrder.proto <https://github.com/FutunnOpen/py-futu-api/tree/master/futu/common/pb/Trd_ModifyOrder.proto>`_ - 2205修改订单(改价、改量、改状态等)
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Trd_ModifyOrder;

	import "Common.proto";
	import "Trd_Common.proto";

	message C2S
	{
		required Common.PacketID packetID = 1; //交易写操作防重放攻击
		required Trd_Common.TrdHeader header = 2; //交易公共参数头
		required uint64 orderID = 3; //订单号，forAll为true时，传0
		required int32 modifyOrderOp = 4; //修改操作类型，参见Trd_Common.ModifyOrderOp的枚举定义
		optional bool forAll = 5; //是否对此业务账户的全部订单操作，true是，false否(对单个订单)，无此字段代表false，仅对单个订单
		
		//下面的字段仅在modifyOrderOp为ModifyOrderOp_Normal有效
		optional double qty = 8; //数量，2位精度，期权单位是"张"
		optional double price = 9; //价格，3位精度(A股2位)
		//以下为调整价格使用，对港、A股有意义，因为港股有价位，A股2位精度，美股可不传
		optional bool adjustPrice = 10; //是否调整价格，如果价格不合法，是否调整到合法价位，true调整，false不调整
		optional double adjustSideAndLimit = 11; //调整方向和调整幅度百分比限制，正数代表向上调整，负数代表向下调整，具体值代表调整幅度限制，如：0.015代表向上调整且幅度不超过1.5%；-0.01代表向下调整且幅度不超过1%
	}

	message S2C
	{
		required Trd_Common.TrdHeader header = 1; //交易公共参数头
		required uint64 orderID = 2; //订单号
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		//以下3个字段每条协议都有，注释说明在InitConnect.proto中
		required int32 retType = 1 [default = -400];
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}

.. note::

	* 请求包标识结构参考 `PacketID <base_define.html#packetid>`_
	* 交易公共参数头结构参考 `TrdHeader <base_define.html#trdheader>`_
	* 修改操作枚举参考 `ModifyOrderOp <base_define.html#modifyorderop>`_
	* 限频接口：30秒内最多30次
	
-------------------------------------

`Trd_UpdateOrder.proto <https://github.com/FutunnOpen/py-futu-api/tree/master/futu/common/pb/Trd_UpdateOrder.proto>`_ - 2208推送订单更新
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Trd_UpdateOrder;

	import "Common.proto";
	import "Trd_Common.proto";

	//推送协议，无C2S和Request结构，retType始终是RetType_Succeed

	message S2C
	{
		required Trd_Common.TrdHeader header = 1; //交易公共参数头
		required Trd_Common.Order order = 2; //订单结构
	}

	message Response
	{
		//以下3个字段每条协议都有，注释说明在InitConnect.proto中
		required int32 retType = 1 [default = -400];
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}

.. note::

	* 交易公共参数头结构参考 `TrdHeader <base_define.html#trdheader>`_
	* 订单结构参考 `Order <base_define.html#order>`_
	
-------------------------------------

`Trd_GetOrderFillList.proto <https://github.com/FutunnOpen/py-futu-api/tree/master/futu/common/pb/Trd_GetOrderFillList.proto>`_ - 2211获取成交列表
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Trd_GetOrderFillList;

	import "Common.proto";
	import "Trd_Common.proto";

	message C2S
	{
		required Trd_Common.TrdHeader header = 1; //交易公共参数头
		optional Trd_Common.TrdFilterConditions filterConditions = 2; //过滤条件
	}

	message S2C
	{
		required Trd_Common.TrdHeader header = 1; //交易公共参数头
		repeated Trd_Common.OrderFill orderFillList = 2; //成交列表
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		//以下3个字段每条协议都有，注释说明在InitConnect.proto中
		required int32 retType = 1 [default = -400];
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}

.. note::

	* 交易公共参数头结构参考 `TrdHeader <base_define.html#trdheader>`_
	* 订单结构参考 `OrderFill <base_define.html#orderfill>`_
	* 过滤条件结构参考 `TrdFilterConditions <base_define.html#trdfilterconditions>`_
	
-------------------------------------

`Trd_UpdateOrderFill.proto <https://github.com/FutunnOpen/py-futu-api/tree/master/futu/common/pb/Trd_UpdateOrderFill.proto>`_ - 2218推送新成交
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Trd_UpdateOrderFill;

	import "Common.proto";
	import "Trd_Common.proto";

	//推送协议，无C2S和Request结构，retType始终是RetType_Succeed

	message S2C
	{
		required Trd_Common.TrdHeader header = 1; //交易公共参数头
		required Trd_Common.OrderFill orderFill = 2; //成交结构
	}

	message Response
	{
		//以下3个字段每条协议都有，注释说明在InitConnect.proto中
		required int32 retType = 1 [default = -400];
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}

.. note::

	* 交易公共参数头结构参考 `TrdHeader <base_define.html#trdheader>`_
	* 订单结构参考 `OrderFill <base_define.html#orderfill>`_
	
-------------------------------------

`Trd_GetHistoryOrderList.proto <https://github.com/FutunnOpen/py-futu-api/tree/master/futu/common/pb/Trd_GetHistoryOrderList.proto>`_ - 2221获取历史订单列表
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Trd_GetHistoryOrderList;

	import "Common.proto";
	import "Trd_Common.proto";

	message C2S
	{
		required Trd_Common.TrdHeader header = 1; //交易公共参数头
		required Trd_Common.TrdFilterConditions filterConditions = 2; //过滤条件
		repeated int32 filterStatusList = 3; //需要过滤的订单状态列表
	}

	message S2C
	{
		required Trd_Common.TrdHeader header = 1; //交易公共参数头
		repeated Trd_Common.Order orderList = 2; //历史订单列表
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		//以下3个字段每条协议都有，注释说明在InitConnect.proto中
		required int32 retType = 1 [default = -400];
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}

.. note::

	* 交易公共参数头结构参考 `TrdHeader <base_define.html#trdheader>`_
	* 订单结构参考 `Order <base_define.html#order>`_
	* 过滤条件结构参考 `TrdFilterConditions <base_define.html#trdfilterconditions>`_
	* 订单状态枚举参考 `OrderStatus <base_define.html#orderstatus>`_
	* 限频接口：30秒内最多10次
	
-------------------------------------

`Trd_GetHistoryOrderFillList.proto <https://github.com/FutunnOpen/py-futu-api/tree/master/futu/common/pb/Trd_GetHistoryOrderFillList.proto>`_ - 2222获取历史成交列表
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: protobuf

	syntax = "proto2";
	package Trd_GetHistoryOrderFillList;

	import "Common.proto";
	import "Trd_Common.proto";

	message C2S
	{
		required Trd_Common.TrdHeader header = 1; //交易公共参数头
		required Trd_Common.TrdFilterConditions filterConditions = 2; //过滤条件
	}

	message S2C
	{
		required Trd_Common.TrdHeader header = 1; //交易公共参数头
		repeated Trd_Common.OrderFill orderFillList = 2; //历史成交列表
	}

	message Request
	{
		required C2S c2s = 1;
	}

	message Response
	{
		//以下3个字段每条协议都有，注释说明在InitConnect.proto中
		required int32 retType = 1 [default = -400];
		optional string retMsg = 2;
		optional int32 errCode = 3;
		
		optional S2C s2c = 4;
	}

.. note::

	* 交易公共参数头结构参考 `TrdHeader <base_define.html#trdheader>`_
	* 成交结构参考 `OrderFill <base_define.html#orderfill>`_
	* 过滤条件结构参考 `TrdFilterConditions <base_define.html#trdfilterconditions>`_
	* 限频接口：30秒内最多10次
	
-------------------------------------
