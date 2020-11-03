# -*- coding: utf-8 -*-

from collections import namedtuple

_ErrField = namedtuple('_ErrField', ('code', 'text'))


class Err:
    """
    0 ~ 999 通用错误
    1000 ~ 1999 行情错误
    2000 ~ 2999 交易错误
    """
    Ok = _ErrField(0, 'Ok')
    ConnectionLost = _ErrField(1, 'Connection lost')
    Timeout = _ErrField(2, 'Timeout')
    NotConnected = _ErrField(3, 'Not connected')
    PacketDataErr = _ErrField(4, 'Packet data error')
    ConnectionClosed = _ErrField(5, 'Connection closed')
    ParamErr = _ErrField(6, 'Parameter error')
    NotSetRSAFile = _ErrField(7, 'Conn is encrypted, but no RSA private key file is set. Call SysConfig.set_init_rsa_file.')
    RsaErr = _ErrField(8, 'RSA key is invalid')
    WrongType = _ErrField(9, 'Wrong type')
    WrongValue = _ErrField(10, 'Wrong value')
    NoNeedUnlock = _ErrField(2000, 'No need to unlock, because REAL trade is not supported in this market')
    NoAccForSecurityFirm = _ErrField(2001, 'Something wrong with the specified securities firm ')


def _make_kwargs_str(**kwargs):
    msg = ''
    if len(kwargs) > 0:
        msg = ':'
        for k, v in kwargs.items():
            msg += ' {0}={1};'.format(k, v)
    return msg


def make_msg(err, msg_=None, **kwargs):
    msg_ = '' if msg_ is None else ': ' + msg_
    if isinstance(err, str):
        return err + msg_ + _make_kwargs_str(**kwargs)
    else:
        return err.text + msg_ + _make_kwargs_str(**kwargs)

def make_wrong_type_msg(var_name, right_type):
    return '{}. {} should be {}'.format(Err.WrongType.text, var_name, right_type)

def make_wrong_value_msg(var_name, right_value):
    return '{}. {} should be {}'.format(Err.WrongValue.text, var_name, right_value)


def make_wrong_value_msg_utf8_len_le(var_name, max_len):
    return 'Error variable. The {} parameter cannot be longer than {} bytes after being converted to utf8'.format(
        var_name,
        max_len)
