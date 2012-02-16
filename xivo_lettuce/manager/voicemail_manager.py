# -*- coding: utf-8 -*-

from lettuce.registry import world
from xivo_lettuce.common import *

WS_VOICEMAIL = get_webservices('voicemail')


def delete_voicemail_from_number(voicemail_number):
    for id in find_voicemail_id_from_number(voicemail_number):
        WS_VOICEMAIL.delete(id)


def find_voicemail_id_from_number(voicemail_number):
    voicemail_list = WS_VOICEMAIL.list()
    if voicemail_list:
        return [voicemailinfo['uniqueid'] for voicemailinfo in voicemail_list if
                voicemailinfo['mailbox'] == str(voicemail_number)]
    return []
