# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world

from xivo_lettuce.common import *
from xivo_lettuce.manager.user_import_manager import *


@step(u'When I import a user "([^"]*)" "([^"]*)" with a SIP line "([^"]*)"$')
def when_i_import_a_user_with_sip_line(step, firstname, lastname, linenumber):
    insert_simple_user(firstname, lastname, linenumber)

@step(u'When I import a user "([^"]*)" "([^"]*)" with a SIP line "([^"]*)" and voicemail$')
def when_i_import_a_user_with_sip_line_and_voicemail(step, firstname, lastname, linenumber):
    insert_adv_user_with_mevo(firstname, lastname, linenumber)

@step(u'When I import a user "([^"]*)" "([^"]*)" with a SIP line "([^"]*)" and incall "([^"]*)"$')
def when_i_import_a_user_with_sip_line_and_incall(step, firstname, lastname, linenumber, incalexten):
    insert_adv_user_with_incall(firstname, lastname, linenumber, incalexten)

@step(u'When I import a user "([^"]*)" "([^"]*)" with a SIP line "([^"]*)" and incall "([^"]*)" and voicemail - full$')
def when_i_import_a_user_with_sip_line_and_incall_and_voicemail_full(step, firstname, lastname, linenumber, incalexten):
    insert_adv_user_full_infos(firstname, lastname, linenumber, incalexten)
