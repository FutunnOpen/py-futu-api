# -*- coding: utf-8 -*-

import json
import os
from abc import abstractmethod
from bidict import bidict

__JsonFileName__ = "Qot_Common.proto.json"
__PBPrefixName__ = "Qot_Common_pb2."
__TemplateCodeFileName__ = "template_code.txt"
__TemplateFileHeadName__ = "template_head.txt"
__TemplateRstName__ = "rst_template.txt"

class EnumsItemStruct(object):

    def __init__(self, class_name):
        self.class_name = class_name  # 所属的类名
        self.full_name = ""  # 原始变量名
        self.trim_name = ""  # 整理后的变量名，主要是去掉前面的类名头
        self.underscore_name = ""  # 整理后的变量名，把骆驼命名改成大小写命名
        self.str = ""  # 整理后的变量值，做一些约定修整
        self.number = 0
        self.pb_value = ""  # 对应的pb里面的变量名
        self.description = ""

    @classmethod
    def change_variable_name(cls, listx):
        listy = listx[0]
        for i in range(1, len(listx) - 1):

            if listx[i] == '_' or listx[i - 1] == '_' or listx[i + 1] == '_':
                listy += listx[i]

            elif listx[i].isupper() and not listx[i - 1].isupper():  # 加'_',当前为大写，前一个字母为小写
                listy += '_'
                listy += listx[i]

            elif listx[i].isupper() and listx[i - 1].isupper() and listx[i + 1].islower():
                # 加'_',当前为大写，前一个字母为小写
                listy += '_'
                listy += listx[i]
            else:
                listy += listx[i]
        if len(listx) > 1:
            listy += listx[-1]
        return listy.upper()

    def trim(self):
        self.trim_name = self.full_name
        self.pb_value = __PBPrefixName__ + self.full_name

        if len(self.class_name) > 0 and len(self.trim_name) > 0:
            self.trim_name = self.trim_name.replace(self.class_name + "_", "")

        if self.trim_name[0] in list(map(lambda x: str(x), list(range(10)))):
            self.trim_name = self.class_name[:2] + "_" + self.trim_name


        if len(self.description) == 0 and self.number == 0:
            self.description = "未知"

        self.underscore_name = self.change_variable_name(self.trim_name)
        if self.underscore_name in ["UNKNOW", "UNKONW", "UNKNOWN"]:
            self.underscore_name = "NONE"

        self.str = self.underscore_name
        if self.number == 0 and self.underscore_name == "NONE":
            self.str = "N/A"





class ClassStruct(object):

    def __init__(self):
        self.name = ""
        self.description = ""
        self.values = list()




class GenerateCode(object):

    def __init__(self):
        self.local_path = os.path.dirname(os.path.realpath(__file__))
        self.enums = list()

    def load(self):
        with open(os.path.join(self.local_path, __JsonFileName__), 'r', encoding='UTF-8') as load_f:
            self.enums.clear()
            json_to_python = json.load(load_f)
            files_json = json_to_python["files"]
            enums_json = files_json[0]["enums"]
            for item in enums_json:
                c = ClassStruct()
                c.name = item["longName"]
                c.description = item["description"]
                for v in item["values"]:
                    s = EnumsItemStruct(c.name)
                    s.full_name = v["name"]
                    s.number = int(v["number"])
                    s.description = v["description"]
                    s.trim()
                    c.values.append(s)
                self.enums.append(c)

    def py(self, export_file):
        if len(self.enums) == 0:
            return

        template_code = ""
        with open(os.path.join(self.local_path, __TemplateCodeFileName__), 'r', encoding='UTF-8') as load_f:
            template_code = load_f.read()

        code_file = open(export_file, 'w', encoding='utf-8')
        """写入文件头"""
        with open(os.path.join(self.local_path, __TemplateFileHeadName__), 'r', encoding='UTF-8') as f:
            code_file.write(f.read())

        for class_item in self.enums:
            classdescription = class_item.description.replace("\n", "，")
            classname = class_item.name
            variablecode = ""
            diccode = ""
            code_file.write("\n\n\n'''-------------------------{}----------------------------'''\n\n\n".format(classname))

            for item in class_item.values:
                variablename = item.underscore_name
                strvalue = item.str
                description = item.description
                pbvalue = item.pb_value
                kvcode = "{variablename} = \"{strvalue}\"".format(variablename=variablename, strvalue=strvalue)
                code = "    {kvcode: <50} # {description}\n".format(kvcode=kvcode, description=description)
                variablecode += code
                code = "            self.{variablename}: {pbvalue},\n".format(
                    variablename=variablename, pbvalue=pbvalue)
                diccode += code

            c = template_code.format(classdescription=classdescription,
                                 classname=classname,
                                 variablecode=variablecode.rstrip("\n,"),
                                 diccode=diccode.rstrip("\n,"))
            code_file.write(c)
        code_file.close()

    def rst(self, export_file):
        if len(self.enums) == 0:
            return
        rst_template= ""
        with open(os.path.join(self.local_path, __TemplateRstName__), 'r', encoding='UTF-8') as load_f:
            rst_template = load_f.read()
        code_file = open(export_file, 'w', encoding='utf-8')
        for class_item in self.enums:
            classdescription = class_item.description.replace("\n", "，")
            classname = class_item.name
            dicinfo = ""
            for item in class_item.values:
                name = item.underscore_name
                description = item.description
                kvcode = " ..  py:attribute:: {name}\n\n  {description}\n\n".format(name=name, description=description)
                dicinfo += kvcode

            c = rst_template.format(classname=classname,
                                    classdescription=classdescription,
                                    dicinfo=dicinfo)
            code_file.write(c)
        code_file.close()



if __name__ =="__main__":
    c = GenerateCode()
    c.load()
    path = os.path.dirname(os.path.realpath(__file__))
    c.py(os.path.join(path, "Qot_Common.py"))
    c.rst(os.path.join(path, "Qot_Common.rst"))

# if __name__ =="__main__":
#     print(SortField.to_string("hhh"))
#     print(SortField.to_string(1))
#     print(SortField.to_number("CODE"))
#     print(SortField.to_number(SortField.CODE))
#     print(SortField.to_number(list()))
#     print("-------------------------------------------------------------------")






