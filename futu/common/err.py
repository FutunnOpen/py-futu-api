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

    NoNeedUnlock = _ErrField(2000, 'No need to unlock, because REAL trade is not supported in this market')


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