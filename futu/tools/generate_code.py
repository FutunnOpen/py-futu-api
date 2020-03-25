# -*- coding: utf-8 -*-

import json
import os
import load_template


#__PBPrefixName__ = "GetGlobalState_pb2."

__TemplateCodeFileName__ = "template_code.txt"
__TemplateFileHeadName__ = "template_head.txt"
__TemplateRstName__ = "rst_template.txt"

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


def code_add_space(code, space_count=1, space_str=" "):  # 逐行加空格
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
        self.var_list = list()
        self.list_list = list()
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
            if item.trim_type == "list" or item.trim_type == "code_list":
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
        var_names = list()
        for item in self.var_list:
            var_names.append(item.trim_name)
        """函数返回，主要是组成pd和解析"""
        if self.repeated_count == 1:
            str_code = '\'' + '\',\n\''.join(var_names) + '\''
            return template["list_return"].format(var_name=code_add_space(str_code, 4))
        elif self.repeated_count == 0:
            str_code = '\'' + '\',\n\''.join(var_names) + '\''
            return template["dict_return"].format(var_name=code_add_space(str_code, 4))
        elif self.repeated_count > 1:
            str_code = ""
            for item in self.list_list:
                var_names.clear()
                col_list = item.col_list
                for v in col_list:
                    var_names.append(v.trim_name)
                var_name = '\'' + '\',\n\''.join(var_names) + '\''
                trim_name = item.trim_name
                str_code += template["list_list_item_return"].format(var_name=code_add_space(var_name, 4),
                                                                     trim_name=trim_name,
                                                                     name=trim_name,
                                                                     description=item.description)

            return template["list_list_return"].format(code=str_code)


    def get_list_head(self):
        """获取列表的头部变量名代码"""
        str_code = ""
        for item in self.values:
            str_code += item.get_unpack_var()
        return str_code

    def get_unpack_code(self):
        self.var_list.clear()

        if self.repeated_count == 1:
            """如果有多个重复数据（列表项），这种方式就不适合了"""
            unpack_add_code = ""
            list_name = "ret_list"
            code, self.var_list = self.get_only_repeated_item().sub_list(list_name)
            head_code = code_add_space("{} = list()\n".format(list_name), 1)
            head_code += self.get_list_head()

            unpack_add_code += code
            head_code = code_add_space(head_code, 1)
            return head_code + unpack_add_code

        elif self.repeated_count == 0:
            unpack_code = ""
            """开始遍历赋值"""
            for item in self.values:
                unpack_code += item.get_unpack_dict_code("ret")
                self.var_list.append(item)
            return template["class_unpack_var_add"].format(unpack_code=unpack_code.rstrip('\n'))

        elif self.repeated_count > 1:
            self.list_list.clear()
            code_str = ""
            head_code = "ret_dic = dict()\n" + self.get_list_head()
            for item in self.values:
                if item.trim_type == "list":
                    self.list_list.append(item)
                    list_name = "ret_list_" + item.trim_name
                    item.list_name = list_name
                    head_code += template["class_more_list_add"].format(description=item.description,
                                                                        list_name=list_name,
                                                                        var_name=item.trim_name)
            for item in self.list_list:
                s, l = item.sub_list(item.list_name)
                item.col_list = l
                code_str += s

            return code_add_space(head_code, 1) + code_str

    def get_unpack_return(self):
        if self.repeated_count == 1:
            return "return RET_OK, \"\", ret_list"
        elif self.repeated_count == 0:
            return "return RET_OK, \"\", ret"
        elif self.repeated_count > 1:
            return "return RET_OK, \"\", ret_dic"


