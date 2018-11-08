# -*- coding: utf-8 -*-

from futu.common import bytes_utf8, IS_PY2
from futu.common.utils import *
from futu.common.sys_config import SysConfig
from Crypto.Cipher import AES


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

        if 'aes_cryptor' not in conn_info:
            key = FutuConnMng.get_conn_key(conn_id)
            if not key:
                return None

            key_tmp = bytes_utf8(str(key))
            cryptor = AES.new(key_tmp, AES.MODE_ECB)
            conn_info['aes_cryptor'] = cryptor
            return cryptor

        return conn_info['aes_cryptor']

    @classmethod
    def encrypt_conn_data(cls, conn_id, data):
        if not SysConfig.is_proto_encrypt():
            return RET_OK, '', data

        if type(data) is not bytes:
            data = bytes_utf8(str(data))

        len_src = len(data)
        mod_tail_len = (len_src % 16)

        # AES 要求源数据长度是16的整数倍， 不足的话要补0
        if mod_tail_len != 0:
            data += (b'\x00' * (16 - mod_tail_len))

        aes_cryptor = FutuConnMng.get_conn_aes_cryptor(conn_id)
        if aes_cryptor:
            data = aes_cryptor.encrypt(data)

            # 增加一个16字节的数据块（目前只有最后一个字节有用），如果对原数据有补数据，记录原数据最后一个数据块真实长度
            data_tail = b'\x00' * 15 + bytes_utf8(chr(mod_tail_len))

            data_tail = data_tail[-16:]
            data += data_tail
            return RET_OK, '', data

        return RET_ERROR, 'invalid connid', data

    @classmethod
    def decrypt_conn_data(cls, conn_id, data):
        if not SysConfig.is_proto_encrypt():
            return RET_OK, '', data

        # tail的未尾字节记录解密数据的最一个数据块真实的长度
        data_real = data[:len(data) - 16]
        data_tail = data[-1:]
        import struct
        mem_tmp = b'\0\0\0' + data_tail
        tail_real_len = struct.unpack(">L", mem_tmp)[0]
        # tail_real_len = int.from_bytes(data_tail, 'little')

        aes_cryptor = FutuConnMng.get_conn_aes_cryptor(conn_id)

        if aes_cryptor:
            if IS_PY2:
                de_data = aes_cryptor.decrypt(str(data_real))
            else:
                de_data = aes_cryptor.decrypt(data_real)

            # 去掉在加密前增加的额外数据
            if tail_real_len != 0:
                cut_len = 16 - tail_real_len
                de_data = de_data[0: len(de_data) - cut_len]

            return RET_OK, '', de_data

        return RET_ERROR, 'AES decrypt error, conn_id:{}'.format(conn_id), data




