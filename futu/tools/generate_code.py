# -*- coding: utf-8 -*-

import json
import os
import load_template
from abc import abstractmethod
from bidict import bidict


#__PBPrefixName__ = "GetGlobalState_pb2."

__TemplateCodeFileName__ = "template_code.txt"
__TemplateFileHeadName__ = "template_head.txt"
__TemplateRstName__ = "rst_template.txt"
__TemplateFileFunctionName__ = "template_function.txt"


template = load_template.FutuTemplate()


def change_variable_name(listx):  # 修改变量名
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


def code_add_space(code, space_count=1, space_str="	"):  # 逐行加空格
    ls = code.split('\n')
    ret_code = space_line = ""
    for i in range(space_count):
        space_line += space_str

    for s in ls:
        if len(s) > 0:
            ret_code += (space_line + s + "\n")
        else:
            ret_code += "\n"

    return ret_code[:-1]


class EnumsItemStruct(object):

    def __init__(self, obj, class_name, pb_prefix_name):
        self.obj = obj
        self.class_name = class_name  # 所属的类名
        self.pb_prefix_name = pb_prefix_name
        self.full_name = obj["name"] # 原始变量名
        self.number = int(obj["number"])
        self.description = obj["description"]

        self.trim_name = self.full_name  # 整理后的变量名，主要是去掉前面的类名头
        self.pb_value = self.pb_prefix_name + self.full_name # 对应的pb里面的变量名

        if len(self.class_name) > 0 and len(self.trim_name) > 0:
            self.trim_name = self.trim_name.replace(self.class_name + "_", "")

        if self.trim_name[0] in list(map(lambda x: str(x), list(range(10)))):
            self.trim_name = self.class_name[:2] + "_" + self.trim_name

        if not isinstance(self.description, str):
            self.description = ""
        if len(self.description) == 0 and self.number == 0:
            self.description = "未知"

        self.underscore_name = change_variable_name(self.trim_name) # 整理后的变量名，把骆驼命名改成大小写命名
        if self.underscore_name in ["UNKNOW", "UNKONW", "UNKNOWN"]:
            self.underscore_name = "NONE"

        self.str = self.underscore_name # 整理后的变量值，做一些约定修整
        if self.number == 0 and self.underscore_name == "NONE":
            self.str = "N/A"


