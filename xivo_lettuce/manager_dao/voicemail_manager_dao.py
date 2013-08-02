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


def delete_voicemail_with_number_context(number, context):
    remote_exec(_delete_voicemail_with_number_context, number=number, context=context)


def _delete_voicemail_with_number_context(channel, number, context):
    from xivo_dao.data_handler.voicemail import services as voicemail_services

    try:
        voicemail = voicemail_services.get_by_number_context(number, context)
    except LookupError:
        return

    voicemail_services.delete(voicemail)


def delete_voicemail_with_user_id(user_id):
    remote_exec(_delete_voicemail_with_user_id, user_id=user_id)


def _delete_voicemail_with_user_id(channel, user_id):
    from xivo_dao.data_handler.voicemail import services as voicemail_services
    from xivo_dao import user_dao

    try:
        user = user_dao.get(user_id)
    except LookupError:
        return

    voicemail = voicemail_services.get(user.voicemailid)

    voicemail_services.delete(voicemail)
