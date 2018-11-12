

from futuquant import *
import pandas as pd
import numpy as np
import os
import time
from time import sleep


def test_tick(code_list, ip, host):

    quote_context = OpenQuoteContext(host=ip, port=host)
    quote_context.start()

    while True:
        ret, data = quote_context.subscribe(code_list, SubType.TICKER)
        if ret != RET_OK:
            print(data)
            break
        count = 0
        for x in code_list:
            print(quote_context.get_rt_ticker(x))
            count = count + 1
            if count >= 10:
                break
        sleep(2)
        quote_context.unsubscribe(code_list, SubType.TICKER)
        print("loop sub")
        sleep(2)
    quote_context.close()


def test_kline(code_list, ip, host):

    quote_context = OpenQuoteContext(host=ip, port=host)
    quote_context.start()

    while True:
        ret, data = quote_context.subscribe(code_list, SubType.K_DAY)
        if ret != RET_OK:
            print(data)
            break
        for x in code_list:
            print(quote_context.get_cur_kline(x, 1000))
        sleep(10)
        quote_context.unsubscribe(code_list, SubType.TICKER)
        break

    quote_context.close()


def test1():

    """
    for x in range(10):
        codes = code_list[int(x * sub_cout/10): int((x+1) * sub_cout/10)]

        ret, data = quote_context.subscribe(codes, SubType.K_DAY)
        if ret != RET_OK:
            print(data)
            sleep(3)

        print("loop: {}".format(x))
        sleep(3)
        for x in codes:
            print(quote_context.get_cur_kline(x, 1000))

    print(codes_error)
    """

def main():

    filename = time.strftime("%Y-%m-%d", time.localtime()) + '.csv'

    if os.path.exists(filename):
        symbols = pd.read_csv(filename, usecols=['code', 'name'])
        symbol_code = symbols['code'].values.tolist()
        symbol_name = symbols['name'].values.tolist()
    else:
        print("Please run stock select script first !!! >>> guolin_Futu.py")
        exit(0)

    sub_cout = 100
    code_list = symbol_code[0:sub_cout]

    # ip = "193.112.189.131"
    ip = "172.18.10.58"
    host = 11112

    # test_kline(code_list, ip , host)

    #################################################################
    quote_context = OpenQuoteContext(host=ip, port=host)

    codes_error = []
    for code in code_list:
        ret, data = quote_context.subscribe(code, SubType.K_DAY)
        print("loop: {}".format(code))
        if ret != RET_OK:
            print("code={} erro:{}".format(code, data))
            codes_error.append(code)
            quote_context.close()
            break
        print("code= {} sub ret={} data={}".format(code, ret, data))
        ret, data = quote_context.get_cur_kline(code, 1000)
        print("code= {} get ret={} data={}".format(code, ret, data))


if __name__ == "__main__":
    main()
