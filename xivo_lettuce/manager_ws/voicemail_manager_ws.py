# -*- coding: utf-8 -*-

from lettuce.registry import world


def delete_voicemail_with_id(voicemail_id):
    world.ws.voicemails.delete(voicemail_id)


def delete_voicemail_with_number(voicemail_number):
    for id in find_voicemail_id_with_number(voicemail_number):
        delete_voicemail_with_id(id)


def find_voicemail_id_with_number(voicemail_number):
    voicemail_list = world.ws.voicemails.search(voicemail_number)
    if voicemail_list:
        return [voicemail.id for voicemail in voicemail_list if
                voicemail.mailbox == str(voicemail_number)]
    return []
