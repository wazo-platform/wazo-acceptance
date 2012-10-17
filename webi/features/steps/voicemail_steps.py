# -*- coding: utf-8 -*-

from lettuce import step

from xivo_lettuce.manager_ws import voicemail_manager_ws


@step(u'Given there is no voicemail "([^"]*)"')
def given_there_is_no_voicemail_1(step, voicemail_number):
    voicemail_manager_ws.delete_voicemail_with_number(voicemail_number)