class ParameterItem(object):
    def __init__(self, obj, class_owner):
        self.obj = obj
        self.class_owner = class_owner
        self.class_name = class_owner.name  # 所属的类名
        self.pb_prefix_name = class_owner.pb_prefix_name
        self.name = obj["name"] # 原始变量名
        self.full_type = obj["fullType"] # 原始变量名
        self.long_type = obj["longType"]  # 原始变量名
        self.trim_name = change_variable_name(self.name).lower() # 整理后的名字
        self.trim_type = self.long_type
        self.description = obj["description"]
        self.label = obj["label"]
        self.warning_filter = ""
        self.repeated_class = None
        self.trim()

    def trim(self):
        if self.obj is None:
            return
        # 股票名特殊处理
        if self.full_type == "Qot_Common.Security":
            if self.label == "repeated":  # 股票列表
                self.trim_type = "list"
                self.trim_name = "code_list"

            else:  # 单个股票
                self.trim_name = "code"
                self.trim_type = "string"

        # 嵌套了复杂类型list
        elif self.label == "repeated":
            self.trim_type = "list"

        elif self.name == "time":
            self.trim_name = "{}_time".format(change_variable_name(self.class_name).lower())
            if len(self.class_owner.description) > 0:
                self.description = self.class_owner.description + "  " + self.description

    def is_timestamp(self):
        """有两种数据类型时，timestamp需要过滤掉"""
        if self.long_type == "double" and self.name.lower().find("timestamp") != -1:
            return True
        return False

    def get_args(self):
        return "            \"{}\": {},".format(self.trim_name, self.trim_name)

    def get_warning_filter(self):
        if self.trim_name == "code_list":
            self.warning_filter = "        if is_str(code_list):\n" \
                                  "            code_list = code_list.split(',')\n" \
                                  "        elif isinstance(code_list, list):\n" \
                                  "            pass\n" \
                                  "        else:\n" \
                                  "            return RET_ERROR, " \
                                  "\"code list must be like ['HK.00001', 'HK.00700'] or 'HK.00001,HK.00700'\"\n" \
                                  "        code_list = unique_and_normalize_list(code_list)\n" \
                                  "        for code in code_list:\n" \
                                  "            if code is None or is_str(code) is False:\n" \
                                  "                error_str = ERROR_STR_PREFIX + " \
                                  "\"the type of param in code_list is wrong\"\n" \
                                  "                return RET_ERROR, error_str\n"
        elif self.trim_name == "code":
            self.warning_filter = "        if code is None or is_str(code) is False:\n" \
                                  "            error_str = ERROR_STR_PREFIX + 'the type of code param is wrong'\n" \
                                  "            return RET_ERROR, error_str\n"
        return self.warning_filter

    def get_pack_req_filter(self):
        if self.trim_name == "code_list":
            return "        stock_tuple_list = []\n" \
                   "        failure_tuple_list = []\n" \
                   "        for stock_str in code_list:\n" \
                   "            ret_code, content = split_stock_str(stock_str)\n" \
                   "            if ret_code != RET_OK:\n" \
                   "                error_str = content\n" \
                   "                failure_tuple_list.append((ret_code, error_str))\n" \
                   "                continue\n" \
                   "            market_code, stock_code = content\n" \
                   "            stock_tuple_list.append((market_code, stock_code))\n" \
                   "        if len(failure_tuple_list) > 0:\n" \
                   "            error_str = '\\n'.join([x[1] for x in failure_tuple_list])\n" \
                   "            return RET_ERROR, error_str, None\n"

        elif self.trim_name == "code":
            return "        ret, content = split_stock_str(code)\n" \
                   "        if ret == RET_ERROR:\n" \
                   "            error_str = content\n" \
                   "            return RET_ERROR, error_str, None\n" \
                   "        market_code, stock_code = content\n"

    def get_pack_req_add(self):
        if self.trim_name == "code_list":
            return "        for market_code, stock_code in stock_tuple_list:\n" \
                   "            stock_inst = req.c2s.{}.add()\n" \
                   "            stock_inst.market = market_code\n" \
                   "            stock_inst.code = stock_code\n".format(self.name)
        elif self.trim_name == "code":
            return "        req.c2s.{0}.market = market_code\n" \
                   "        req.c2s.{0}.code = stock_code".format(self.name)
        else:
            return "        req.c2s.{0} = {1}\n".format(self.name, self.trim_name)

    def set_repeated(self, class_obj):
        if self.repeated_class is None and self.full_type == class_obj.full_name:
            self.repeated_class = class_obj

    def get_unpack_var(self):
        if self.is_timestamp():
            return ""
        else:
            if self.full_type == "Qot_Common.Security":
                s_code = template["class_unpack_code"].format(name=self.name)
            else:
                s_code = "#  {description} type={long_type}\n" \
                         "{trim_name}=rsp_pb.s2c.{name}\n".\
                    format(description=self.description,
                           long_type=self.long_type,
                           trim_name=self.trim_name,
                           name=self.name)
            return code_add_space(s_code, 2)

    def get_unpack_list_add(self, ret_list_name):
        """用于列表遍历"""
        name_list = list()
        if self.trim_type == "list" and self.repeated_class is not None:
            str_code = ""
            for item in self.repeated_class.values:
                if item.is_timestamp():
                    continue
                str_code += "#  {description} type={long_type}\n" \
                            "data[\"{trim_name}\"]=item.{name}\n". \
                    format(description=item.description,
                           long_type=item.long_type,
                           trim_name=item.trim_name,
                           name=item.name)
                name_list.append(item.trim_name)

            if len(str_code) > 0:
                head_code = "for item in {trim_name}:\n" \
                    "	data = dict()\n" \
                    "	{list_name}.append(data)\n".\
                    format(trim_name=self.trim_name, list_name=ret_list_name)
                return code_add_space(head_code, 2) + code_add_space(str_code, 3), name_list

        return "", name_list

    def get_unpack_add(self, ret_list_name):
        if self.is_timestamp() or self.trim_type == "list":
            return ""
        else:
            if self.full_type == "Qot_Common.Security":
                name = "stock_code"
            else:
                name = self.name
            s_code = "#  {description} type={long_type}\n" \
                     "data[\"{trim_name}\"]={name}\n".\
                format(description=self.description,
                       long_type=self.long_type,
                       trim_name=self.trim_name,
                       name=name)
            return code_add_space(s_code, 3)

    def get_unpack_dict_code(self, ret_name):
        if self.is_timestamp():
            return ""
        else:
            if self.full_type == "Qot_Common.Security":
                s_code = "#  {description} type={long_type}\n" \
                         "{ret_name}[\"stock_code\"]= merge_qot_mkt_stock_str({trim_name}.market, {trim_name}.code)\n". \
                    format(description=self.description,
                           long_type=self.long_type,
                           trim_name=self.trim_name,
                           ret_name=ret_name)
            else:
                s_code = "#  {description} type={long_type}\n" \
                         "{ret_name}[\"{trim_name}\"]=rsp_pb.s2c.{name}\n".\
                    format(description=self.description,
                           long_type=self.long_type,
                           trim_name=self.trim_name,
                           name=self.name,
                           ret_name=ret_name)
            return code_add_space(s_code, 2)


