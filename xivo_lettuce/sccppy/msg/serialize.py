# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import collections
import struct

_HEADER_FORMAT = struct.Struct('<III')
_HEADER_SIZE = _HEADER_FORMAT.size


class MsgSerializer(object):

    def serialize_msg(self, msg):
        body = msg.serialize()
        header = _HEADER_FORMAT.pack(len(body) + 4, 0, msg.id)
        return header + body


class MsgDeserializer(object):

    _MAX_BODY_SIZE = 2000

    def __init__(self, msg_registry):
        self.msgs_queue = collections.deque()
        self._msg_registry = msg_registry
        self._buf = ''

    def deserialize_msg(self, string):
        self._buf += string
        while self._deserialize_next_msg():
            pass

    def _deserialize_next_msg(self):
        if len(self._buf) < _HEADER_SIZE:
            return False

        length, _, msg_id = _HEADER_FORMAT.unpack(self._buf[:_HEADER_SIZE])
        body_size = length - 4
        if body_size < 0 or body_size > self._MAX_BODY_SIZE:
            # XXX should raise another kind of exception
            raise Exception('invalid msg body size: %d' % body_size)

        total_size = _HEADER_SIZE + body_size
        if len(self._buf) < total_size:
            return False

        body = self._buf[_HEADER_SIZE:total_size]
        self._buf = self._buf[total_size:]

        msg = self._msg_registry.new_msg_from_id(msg_id)
        msg.deserialize(body)
        self.msgs_queue.append(msg)

        return True
