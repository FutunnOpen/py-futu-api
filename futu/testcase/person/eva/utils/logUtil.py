#-*-coding:utf-8-*-

import logging
import os
import sys
import time

class Logs(object):
    '''记录日志'''

    def getNewLogger(self,name,dir= None):
        '''

        :param name: 日志实例名
        :param dir: 日志所在文件夹名
        :return:
        '''
        logger = logging.getLogger(name)
        dir_path = os.path.dirname(os.path.dirname(os.getcwd())) + os.path.sep + 'log'
        if dir is None:
            dir = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        dir_path = dir_path+os.path.sep+dir
        if os.path.exists(dir_path) is False:
            os.makedirs(dir_path)
        log_abs_name = dir_path + os.path.sep + name + '.txt'
        print(log_abs_name+'\n')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler = logging.FileHandler(log_abs_name)
        handler.setFormatter(formatter)
        console = logging.StreamHandler(stream=sys.stdout)

        logger.addHandler(handler)  # 设置日志输出到文件
        logger.addHandler(console)  # 设置日志输出到屏幕控制台
        logger.setLevel(logging.DEBUG)  # 设置打印的日志等级

        return logger