# -*- coding: utf-8 -*-

from lettuce import world


def delete_voicemail_with_id(voicemail_id):
    world.ws.voicemails.delete(voicemail_id)


def delete_voicemails_with_number(number):
    for voicemail in _search_voicemails_with_number(number):
        delete_voicemail_with_id(voicemail.id)


def _search_voicemails_with_number(number):
    return world.ws.voicemails.search_by_number(number)