class BaseClass(ClassItemStruct):
    def __init__(self, full_type):
        self.name = full_type
        self.description = "base type " + full_type
        self.json_obj = None
        self.pb_prefix_name = None
        self.class_type = "class"
        self.repeated_count = 0
        self.var_list = list()
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
        self.description = obj["description"].replace('\n', '')

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
        self.python_type = obj["longType"]  # python对应的变量名
        self.trim_name = change_variable_name(self.name).lower() # 整理后的名字
        self.description = obj["description"].replace('\n', '')
        self.label = obj["label"]

        self.trim()

    def trim(self):
        if self.obj is None:
            return
        # 嵌套了复杂类型list
        if self.label == "repeated":
            if self.full_type == "Qot_Common.Security":
                self.trim_type = "code_list"
                if self.trim_name == "security_list":
                    self.trim_name = "code_list"
            else:
                self.trim_type = "list"

        # 股票代码类型需要特殊处理
        elif self.full_type == "Qot_Common.Security":
            self.trim_type = "code"
            if self.trim_name == "security":
                self.trim_name = "stock_code"
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

        elif self.full_type in ["int32", "int64", "double", "float", "string", "bool", "bytes"]:
            self.self_class = BaseClass(self.full_type)

        self.python_type = self.trim_type
        if self.trim_type in ["int32", "int64"]:
            self.python_type = "int"
        if self.trim_type in ["double", "float"]:
            self.python_type = "float"


    def get_args(self):
        return "            \"{}\": {},".format(self.trim_name, self.trim_name)

    def get_warning_filter(self):
        warning_filter = ""
        if self.trim_type == "code_list":
            warning_filter = template.get("code_list_warning_filter", 2)
        elif self.trim_type == "code":
            warning_filter = template.get("code_warning_filter", 2).format(trim_name=self.trim_name)
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
        return ""

    def get_pack_req_add(self):
        if self.trim_type == "code_list":
            return template.get("pack_code_list_add", 2).format(name=self.name)
        elif self.trim_type == "code":
            return "        req.c2s.{0}.market = market_code\n" \
                   "        req.c2s.{0}.code = stock_code".format(self.name)
        else:
            return "        req.c2s.{0} = {1}\n".format(self.name, self.trim_name)

    def set_class(self, class_obj):
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
            return s_code

    def sub_list(self, list_name, sub_item_name="item", add_code=""):
        if self.self_class is None or self.self_class.repeated_count > 1:
            raise Exception("不能支持子节点有多个列表的情况")

        str_code = for_code = ""
        ret_list = list()

        if sub_item_name == "item":  # 顶级节点,把父节点的，也就是顶层父节点的数据加进去
            if self.name == "test":
                sub_item_name = "item"
            for item in self.class_owner.values:
                if item.trim_type != "list" and self.trim_type != "timestamp":
                    ret_list.append(item)
                    add_code += code_add_space(("data[\"{0}\"] = {0}\n".format(item.trim_name)), 1)

        if self.self_class.repeated_count == 1:  # 下面子节点仍然有list
            for item in self.self_class.values:
                if self.trim_type == "timestamp":
                    continue
                """加入自己那层的数据"""
                str_code += code_add_space(item.get_unpack_var(sub_item_name), 1)
                if item.trim_type != "list":
                    ret_list.append(item)
                    add_code += code_add_space(("data[\"{0}\"] = {0}\n".format(item.trim_name)), 1)
            sub_sub_item_name = "sub_" + sub_item_name

            s, l = self.self_class.get_only_repeated_item().sub_list(list_name, sub_sub_item_name, add_code)
            str_code += s
            ret_list.extend(l)

        elif self.self_class.repeated_count == 0:
            """理解为最后一层"""
            for item in self.self_class.values:
                if self.trim_type == "timestamp":
                    continue
                str_code += code_add_space(item.get_item_unpack_add(sub_item_name), 1)
                ret_list.append(item)
            str_code += add_code

        for_code = "for {sub_item} in {trim_name}:\n". \
            format(trim_name=self.trim_name,
                   sub_item=sub_item_name)
        if self.self_class.repeated_count == 0:
            for_code += "	{list_name}.append(data)\n". \
                format(list_name=list_name)

        return code_add_space(for_code + str_code, 1), ret_list



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
        print("GenerateCode class_name = {} | prefix = {}".format(class_name, prefix))
        self.local_path = os.path.dirname(os.path.realpath(__file__))
        self.common_pb_path = os.path.abspath(os.path.join(self.local_path, "../common/pb/"))
        self.out_put_path = os.path.join(self.local_path, "code")
        if not os.path.exists(self.out_put_path):
            os.makedirs(self.out_put_path)

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
        with open(os.path.join(self.common_pb_path, self.json_filename), 'r', encoding='UTF-8') as load_f:
            self.obj = json.load(load_f)
            self.load_enums()
            self.load_parameter()
            for i in range(10):
                self.set_parameter_class(self.obj)  # 嵌套重复元素
        with open(os.path.join(self.common_pb_path, "Qot_Common.proto.json"), 'r', encoding='UTF-8') as load_f:
            self.set_parameter_class(json.load(load_f))
        with open(os.path.join(self.common_pb_path, "Trd_Common.proto.json"), 'r', encoding='UTF-8') as load_f:
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

        export_file = os.path.join(self.out_put_path, "{}.py".
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
            pack_req_filter += '        \"\"\"check {1} {0}\"\"\"\n'.format(v.description, v.trim_name)
            pack_req_filter += s

            pack_req_add += v.get_pack_req_add()
            if i < (len(self.c2s.values) - 1):
                parameter += ","
                kargs += ",\n"

        # with open(os.path.join(self.local_path, __TemplateFileFunctionName__), 'r', encoding='UTF-8') as load_f:
        template_code = template["class_function"]
        unpack_code = code_add_space(self.s2c.get_unpack_code().rstrip('\n'),1)
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
                                        get_unpack_code= unpack_code,
                                        get_unpack_return=self.s2c.get_unpack_return())

        code_file.write(code_str)
        code_file.close()

    def out_enums(self):
        if len(self.enums) == 0:
            return
        export_file = os.path.join(self.out_put_path, "{}_enums.py".format(change_variable_name(self.class_name).lower()))
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
        export_file = os.path.join(self.out_put_path, "{}_enums.rst".format(change_variable_name(self.class_name).lower()))
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

    def rst_class(self):
        if self.c2s is None or self.s2c is None:
            return

        export_file = os.path.join(self.out_put_path, "{}.rst".
                                   format(change_variable_name(self.class_name).lower()))
        code_file = open(export_file, 'w', encoding='utf-8')
        code_str = ""
        for i in range(len(self.s2c.values)):
            v = self.s2c.values[i]
            description = v.description
            python_type = v.python_type
            name = v.trim_name
            line = " {:<32}{:<15}{}\n".format(name, python_type, description)
            code_str += line

        code_file.write(code_str)
        code_file.close()

    def save(self):
        self.out_enums()
        self.out_class()
        self.rst_enums()
        self.rst_class()


