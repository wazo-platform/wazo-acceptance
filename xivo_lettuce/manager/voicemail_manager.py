# -*- coding: utf-8 -*-

from lettuce.registry import world
from webservices.webservices import WebServicesFactory

VOICEMAIL_URL = '/service/ipbx/index.php/pbx_settings/voicemail/%s'
WS_VOICEMAIL = WebServicesFactory('ipbx/pbx_settings/voicemail')


def delete_voicemail_from_number(voicemail_number):
    for id in find_voicemail_id_from_number(voicemail_number):
        WS_VOICEMAIL.delete(id)


def find_voicemail_id_from_number(voicemail_number):
    voicemail_list = WS_VOICEMAIL.list()
    if voicemail_list:
        return [voicemailinfo['uniqueid'] for voicemailinfo in voicemail_list if
                voicemailinfo['mailbox'] == voicemail_number]
    return []
