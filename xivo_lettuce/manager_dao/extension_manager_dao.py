# -*- coding: utf-8 -*-
#
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

from xivo_lettuce.remote_py_cmd import remote_exec
from xivo_dao.data_handler.extension import services as extension_services
from xivo_dao.data_handler.exception import ElementNotExistsError


def find_extension_by_exten(exten):
    return extension_services.find_by_exten(exten)


def get_by_exten_context(exten, context):
    try:
        extension = extension_services.get_by_exten_context(exten, context)
    except ElementNotExistsError:
        return None
    return extension


def delete_extension_with_exten_context(exten, context):
    remote_exec(_delete_extension_with_exten_context, exten=exten, context=context)


def _delete_extension_with_exten_context(channel, exten, context):
    from xivo_dao.data_handler.extension import services as extension_services

    try:
        extension = extension_services.get_by_exten_context(exten, context)
    except LookupError:
        return

    extension_services.delete(extension)