class ClassItemStruct(object):

    def __init__(self, json_obj, class_type, pb_prefix_name):
        self.name = json_obj["longName"]
        self.full_name = json_obj["fullName"]
        self.description = json_obj["description"]
        self.json_obj = json_obj
        self.pb_prefix_name = pb_prefix_name
        self.class_type = class_type
        self.has_repeated = False
        self.repeated_count = 0
        self.repeated_var_list = list()
        self.vars_dict = dict()

        if class_type == "enums":
            self.values = list()
            for v in json_obj["values"]:
                s = EnumsItemStruct(v, self.name, self.pb_prefix_name)
                self.values.append(s)

        if class_type == "class":
            self.values = list()
            for v in json_obj["fields"]:
                s = ParameterItem(v, self)
                if s.label == "repeated":
                    self.has_repeated = True
                    self.repeated_count += 1
                self.values.append(s)

    def is_repeated_type(self, full_name):
        for item in self.values:
            if item.full_type == full_name:
                return True
        return False

    def set_repeated(self, class_obj):
        for item in self.values:
            if item.full_type == class_obj.full_name:
                item.set_repeated(class_obj)

    def get_function_return(self):
        """函数返回，主要是组成pd和解析"""
        if self.repeated_count == 1:
            list_name = "ret_list"
            ls = self.vars_dict[list_name]
            if isinstance(ls, list):
                str_code = '\'' + '\',\n\''.join(ls) + '\''
            return template["list_return"].format(var_name=code_add_space(str_code, 4))
        elif self.repeated_count == 0:
            ls = self.vars_dict["ret"]
            if isinstance(ls, list):
                str_code = '\'' + '\',\n\''.join(ls) + '\''
            return template["dict_return"].format(var_name=code_add_space(str_code, 4))

    def get_unpack_code(self):
        self.repeated_var_list.clear()
        self.vars_dict.clear()

        if self.repeated_count == 1:
            """如果有多个重复数据（列表项），这种方式就不适合了"""
            unpack_var = unpack_add = ""
            list_name = "ret_list"
            self.vars_dict[list_name] = list()
            for item in self.values:
                unpack_var += item.get_unpack_var()
            """开始遍历赋值,先枚举列表内的数据"""
            for item in self.values:
                if item.label == "repeated":
                    code, names = item.get_unpack_list_add(list_name)
                    if code is not None:
                        unpack_add += code
                    self.vars_dict[list_name].extend(names)
                    break
            for item in self.values:
                if item.label != "repeated":
                    code = item.get_unpack_add(list_name)
                    if len(code) > 0:
                        unpack_add += code
                        self.vars_dict[list_name].append(item.trim_name)

            return template["class_unpack_list_add"].format(unpack_var=unpack_var.rstrip('\n'),
                                                            unpack_add=unpack_add.rstrip('\n'),
                                                            list_name=list_name)
        elif self.repeated_count == 0:
            unpack_code = ""
            self.vars_dict["ret"] = list()
            """开始遍历赋值"""
            for item in self.values:
                unpack_code += item.get_unpack_dict_code("ret")
                self.vars_dict["ret"].append(item.trim_name)
            return template["class_unpack_var_add"].format(unpack_code=unpack_code.rstrip('\n'))

        elif self.repeated_count > 1:
            """如果有多个重复数据（列表项），可以用元组返回"""
            unpack_var = unpack_add = ""
            self.repeated_var_list.clear()
            for item in self.values:
                unpack_var += item.get_unpack_var()

            """开始遍历列表"""
            for item in self.values:
                if item.label == "repeated":
                    list_name = item.trim_name
                    self.repeated_var_list.append(list_name)
                    s_code = item.get_unpack_list_add(list_name)
                    for v in self.values:
                        if v.trim_name not in self.repeated_var_list and v.label != "repeated":
                            s_code += v.get_unpack_add(list_name)

                    s_code += "\n"
                    unpack_add += s_code

            return unpack_var + unpack_add

    def get_unpack_return(self):
        if self.repeated_count == 1:
            return "return RET_OK, \"\", ret_list"
        elif self.repeated_count == 0:
            return "return RET_OK, \"\", ret"
        elif self.repeated_count > 1:
            return "return RET_OK, \"\", ({})".format(','.join(self.repeated_var_list))


