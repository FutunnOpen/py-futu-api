# encoding: UTF-8

'''
    策略运行脚本
'''
from futu.examples.tiny_quant.tiny_quant_frame.TinyQuantFrame import *
from futu.examples.tiny_quant.demo.tq_sample.TinyStrateSample import *


if __name__ == '__main__':
    my_strate = TinyStrateSample()
    frame = TinyQuantFrame(my_strate)
    frame.run()

