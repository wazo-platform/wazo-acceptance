# -*- coding: utf-8 -*-

from lettuce import step
from xivo_lettuce.common import open_url, submit_form
from xivo_lettuce.manager import meetme_manager


@step(u'When I create a conference room with name "([^"]*)" with number "([^"]*)"')
def when_i_create_a_conference_room_with_name_number(step, name, confno):
    meetme_manager.delete_meetme_by_confno(confno)
    open_url('meetme', 'add')
    meetme_manager.type_name(name)
    meetme_manager.type_context('default')
    meetme_manager.type_confno(confno)
    submit_form()


@step(u'When I create a conference room with name "([^"]*)" with number "([^"]*)" with max participants "([^"]*)"')
def when_i_create_a_conference_room_with_name_number_max_participants(step, name, confno, maxusers):
    meetme_manager.delete_meetme_by_confno(confno)
    open_url('meetme', 'add')
    meetme_manager.type_name(name)
    meetme_manager.type_context('default')
    meetme_manager.type_confno(confno)
    meetme_manager.type_maxusers(maxusers)
    submit_form()
