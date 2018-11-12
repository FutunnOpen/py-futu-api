#-*-coding:utf-8-*-
import pandas

from futuquant.testcase.person.eva.trade.Handler import *
from futuquant.trade.open_trade_context import *
from futuquant import *
import datetime
import logging

if __name__ == '__main__':
    quote_ctx = OpenQuoteContext('127.0.0.1',11111)
    print(quote_ctx.get_plate_list(Market.US, Plate.CONCEPT))