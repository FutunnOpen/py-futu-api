# futu-api - 富途量化投资平台 (Futu Quant Trading API)

### 简介

[​**futu-api**](https://futunnopen.github.io/futuquant/intro/intro.html)开源项目可以满足使用[**富途Open API**](https://www.futunn.com/)软件进行量化投资的需求, 提供包括Python接口、Json和Protobuf接口的行情及交易的API。

- [官方在线文档](https://futunnopen.github.io/futuquant/intro/intro.html)

-------------------

### 安装
```
pip install futu-api
```

###### 注: 本API当前仅支持Python3, 推荐安装anaconda3环境，方便快捷。

---

### 快速上手
```

# 导入futu-api
import futu as ft

# 实例化行情上下文对象
quote_ctx = ft.OpenQuoteContext(host="127.0.0.1", port=11111)

# 上下文控制
quote_ctx.start()              # 开启异步数据接收
quote_ctx.set_handler(ft.TickerHandlerBase())  # 设置用于异步处理数据的回调对象(可派生支持自定义)

# 低频数据接口
market = ft.Market.HK
code = 'HK.00123'
code_list = [code]
plate = 'HK.BK1107'
print(quote_ctx.get_trading_days(market, start_date=None, end_date=None))   # 获取交易日
print(quote_ctx.get_stock_basicinfo(market, stock_type=ft.SecurityType.STOCK))   # 获取股票信息
print(quote_ctx.get_history_kline(code, start=None, end=None, ktype=ft.KLType.K_DAY, autype=ft.AuType.QFQ))  # 获取历史K线
print(quote_ctx.get_autype_list(code_list))                                  # 获取复权因子
print(quote_ctx.get_market_snapshot(code_list))                              # 获取市场快照
print(quote_ctx.get_plate_list(market, ft.Plate.ALL))                         # 获取板块集合下的子板块列表
print(quote_ctx.get_plate_stock(plate))                         # 获取板块下的股票列表

# 高频数据接口
quote_ctx.subscribe(code, [ft.SubType.QUOTE, ft.SubType.TICKER, ft.SubType.K_DAY, ft.SubType.ORDER_BOOK, ft.SubType.RT_DATA, ft.SubType.BROKER])
print(quote_ctx.get_stock_quote(code))  # 获取报价
print(quote_ctx.get_rt_ticker(code))   # 获取逐笔
print(quote_ctx.get_cur_kline(code, num=100, ktype=ft.KLType.K_DAY))   #获取当前K线
print(quote_ctx.get_order_book(code))       # 获取摆盘
print(quote_ctx.get_rt_data(code))          # 获取分时数据
print(quote_ctx.get_broker_queue(code))     # 获取经纪队列

# 停止异步数据接收
quote_ctx.stop()

# 关闭对象
quote_ctx.close()

# 实例化港股交易上下文对象
trade_hk_ctx = ft.OpenHKTradeContext(host="127.0.0.1", port=11111)

# 交易接口列表
print(trade_hk_ctx.unlock_trade(password='123456'))                # 解锁接口
print(trade_hk_ctx.accinfo_query(trd_env=ft.TrdEnv.SIMULATE))      # 查询账户信息
print(trade_hk_ctx.place_order(price=1.1, qty=2000, code=code, trd_side=ft.TrdSide.BUY, order_type=ft.OrderType.NORMAL, trd_env=ft.TrdEnv.SIMULATE))  # 下单接口
print(trade_hk_ctx.order_list_query(trd_env=ft.TrdEnv.SIMULATE))      # 查询订单列表
print(trade_hk_ctx.position_list_query(trd_env=ft.TrdEnv.SIMULATE))    # 查询持仓列表

trade_hk_ctx.close()

```

---

### 示例策略

- 示例策略文件位于目录: (futu-api包安装目录)/py-futu-api/examples 下，用户可参考实例策略来学习API的使用。

---

### 组织结构

![image](https://github.com/FutunnOpen/futuquant/blob/master/docs/source/_static/Structure.png)

​	最新版本在master分支。之前各版本在其他分支上。

---

### 使用须知

- python脚本运行前，需先启动[FutuOpenD](https://www.futunn.com/download/openAPI)网关客户端
- 详情查看[安装指南](https://futunnopen.github.io/futuquant/setup/setup.html)

### API与FutuOpenD网关客户端的架构

![image](https://futunnopen.github.io/futuquant/_images/API.png)

***


### API及FutuOpenD客户端交流方式

* 富途开放API群(229850364, 108534288) 
* 团队或公司客户请在入群后联系群主

***

### 使用说明

* 有任何问题可以到 issues  处提出，我们会及时进行解答。
* 使用新版本时请先仔细阅读接口文档，大部分问题都可以在接口文档中找到你想要的答案。
* 欢迎大家提出建议、也可以提出各种需求，我们一定会尽量满足大家的需求。

---
