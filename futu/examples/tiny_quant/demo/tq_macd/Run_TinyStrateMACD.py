# encoding: UTF-8

'''
    策略运行脚本
'''
from TinyStrateMACD import *
import logging
import futu
import time
from futu.examples.tiny_quant.tiny_quant_frame.TinyQuantFrame import *


if __name__ == '__main__':
    futu.logger.console_level = logging.INFO
    my_strate = TinyStrateMACD()
    frame = TinyQuantFrame(my_strate)
    while True:
        frame.run()
        time.sleep(10000)
        frame.stop()





