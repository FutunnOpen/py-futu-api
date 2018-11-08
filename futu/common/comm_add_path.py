# -*- coding: utf-8 -*-
"""
这个文件主要在开发futu-api库的时候用得上，如果你只是使用futu-api库，可以不用引入这个文件
"""
import os
import sys


def get_package_path(name):
    temp_path = os.getcwd()
    for i in range(0, 3):  # 最多查找3级
        temp_path = os.path.abspath(os.path.dirname(temp_path))
        filename = os.path.basename(temp_path)
        if filename == name:
            break
    return temp_path


#我們不再提供回测框架，这里的回测mini库仅用于demo演示
def add_tiny_quant_frame():
    temp_path = get_package_path("tiny_quant")
    os.path.join(temp_path, "tiny_quant_frame")
    if (temp_path.strip() != '') and (temp_path not in sys.path):
        print(temp_path)
        sys.path.append(temp_path)


#这一段代码是为了开发库的过程中，优先匹配当前工作路径的futu-api库
def add_futu_package_path():
    temp_path = os.path.abspath(os.path.dirname(get_package_path("futu")))
    if (temp_path.strip() != '') and (temp_path not in sys.path):
        sys.path.insert(0, temp_path)
        print(temp_path)

