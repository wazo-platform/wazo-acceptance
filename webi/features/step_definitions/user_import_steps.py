# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world

from xivo_lettuce.common import *
from xivo_lettuce.manager.user_import_manager import *


@step(u'When I import a user "([^"]*)" "([^"]*)" with a SIP line "([^"]*)"$')
def when_i_create_a_user(step, firstname, lastname, linenumber):
    insert_simple_user(firstname, lastname, linenumber)
