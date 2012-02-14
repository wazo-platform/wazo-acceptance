# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world

from xivo_lettuce.manager import voicemail_manager

@step(u'Given there is no voicemail "([^"]*)"')
def given_there_is_no_voicemail_1(step, voicemail_number):
    voicemail_manager.delete_voicemail_from_number(voicemail_number)
