# -*- coding: utf-8 -*-

from futu.common import bytes_utf8, IS_PY2
from futu.common.utils import *
from futu.common.constant import *
from futu.common.sys_config import SysConfig
from Crypto.Cipher import AES
from futu.common.constant import *
import struct


def add_pkcs7_padding(data):
    padding_len = 16 - len(data) % 16
    if padding_len == 0:
        padding_len = 16
    return data + struct.pack('B', padding_len) * padding_len


def remove_pkcs7_padding(data):
    padding_len = data[-1]
    return data[:len(data) - padding_len]


class FutuConnMng(object):
    All_Conn_Dict = {}

    @classmethod
    def add_conn(cls, conn_dict):
        all_conn = FutuConnMng.All_Conn_Dict
        conn_id = conn_dict['conn_id']
        all_conn[conn_id] = conn_dict

    @classmethod
    def remove_conn(cls, conn_id):
        all_conn = FutuConnMng.All_Conn_Dict
        if conn_id in all_conn:
            all_conn.pop(conn_id)

    @classmethod
    def get_conn_info(cls, conn_id):
        all_conn = FutuConnMng.All_Conn_Dict
        return all_conn[conn_id] if conn_id in all_conn else None

    @classmethod
    def get_conn_key(cls, conn_id):
        conn_info = FutuConnMng.get_conn_info(conn_id)
        return conn_info['conn_key'] if conn_info else None

    @classmethod
    def get_conn_user_id(cls, conn_id):
        conn_info = FutuConnMng.get_conn_info(conn_id)
        return conn_info['login_user_id'] if conn_info else 0

    @classmethod
    def get_conn_aes_cryptor(cls, conn_id):
        conn_info = FutuConnMng.get_conn_info(conn_id)
        if not conn_info:
            return None

        key = conn_info.get('conn_key')
        iv = conn_info.get('conn_iv')
        if not key:
            return None
        key = bytes_utf8(key)
        if iv:  # AES CBC加密
            iv = bytes_utf8(iv)
            return AES.new(key, AES.MODE_CBC, iv=iv)
        else:  # FTAES ECB加密
            if 'aes_cryptor' not in conn_info:
                cryptor = AES.new(key, AES.MODE_ECB)
                conn_info['aes_cryptor'] = cryptor
                return cryptor

            return conn_info['aes_cryptor']

    @classmethod
    def encrypt_conn_data(cls, conn_id, data):
        if type(data) is not bytes:
            data = bytes_utf8(str(data))

        conn_info = FutuConnMng.get_conn_info(conn_id)
        if not conn_info:
            return RET_ERROR, 'invalid connid', data

        aes_cryptor = FutuConnMng.get_conn_aes_cryptor(conn_id)
        if not aes_cryptor:
            return RET_ERROR, 'invalid connid', data

        has_conn_iv = conn_info.get('conn_iv') is not None
        if not has_conn_iv:  # FTAES ECB
            len_src = len(data)
            mod_tail_len = (len_src % 16)

            # AES 要求源数据长度是16的整数倍， 不足的话要补0
            if mod_tail_len != 0:
                data += (b'\x00' * (16 - mod_tail_len))

            data = aes_cryptor.encrypt(data)

            # 增加一个16字节的数据块（目前只有最后一个字节有用），如果对原数据有补数据，记录原数据最后一个数据块真实长度
            data_tail = b'\x00' * 15 + bytes_utf8(chr(mod_tail_len))

            data_tail = data_tail[-16:]
            data += data_tail
            return RET_OK, '', data
        else:  # AES CBC
            data = add_pkcs7_padding(data)
            return RET_OK, '', aes_cryptor.encrypt(data)

    @classmethod
    def decrypt_conn_data(cls, conn_id, data):
        conn_info = FutuConnMng.get_conn_info(conn_id)
        if not conn_info:
            return RET_ERROR, 'invalid connid', data

        aes_cryptor = FutuConnMng.get_conn_aes_cryptor(conn_id)
        if not aes_cryptor:
            return RET_ERROR, 'invalid connid', data

        has_conn_iv = conn_info.get('conn_iv') is not None
        if not has_conn_iv:  # FTAES ECB
            # tail的未尾字节记录解密数据的最一个数据块真实的长度
            data_real = data[:len(data) - 16]
            data_tail = data[-1:]
            import struct
            mem_tmp = b'\0\0\0' + data_tail
            tail_real_len = struct.unpack(">L", mem_tmp)[0]
            # tail_real_len = int.from_bytes(data_tail, 'little')

            if IS_PY2:
                de_data = aes_cryptor.decrypt(str(data_real))
            else:
                de_data = aes_cryptor.decrypt(data_real)

            # 去掉在加密前增加的额外数据
            if tail_real_len != 0:
                cut_len = 16 - tail_real_len
                de_data = de_data[0: len(de_data) - cut_len]

            return RET_OK, '', de_data
        else:  # AES CBC
            de_data = aes_cryptor.decrypt(data)
            de_data = remove_pkcs7_padding(de_data)
            return RET_OK, '', de_data

    @classmethod
    def is_conn_encrypt(cls, conn_id):
        conn_info = cls.get_conn_info(conn_id)
        if conn_info:
            return conn_info['is_encrypt']
        return SysConfig.is_proto_encrypt()
