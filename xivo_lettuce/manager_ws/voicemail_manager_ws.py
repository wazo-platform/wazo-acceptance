# -*- coding: utf-8 -*-

from lettuce import world


def delete_voicemail_with_id(voicemail_id):
    world.ws.voicemails.delete(voicemail_id)


def delete_all_voicemails_with_number(voicemail_number):
    for voicemail in _search_voicemails_with_number(voicemail_number):
        delete_voicemail_with_id(voicemail.id)


def _search_voicemails_with_number(number):
    number = str(number)

    voicemails = world.ws.voicemails.search(number)
    return [voicemail for voicemail in voicemails if voicemail.mailbox == number]
