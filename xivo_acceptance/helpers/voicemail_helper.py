# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
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

from xivo_lettuce.remote_py_cmd import remote_exec, remote_exec_with_result


def delete_voicemail_with_id(voicemail_id):
    remote_exec(_delete_voicemail_with_id, voicemail_id=voicemail_id)


def _delete_voicemail_with_id(channel, voicemail_id):
    from xivo_dao.data_handler.voicemail import services
    from xivo_dao.data_handler.exception import ElementNotExistsError

    try:
        voicemail = services.get(voicemail_id)
        services.delete(voicemail)
    except ElementNotExistsError:
        pass


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


def add_or_replace_voicemail(parameters):
    _delete_voicemail(parameters)
    create_voicemail(parameters)


def _delete_voicemail(parameters):
    if 'number' in parameters:
        number = parameters['number']
        context = parameters.get('context', 'default')
        delete_voicemail_with_number_context(number, context)


def create_voicemail(parameters):
    remote_exec(_create_voicemail, parameters=parameters)


def _create_voicemail(channel, parameters):
    from xivo_dao.alchemy.voicemail import Voicemail as VoicemailSchema
    from xivo_dao.helpers.db_manager import AsteriskSession

    voicemail = VoicemailSchema()

    voicemail.fullname = parameters['name']
    voicemail.mailbox = parameters['number']
    voicemail.context = parameters['context']

    if 'password' in parameters:
        voicemail.password = parameters['password']

    if 'email' in parameters:
        voicemail.email = parameters['email']

    if 'language' in parameters:
        voicemail.language = parameters['language']

    if 'timezone' in parameters:
        voicemail.tz = parameters['timezone']

    if 'max_messages' in parameters:
        voicemail.maxmsg = int(parameters['max_messages'])

    if 'attach_audio' in parameters:
        voicemail.attach = int(parameters['attach_audio'])

    if 'delete_messages' in parameters:
        voicemail.deletevoicemail = int(parameters['delete_messages'])

    if 'ask_password' in parameters:
        voicemail.skipcheckpass = int(parameters['ask_password'])

    AsteriskSession.begin()
    AsteriskSession.add(voicemail)
    AsteriskSession.commit()


def total_voicemails():
    return remote_exec_with_result(_total_voicemails)


def _total_voicemails(channel):
    from xivo_dao.alchemy.voicemail import Voicemail as VoicemailSchema
    from xivo_dao.helpers.db_manager import AsteriskSession

    count = AsteriskSession.query(VoicemailSchema).count()
    channel.send(count)


def find_voicemail_id_with_number(number, context='default'):
    return remote_exec_with_result(_find_voicemail_id_with_number, number=number, context=context)


def _find_voicemail_id_with_number(channel, number, context):
    from xivo_dao.data_handler.voicemail import services
    from xivo_dao.data_handler.exception import ElementNotExistsError

    try:
        voicemail = services.get_by_number_context(number, context)
        channel.send(voicemail.id)
    except ElementNotExistsError:
        channel.send(None)
