# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world

from xivo_lettuce.common import *
from xivo_lettuce.manager import meetme_manager
from xivo_lettuce.manager import context_manager


@step(u'When I create a conference room with name "([^"]*)" with number "([^"]*)"')
def when_i_create_a_conference_room_with_name_number(step, name, confno):
    context_manager.check_context_number_in_interval('default', 'meetme', confno)
    meetme_manager.delete_all_meetme()
    open_url('meetme', 'add')
    meetme_manager.type_name(name)
    meetme_manager.type_context('default')
    meetme_manager.type_confno(confno)
    submit_form()


@step(u'When I create a conference room with name "([^"]*)" with number "([^"]*)" with max participants "([^"]*)"')
def when_i_create_a_conference_room_with_name_number_max_participants(step, name, confno, maxusers):
    context_manager.check_context_number_in_interval('default', 'meetme', confno)
    meetme_manager.delete_all_meetme()
    open_url('meetme', 'add')
    meetme_manager.type_name(name)
    meetme_manager.type_context('default')
    meetme_manager.type_confno(confno)
    meetme_manager.type_maxusers(maxusers)
    submit_form()
