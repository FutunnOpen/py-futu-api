from futuquant.examples.app.stock_alarm.data_acquisition import quote_test
from futuquant.examples.app.stock_alarm.config import *

stock_list = ['HK.02318', 'HK.02828','US.AAPL','US.GOOG']  # 监控的股票列表
quote_test(stock_list, config.host, config.port)  # 开始监控