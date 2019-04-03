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


template = load_template.FutuTemplate("function.template")



def change_variable_name(listx):  # 修改变量名
    """把骆驼变量名变成下划线的方式（全大写）"""
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
    """传入字符串，逐行加入空格，符合python规范"""
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

class ClassItemStruct(object):

    def __init__(self, json_obj, class_type, pb_prefix_name):
        self.name = json_obj["longName"]
        self.full_name = json_obj["fullName"]
        self.description = json_obj["description"]
        self.json_obj = json_obj
        self.pb_prefix_name = pb_prefix_name
        self.class_type = class_type
        self.repeated_count = 0
        self.repeated_var_list = list()
        self.vars_dict = dict()
        self.values = list()

        if class_type == "enums":
            for v in json_obj["values"]:
                s = EnumsItemStruct(v, self.name, self.pb_prefix_name)
                self.values.append(s)

        if class_type == "class":
            for v in json_obj["fields"]:
                s = ParameterItem(v, self)
                if s.label == "repeated":
                    #self.has_repeated = True
                    self.repeated_count += 1
                self.values.append(s)

    def get_only_repeated_item(self):
        for item in self.values:
            if item.trim_type == "list":
                return item

    # def is_repeated_type(self, full_name):
    #     for item in self.values:
    #         if item.full_type == full_name:
    #             return True
    #     return False

    def set_parameter_class(self, class_obj):
        for item in self.values:
            item.set_class(class_obj)

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
            unpack_add = ""
            list_name = "ret_list"
            code, var_list = self.get_only_repeated_item().sub_list(list_name)
            ls = list()
            for item in var_list:
                ls.append(item.trim_name)
            self.vars_dict[list_name] = ls
            unpack_add += code_add_space(code, 1)
            return template["class_unpack_list_add"].format(unpack_add=unpack_add.rstrip('\n'),
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
                    s_code, _ = item.get_unpack_list_add(list_name)
                    for v in self.values:
                        if v.trim_name not in self.repeated_var_list and v.label != "repeated":
                            """其他元素压平合并进去"""
                            s_code += v.get_unpack_add()

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


class BaseClass(ClassItemStruct):
    def __init__(self, full_type):
        self.name = full_type
        self.description = "base type " + full_type
        self.json_obj = None
        self.pb_prefix_name = None
        self.class_type = "class"
        self.repeated_count = 0
        self.repeated_var_list = list()
        self.vars_dict = dict()
        self.full_name = full_type
        self.values = list()


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
        self.pb_prefix_name = class_owner.pb_prefix_name
        self.self_class = None
        # self.repeated_class = None

        self.name = obj["name"] # 原始变量名
        self.full_type = obj["fullType"] # 原始变量名
        self.trim_type = obj["longType"]  # 原始变量名
        self.trim_name = change_variable_name(self.name).lower() # 整理后的名字
        self.description = obj["description"]
        self.label = obj["label"]

        self.trim()

    def trim(self):
        if self.obj is None:
            return
        # 嵌套了复杂类型list
        if self.label == "repeated":
            if self.full_type == "Qot_Common.Security":
                self.trim_type = "code_list"
            else:
                self.trim_type = "list"
        # 股票代码类型需要特殊处理
        elif self.full_type == "Qot_Common.Security":
            self.trim_type = "code"
        # timestamp类型需要跳过
        elif self.full_type == "double" and self.name.lower().find("timestamp") != -1:
            self.trim_type = "timestamp"

        # 时间特殊处理，因为time、code太笼统
        if self.trim_name == "time" or self.trim_name == "code":
            self.trim_name = "{}_{}".format(change_variable_name(self.class_owner.name).lower(), self.trim_name)

        # 注释太短了的不知所云
        if len(self.description) < 5:
            if len(self.class_owner.description) > 0:
                self.description = self.class_owner.description + "  " + self.description

        #名字太短了容易撞车
        if len(self.trim_name) < 5:
            owner_name = change_variable_name(self.class_owner.name).lower()
            if owner_name != "s2c" and owner_name != "c2s" and owner_name != "":
                self.trim_name = "{}_{}".format(owner_name, self.trim_name)

        if self.trim_type in ["int32", "int64", "double",
                              "float", "string", "bool", "bytes", "code_list",
                              "code", "timestamp"]:
            self.self_class = BaseClass(self.trim_type)

    def get_args(self):
        return "            \"{}\": {},".format(self.trim_name, self.trim_name)

    def get_warning_filter(self):
        if self.trim_type == "code_list":
            warning_filter = template.get("code_list_warning_filter", 2)
        elif self.trim_type == "code":
            warning_filter = template.get("code_warning_filter", 2)
        return warning_filter

    def get_parameter_name(self):
        if self.trim_type == "code_list":
            return "code_list"
        elif self.trim_type == "code":
            return "stock_code"
        return self.trim_name

    def get_pack_req_filter(self):
        if self.trim_type == "code_list":
            return template.get("pack_code_list_filter", 2)
        elif self.trim_type == "code":
            return template.get("pack_code_filter", 2)

    def get_pack_req_add(self):
        if self.trim_type == "code_list":
            return template.get("pack_code_list_add", 2).format(name=self.name)
        elif self.trim_type == "code":
            return "        req.c2s.{0}.market = market_code\n" \
                   "        req.c2s.{0}.code = stock_code".format(self.name)
        else:
            return "        req.c2s.{0} = {1}\n".format(self.name, self.trim_name)

    def set_class(self, class_obj):
        print(class_obj.full_name)
        if (self.self_class is None) and (self.full_type == class_obj.full_name):
            self.self_class = class_obj
        """遍历问问子节点"""
        if (self.self_class is not None) and (not isinstance(self.self_class, BaseClass)):
            for item in self.self_class.values:
                item.set_class(class_obj)

    def get_unpack_var(self, parents_name="rsp_pb.s2c"):
        if self.trim_type == "timestamp":
            return ""
        else:
            if self.full_type == "Qot_Common.Security":
                s_code = template["class_unpack_code"].format(trim_name=self.trim_name,
                                                              name=self.name,
                                                              parents_name=parents_name)
            else:
                s_code = "#  {description} type = {trim_type}\n" \
                         "{trim_name} = {parents_name}.{name}\n".\
                    format(description=self.description,
                           trim_type=self.full_type,
                           trim_name=self.trim_name,
                           parents_name=parents_name,
                           name=self.name)
            return code_add_space(s_code, 1)

    def sub_list(self, list_name, sub_item_name="item", add_code=""):
        if self.self_class.repeated_count > 1:
            raise Exception("不能支持子节点有多个列表的情况")

        head_code = str_code = for_code = ""
        ret_list = list()

        if self.self_class.repeated_count == 1:
            my_add_code = ""
            if sub_item_name == "item":  # 顶级节点
                for item in self.class_owner.values:
                    if item.trim_type != "list":
                        ret_list.append(item)
                        head_code += item.get_unpack_var()
                        my_add_code += code_add_space(("data[\"{0}\"] = {0}\n".format(item.trim_name)), 1)
            for item in self.self_class.values:
                str_code += item.get_unpack_var(sub_item_name)
                if item.trim_type != "list":
                    ret_list.append(item)
                    my_add_code += code_add_space(("data[\"{0}\"] = {0}\n".format(item.trim_name)), 1)
            sub_sub_item_name = "sub_" + sub_item_name
            add_code += my_add_code

            s, l = self.self_class.get_only_repeated_item().sub_list(list_name, sub_sub_item_name, add_code)
            str_code += s
            ret_list.extend(l)

        elif self.self_class.repeated_count == 0:
            """理解为最后一层"""
            for item in self.self_class.values:
                str_code += code_add_space(item.get_item_unpack_add(sub_item_name), 1)
                ret_list.append(item)
            str_code += add_code

        for_code = "for {sub_item} in {trim_name}:\n". \
            format(trim_name=self.trim_name,
                   sub_item=sub_item_name)
        if self.self_class.repeated_count == 0:
            for_code += "	{list_name}.append(data)\n". \
                format(list_name=list_name)

        return head_code + code_add_space(for_code + str_code, 1), ret_list

    def get_item_unpack_add(self, item_name=""):
        if self.trim_type == "timestamp" or self.trim_type == "list":
            return ""
        else:
            if len(item_name) > 0:
                item_name += "."
            if self.trim_type == "code" and item_name != "":
                s_code = "merge_qot_mkt_stock_str({parents_name}.{name}.market,{parents_name}.{name}.code)".\
                    format(name=self.name,
                           parents_name=item_name).rstrip('\n')

                return "#  {description} type = {trim_type}\n" \
                       "data[\"{trim_name}\"] = {code}\n".\
                    format(description=self.description,
                           trim_type=self.trim_type,
                           trim_name=self.trim_name,
                           code=s_code)
            else:
                return "#  {description} type = {trim_type}\n" \
                       "data[\"{trim_name}\"] = {item_name}{name}\n".\
                    format(description=self.description,
                           trim_type=self.trim_type,
                           trim_name=self.trim_name,
                           item_name=item_name,
                           name=self.name)



    # def get_unpack_list_add(self, ret_list_name):
    #     """用于列表遍历"""
    #     name_list = list()
    #     if self.trim_type == "list" and self.self_class is not None:
    #         str_code = ""
    #         for item in self.self_class.values:
    #             if self.trim_type == "timestamp":
    #                 continue
    #             if item.trim_type == "list":
    #                 sub_item_name = "sub_item"
    #                 s, l = self._sub_list(item, sub_item_name, ret_list_name)
    #                 str_code += code_add_space(s, 1)
    #                 name_list.extend(l)
    #             else:
    #                 str_code += item.get_item_unpack_add("item.")
    #             name_list.append(item.trim_name)
    #
    #         if self.self_class.repeated_count == 0:
    #             head_code = "for item in {trim_name}:\n" \
    #                 "	data = dict()\n" \
    #                 "	{list_name}.append(data)\n".\
    #                 format(trim_name=self.trim_name, list_name=ret_list_name)
    #             return code_add_space(head_code, 2) + code_add_space(str_code, 3), name_list
    #
    #     return "", name_list

    # def get_unpack_sub_list_add(self, ret_list_name, sub_item_name):
    #     """用于列表的列表遍历"""
    #     name_list = list()
    #     str_code = ""
    #     for item in self.self_class.values:
    #         if self.trim_type == "timestamp":
    #             continue
    #         if item.trim_type == "list":
    #             sub_sub_item_name = "sub_" + sub_item_name
    #             s, l = self._sub_list(item, sub_sub_item_name, ret_list_name)
    #         else:
    #             str_code += item.get_item_unpack_add("item.")
    #         name_list.append(item.trim_name)
    #     return code_add_space(str_code, 1), name_list

    # def get_unpack_add(self):
    #     return code_add_space(self.get_item_unpack_add(), 3)

    def get_unpack_dict_code(self, ret_name):
        if self.trim_type == "timestamp":
            return ""
        else:
            if self.full_type == "Qot_Common.Security":
                s_code = "#  {description} type={trim_type}\n" \
                         "{ret_name}[\"{trim_name}\"]= merge_qot_mkt_stock_str({trim_name}.market, {trim_name}.code)\n". \
                    format(description=self.description,
                           trim_type=self.trim_type,
                           trim_name=self.trim_name,
                           ret_name=ret_name)
            else:
                s_code = "#  {description} type={trim_type}\n" \
                         "{ret_name}[\"{trim_name}\"]=rsp_pb.s2c.{name}\n".\
                    format(description=self.description,
                           trim_type=self.trim_type,
                           trim_name=self.trim_name,
                           name=self.name,
                           ret_name=ret_name)
            return code_add_space(s_code, 2)


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
            self.set_parameter_class(self.obj)  # 嵌套重复元素
            self.set_parameter_class(self.obj)  # 嵌套重复元素
        with open(os.path.join(self.local_path, "Qot_Common.proto.json"), 'r', encoding='UTF-8') as load_f:
            self.set_parameter_class(json.load(load_f))

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

    def set_parameter_class(self, obj):
        if obj is None or self.s2c is None or self.c2s is None:
            return

        files_json = obj["files"]
        messages_json = files_json[0]["messages"]

        for item in messages_json:
            class_obj = ClassItemStruct(item, "class", self.pb_prefix_name)
            self.s2c.set_parameter_class(class_obj)
            self.c2s.set_parameter_class(class_obj)

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

        # 大于5的时候变成结构体
        for i in range(len(self.c2s.values)):
            v = self.c2s.values[i]
            parameter += v.get_parameter_name()
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
    c = GenerateCode("GetOwnerPlate", "Qot")
    c.load()
    c.save()