class GenerateCode(object):

    def __init__(self, class_name, prefix=""):
        self.local_path = os.path.dirname(os.path.realpath(__file__))
        self.enums = list()
        self.class_name = class_name
        self.prefix = prefix
        if prefix != "":
            self.json_filename = "{}_{}.proto.json".format(prefix, class_name)
        else:
            self.json_filename = "{}.proto.json".format(class_name)
        self.pb_prefix_name = "{}_pb2.".format(class_name)
        self.obj = None
        self.c2s = self.s2c = None

    def load(self):
        self.obj = None
        with open(os.path.join(self.local_path, self.json_filename), 'r', encoding='UTF-8') as load_f:
            self.obj = json.load(load_f)
            self.load_enums()
            self.load_parameter()
            self.load_repeated_parameter(self.obj)  # 嵌套重复元素
        with open(os.path.join(self.local_path, "Qot_Common.proto.json"), 'r', encoding='UTF-8') as load_f:
            self.load_repeated_parameter(json.load(load_f))

    def load_enums(self):
        self.enums.clear()
        if self.obj is not None:
            files_json = self.obj["files"]
            enums_json = files_json[0]["enums"]
            for item in enums_json:
                c = ClassItemStruct(item, "enums", self.pb_prefix_name)
                self.enums.append(c)

    def load_parameter(self):
        self.c2s = self.s2c = None
        if self.obj is not None:
            files_json = self.obj["files"]
            messages_json = files_json[0]["messages"]
            for item in messages_json:
                long_name = item["longName"]
                if long_name == "C2S":
                    self.c2s = ClassItemStruct(item, "class", self.pb_prefix_name)
                if long_name == "S2C":
                    self.s2c = ClassItemStruct(item, "class", self.pb_prefix_name)

    def load_repeated_parameter(self, obj):
        if obj is None or self.s2c is None or self.c2s is None:
            return

        files_json = obj["files"]
        messages_json = files_json[0]["messages"]

        if self.s2c.has_repeated:
            for item in messages_json:
                full_name = item["fullName"]
                if self.s2c.is_repeated_type(full_name):
                    self.s2c.set_repeated(ClassItemStruct(item, "class", self.pb_prefix_name))

        if self.c2s.has_repeated:
            for item in messages_json:
                full_name = item["fullName"]
                if self.c2s.is_repeated_type(full_name):
                    self.c2s.set_repeated(ClassItemStruct(item, "class", self.pb_prefix_name))

    def out_class(self):
        if self.c2s is None or self.s2c is None:
            return

        export_file = os.path.join(self.local_path, "{}.py".
                                   format(change_variable_name(self.class_name).lower()))
        code_file = open(export_file, 'w', encoding='utf-8')
        function_name = change_variable_name(self.class_name).lower()  # 函数名
        kargs = parameter = warning_filter = ""
        notes = "        " + self.class_name
        pack_req_filter = pack_req_add = ""

        if self.prefix != "":
            pb_file_name = "{}_{}".format(self.prefix, self.class_name)
        else:
            pb_file_name = "{}".format(self.class_name)

        if len(self.c2s.values) < 5:  # 大于5的时候变成结构体
            for i in range(len(self.c2s.values)):
                v = self.c2s.values[i]
                parameter += v.trim_name
                warning_filter += v.get_warning_filter()
                kargs += v.get_args()

                s = v.get_pack_req_filter()
                pack_req_filter += '        \"\"\"check {1} {0}\"\"\"\n'.format(v.description, v.trim_name)
                pack_req_filter += s

                pack_req_add += v.get_pack_req_add()
                if i < (len(self.c2s.values) - 1):
                    parameter += ","
                    kargs += ",\n"

        # with open(os.path.join(self.local_path, __TemplateFileFunctionName__), 'r', encoding='UTF-8') as load_f:
        template_code = template["class_function"]
        unpack_code = self.s2c.get_unpack_code().rstrip('\n')
        code_str = template_code.format(function_name=function_name,
                                        parameter=parameter,
                                        notes=notes,
                                        warning_filter=warning_filter,
                                        class_name=self.class_name,
                                        kargs=kargs,
                                        get_function_return=self.s2c.get_function_return(),
                                        pack_req_filter=pack_req_filter,
                                        pack_req_add=pack_req_add,
                                        pb_file_name=pb_file_name,
                                        get_unpack_code=unpack_code,
                                        get_unpack_return=self.s2c.get_unpack_return())

        code_file.write(code_str)
        code_file.close()

    def out_enums(self):
        if len(self.enums) == 0:
            return
        export_file = os.path.join(self.local_path, "{}_enums.py".format(change_variable_name(self.class_name).lower()))
        with open(os.path.join(self.local_path, __TemplateCodeFileName__), 'r', encoding='UTF-8') as load_f:
            template_code = load_f.read()
        code_file = open(export_file, 'w', encoding='utf-8')
        """写入文件头"""
        with open(os.path.join(self.local_path, __TemplateFileHeadName__), 'r', encoding='UTF-8') as f:
            code_file.write(f.read())

        for class_item in self.enums:
            class_description = class_item.description.replace("\n", "，")
            class_name = class_item.name
            variable_code = ""
            dic_code = ""
            code_file.write("\n\n\n'''-------------------------{}----------------------------'''\n\n\n"
                            .format(class_name))

            for item in class_item.values:
                variablename = item.underscore_name
                strvalue = item.str
                description = item.description
                pbvalue = item.pb_value
                kvcode = "{variablename} = \"{strvalue}\"".format(variablename=variablename, strvalue=strvalue)
                # < 50表示左对齐50个空格

                code = "    {kvcode: <50} # {description}\n".format(kvcode=kvcode, description=description)
                variable_code += code

                code = "            self.{variablename}: {pbvalue},\n".format(
                    variablename=variablename, pbvalue=pbvalue)
                dic_code += code

            c = template_code.format(classdescription=class_description,
                                 classname=class_name,
                                 variablecode=variable_code.rstrip("\n,"),
                                 diccode=dic_code.rstrip("\n,"))
            code_file.write(c)
        code_file.close()

    def rst_enums(self):
        if len(self.enums) == 0:
            return
        export_file = os.path.join(self.local_path, "{}_enums.rst".format(change_variable_name(self.class_name).lower()))
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

    def save(self):
        self.out_enums()
        self.out_class()
        self.rst_enums()




if __name__ =="__main__":
    # import pandas as pd
    # df = pd.DataFrame({'A': 1, 'B': 1}, index=[0])  # 'A'是columns，对应的是list
    # print(df)

    c = GenerateCode("GetCapitalDistribution", "Qot")
    c.load()
    c.save()

# if __name__ =="__main__":
#     print(SortField.to_string("hhh"))
#     print(SortField.to_string(1))
#     print(SortField.to_number("CODE"))
#     print(SortField.to_number(SortField.CODE))
#     print(SortField.to_number(list()))
#     print("-------------------------------------------------------------------")






