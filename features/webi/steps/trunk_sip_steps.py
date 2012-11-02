# -*- coding: utf-8 -*-

from lettuce import step, world
from xivo_lettuce import form
from xivo_lettuce.common import open_url, remove_line
from xivo_lettuce.manager_ws import trunksip_manager_ws


@step(u'Given there is no trunksip "([^"]*)"')
def given_there_is_no_trunksip(step, name):
    trunksip_manager_ws.delete_trunksips_with_name(name)


@step(u'Given there is a trunksip "([^"]*)"')
def given_there_is_a_trunksip(step, name):
    trunksip_manager_ws.delete_trunksips_with_name(name)
    trunksip_manager_ws.add_trunksip('192.168.32.1', name)


@step(u'When I create a trunksip with name "([^"]*)"')
def when_i_create_a_trunksip_with_name_and_trunk(step, name):
    open_url('trunksip', 'add')
    input_name = world.browser.find_element_by_id('it-protocol-name', 'trunksip form not loaded')
    input_name.send_keys(name)
    form.submit.submit_form()


@step(u'When I remove the trunksip "([^"]*)"')
def when_i_remove_the_trunksip(step, name):
    open_url('trunksip', 'list')
    remove_line(name)
