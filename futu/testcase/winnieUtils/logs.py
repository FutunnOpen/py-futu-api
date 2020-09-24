# -*- coding:utf-8 -*-
import os
import logging
import sys

class MyLogger():
    log_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))),"logs")
    def geLogger(self,name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        formater = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        log_path = os.path.join(MyLogger.log_path, name)
        fh_handler = logging.FileHandler(log_path, 'w')
        fh_handler.setFormatter(formater)

        con_handler = logging.StreamHandler(sys.stdout)
        con_handler.setFormatter(formater)

        logger.addHandler(fh_handler)
        logger.addHandler(con_handler)
        return logger


if __name__ == '__main__':
    print(MyLogger.log_path)