# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world

from xivo_lettuce.common import *
from xivo_lettuce.manager import voicemail_manager as mevo

@step(u'Given there is no voicemail "([^"]*)"')
def given_there_is_no_voicemail_1(step, voicemail_number):
    mevo.delete_voicemail_from_number(voicemail_number)

