# -*- coding: UTF-8 -*-

def Msg(msg_id, *fields):
    fields_by_name = dict((field.name, field) for field in fields)
    if len(fields) != len(fields_by_name):
        raise Exception('same field name used twice')

    class_dict = {
        'MSG_ID': msg_id,
        '_FIELDS': fields,
    }
    class_dict.update(fields_by_name)

    return type('Msg0x%04X' % msg_id, (_BaseMsg,), class_dict)


class _BaseMsg(object):

    def __init__(self):
        for field in self._FIELDS:
            field.zero(self)

    def serialize(self):
        # TODO
        pass

    def deserialize(self, buf):
        # TODO
        pass


class Uint32(object):

    _MINVAL = 0
    _MAXVAL = 2 ** 32 - 1

    def __init__(self, name):
        self.name = name
        self._obj_name = '_fieldval_%s' % name

    def zero(self, obj):
        setattr(obj, self._obj_name, 0)

    def __get__(self, obj, objtype):
        return getattr(obj, self._obj_name)

    def __set__(self, obj, value):
        if not isinstance(value, int):
            raise ValueError('expected integer type; got %s type' % type(value).__name__)
        if not self._MINVAL <= value <= self._MAXVAL:
            raise ValueError('value %s is out of range' % value)
        setattr(obj, self._obj_name, value)


class Uint8(object):

    _MINVAL = 0
    _MAXVAL = 2 ** 8 - 1

    def __init__(self, name):
        self.name = name
        self._obj_name = '_fieldval_%s' % name

    def zero(self, obj):
        setattr(obj, self._obj_name, 0)

    def __get__(self, obj, objtype):
        return getattr(obj, self._obj_name)

    def __set__(self, obj, value):
        if not isinstance(value, int):
            raise ValueError('expected integer type; got %s type' % type(value).__name__)
        if not self._MINVAL <= value <= self._MAXVAL:
            raise ValueError('value %s is out of range' % value)
        setattr(obj, self._obj_name, value)


class Bytes(object):

    def __init__(self, name, length):
        self.name = name
        self._length = length
        self._obj_name = '_fieldval_%s' % name

    def zero(self, obj):
        setattr(obj, self._obj_name, '')

    def __get__(self, obj, objtype):
        return getattr(obj, self._obj_name)

    def __set__(self, obj, value):
        # not using basestring since we really want byte string and no unicode string
        if not isinstance(value, str):
            raise ValueError('expected str type; got %s type' % type(value).__name__)
        if len(value) > self._length:
            raise ValueError('value %s is too long' % value)
        setattr(obj, self._obj_name, value)


REGISTER_MSG_ID = 0x0001


RegisterMsg = Msg(REGISTER_MSG_ID,
    Bytes('name', 16),
    Uint32('user_id'),
    Uint32('line_instance'),
    Uint32('ip'),
    Uint32('type'),
    Uint32('max_streams'),
    Uint32('active_streams'),
    Uint8('proto_version'),
)
