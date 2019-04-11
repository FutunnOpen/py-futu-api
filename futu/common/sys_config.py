# -*- coding: utf-8 -*-
import os
import sys
import traceback
from futu.common import bytes_utf8, IS_PY2, str_utf8
from futu.common.constant import *
from futu.common.ft_logger import logger
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1
from Crypto import Random


class SysConfig(object):
    IS_PROTO_ENCRYPT = False                # api通讯协议是否加密
    INIT_RSA_FILE = ''                      # 初始连接协议用到的rsa private key file
    RSA_OBJ = None                          # ras加解密对象
    PROTO_FMT = None                        # 协议格式
    CLINET_ID = None                        # Client标识
    CLIENT_VER = None                       # Client ver
    ALL_THREAD_DAEMON = False               # 是否所有产生的线程都是daemon线程

    @classmethod
    def set_client_info(cls, client_id, client_ver):
        """
        ..  py:function:: set_client_info(cls, client_id, client_ver)

        设置调用api的客户端信息, 非必调接口

        :param client_id: str, 客户端标识
        :param client_ver: int, 客户端版本号
        :return: None

        :example:

        .. code:: python

         from futu import *
         SysConfig.set_client_info("MyFutuAPI", 0)
         quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
         quote_ctx.close()

        """

        SysConfig.CLINET_ID = client_id
        SysConfig.CLIENT_VER = client_ver

    @classmethod
    def get_client_id(cls):
        return SysConfig.CLINET_ID if SysConfig.CLINET_ID else DEFULAT_CLIENT_ID

    @classmethod
    def get_client_ver(cls):
        return SysConfig.CLIENT_VER if SysConfig.CLIENT_VER is not None else CLIENT_VERSION

    @classmethod
    def get_proto_fmt(cls):
        return SysConfig.PROTO_FMT if SysConfig.PROTO_FMT else DEFULAT_PROTO_FMT

    @classmethod
    def set_proto_fmt(cls, proto_fmt):
        """

        ..  py:function:: set_proto_fmt(cls, proto_fmt)

        设置通讯协议body格式, 目前支持Protobuf | Json两种格式, 非必调接口

        :param proto_fmt: ProtoFMT
        :return: None

        :example:

        .. code:: python

         from futu import *
         SysConfig.set_proto_fmt(ProtoFMT.Protobuf)
         quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
         quote_ctx.close()

        """
        fmt_list = [ProtoFMT.Protobuf, ProtoFMT.Json]

        if proto_fmt not in fmt_list:
            raise Exception("proto_fmt error")
        SysConfig.PROTO_FMT = proto_fmt

    @classmethod
    def enable_proto_encrypt(cls, is_encrypt):
        """
        ..  py:function:: enable_proto_encrypt(cls, is_encrypt)

        设置通讯协议是否加密, 网关客户端和api需配置相同的RSA私钥文件,在连接初始化成功后，网关会下发随机生成的AES 加密密钥

        :param is_encrypt: bool
        :return: None

        :example:

        .. code:: python

         from futu import *
         SysConfig.enable_proto_encrypt(True)
         SysConfig.set_init_rsa_file("conn_key.txt")   # rsa 私钥文件路径
         quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
         quote_ctx.close()

        """
        SysConfig.IS_PROTO_ENCRYPT = bool(is_encrypt)

    @classmethod
    def set_init_rsa_file(cls, file):
        """
        ..  py:function:: set_init_rsa_file(cls, file)

        设置RSA私钥文件, 要求1024位, 格式为PKCS#1

        :param file:  str, 文件路径
        :return: None

        :example:

        .. code:: python

         from futu import *
         SysConfig.enable_proto_encrypt(True)
         SysConfig.set_init_rsa_file("conn_key.txt")   # rsa 私钥文件路径
         quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
         quote_ctx.close()

        """
        SysConfig.INIT_RSA_FILE = str(file)
        SysConfig.RSA_OBJ = None
        RsaCrypt.CHIPPER = None

    @classmethod
    def get_init_rsa_obj(cls):
        """
        :return: str , private key for init connect protocol
        """

        if not SysConfig.RSA_OBJ:
            SysConfig._read_rsa_keys()

        return SysConfig.RSA_OBJ

    @classmethod
    def is_proto_encrypt(cls):
        """
        :return: bool
        """
        return SysConfig.IS_PROTO_ENCRYPT

    @classmethod
    def _read_rsa_keys(cls):
        file_path = SysConfig.INIT_RSA_FILE if SysConfig.INIT_RSA_FILE \
            else os.path.join(os.path.dirname(__file__), DEFAULT_INIT_PRI_KEY_FILE)

        try:
            f = open(file_path, 'rb')
            df = f.read()
            if type(df) is not str:
                df = str_utf8(df)

            rsa = RSA.importKey(df)
            pub_key = rsa.publickey().exportKey()
            if not pub_key:
                raise Exception("Illegal format of file content")

            SysConfig.RSA_OBJ = rsa

        except Exception as e:
            traceback.print_exc()
            err = sys.exc_info()[1]
            err_msg = "Fatal error occurred in getting proto key, detail:{}".format(err)
            logger.error(err_msg)
            raise Exception(err_msg)

    @classmethod
    def set_all_thread_daemon(cls, all_daemon):
        """
        设置是否所有内部创建的线程都是daemon线程
        :param all_daemon: bool
        :return:
        """
        SysConfig.ALL_THREAD_DAEMON = all_daemon

    @classmethod
    def get_all_thread_daemon(cls):
        return SysConfig.ALL_THREAD_DAEMON


class RsaCrypt(object):
    RANDOM_GENERATOR = Random.new().read
    CHIPPER = None
    @classmethod
    def encrypt(cls, data):
        if RsaCrypt.CHIPPER is None:
            rsa = SysConfig.get_init_rsa_obj()
            RsaCrypt.CHIPPER = Cipher_pkcs1.new(rsa)

        if type(data) is not bytes:
            data = bytes_utf8(str(data))

        # 单次加密串的长度最大为(key_size / 8) - 11
        # 1024 bit的证书用100， 2048 bit的证书用 200
        one_len = 100
        ret_data = b''
        for i in range(0, len(data), one_len):
            ret_data += RsaCrypt.CHIPPER.encrypt(data[i:i + one_len])
        return ret_data

    @classmethod
    def decrypt(cls, data):
        if RsaCrypt.CHIPPER is None:
            rsa = SysConfig.get_init_rsa_obj()
            RsaCrypt.CHIPPER = Cipher_pkcs1.new(rsa)

        # 1024 bit的证书用128，2048 bit证书用256位
        one_len = 128
        ret_data = b''

        # python2下需转成str类型,否则异常
        if IS_PY2:
            data = str(data)

        for i in range(0, len(data), one_len):
            ret_data += RsaCrypt.CHIPPER.decrypt(data[i:i + one_len], RsaCrypt.RANDOM_GENERATOR)

        return ret_data


"""
test_str = 'futu api' * 32
dt_encrypt = RsaCrypt.encrypt(test_str)
print(dt_encrypt)
dt_decrypt = RsaCrypt.decrypt(dt_encrypt)
print(dt_decrypt)
"""

"""
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

key = b'0123456789abcdef'
cryptor = AES.new(key, AES.MODE_ECB, key)

src = b'123'
len_src = len(src)
add = 16 - (len_src % 16)
src = src
src2 = src + (b'\0' * add)

dst = cryptor.encrypt(src2)
hex_dst = b2a_hex(dst)
print(hex_dst)

src3 = cryptor.decrypt(dst)
print("len={} decrypt={}".format(len(src3), src3))
"""