class Generate(object):
    def __init__(self):
        self.local_path = os.path.dirname(os.path.realpath(__file__))
        self.common_pb_path = os.path.abspath(os.path.join(self.local_path, "../common/pb/"))
        self.pb_list = list()

        """统统载入进来再说"""
        f_list = os.listdir(self.common_pb_path)
        for f in f_list:
            if os.path.splitext(f)[1] == '.proto':
                self.pb_list.append(f)

    def find_pb_by_names(self, names):
        f_list = list()
        for f in self.pb_list:
            (_, file_name) = os.path.split(f)
            for s in names:
                if f.find(s) != -1:
                    f_list.append(f)
                    break
        return f_list

    def generate_json(self, names=None):
        if names is not None:
            f_list = self.find_pb_by_names(names)
        else:
            f_list = self.pb_list

        for f in f_list:
            (_, file_name) = os.path.split(f)

            cmd = '''cd /d {work_path} & \
                  protoc.exe -I=. --python_out=./  {file_name} & \
                  protoc.exe --doc_out=. --doc_opt=json,{file_name}.json ./{file_name} &'''\
                .format(file_name=file_name,
                        work_path=self.common_pb_path)
            os.system(cmd)
            print(cmd)

    def generate_code(self, names):
        if names is not None:
            pb_list = self.find_pb_by_names(names)
        else:
            pb_list = self.pb_list

        for f in pb_list:
            (_, file_name) = os.path.split(f)
            json_file_path = os.path.join(self.common_pb_path, file_name + ".json")
            if not os.path.exists(json_file_path):
                print(json_file_path + " not exists")
                continue
            (name, _) = os.path.splitext(file_name)

            if name.find("Qot_") == 0:
                prefix = "Qot"
                class_name = name[4:]
            elif name.find("Trd_") == 0:
                prefix = "Trd"
                class_name = name[4:]
            else:
                prefix = ""
                class_name = name

            if class_name in ["Common", "Sub"]:
                continue
            code = GenerateCode(class_name, prefix)
            code.load()
            code.save()


def generate(names):
    if isinstance(names, str):
        names = [names]
    gener = Generate()
    gener.generate_json(names)
    gener.generate_code(names)


if __name__ =="__main__":
    generate(None)
    # c = GenerateCode("GetOwnerPlate", "Qot")
    # c.load()
    # c.save()






