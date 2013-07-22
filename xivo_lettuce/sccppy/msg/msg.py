# -*- coding: utf-8 -*-

# Copyright (C) 2013  Avencall
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

from xivo_lettuce.sccppy.msg.base import Msg, Bytes, Uint32, Uint8


KeepAliveMsg = Msg(0x0000)

RegisterMsg = Msg(0x0001,
    Bytes('name', 16),
    Uint32('user_id'),
    Uint32('line_instance'),
    Uint32('ip'),
    Uint32('type'),
    Uint32('max_streams'),
    Uint32('active_streams'),
    Uint8('proto_version'),
)

RegisterAckMsg = Msg(0x0081,
    Uint32('keepalive'),
    Bytes('date_template', 6),
    Bytes('res', 2),
    Uint32('secondary_keep_alive'),
    Uint8('proto_version'),
    Uint8('unknown1'),
    Uint8('unknown2'),
    Uint8('unknown3'),
)

KeepAliveAckMsg = Msg(0x0100)
