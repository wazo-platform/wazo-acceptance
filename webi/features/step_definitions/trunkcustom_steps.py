# -*- coding: utf-8 -*-

from lettuce import step, world

from xivo_lettuce.common import open_url, remove_line, submit_form
from xivo_lettuce.manager_ws import trunkcustom_manager_ws


@step(u'Given there is a trunkcustom "([^"]*)"')
def given_there_is_a_trunkcustom(step, name):
    data = {'name': name,
            'interface': name}
    trunkcustom_manager_ws.add_or_replace_customtrunk(data)


@step(u'Given there is no trunkcustom "([^"]*)"')
def given_there_is_no_trunkcustom(step, name):
    trunkcustom_manager_ws.delete_customtrunk_with_name_if_exists(name)


@step(u'When I create a trunkcustom with name "([^"]*)"')
def when_i_create_a_trunkcustom_with_name_and_trunk(step, name):
    open_url('trunkcustom', 'add')
    input_name = world.browser.find_element_by_id('it-protocol-name', 'trunkcustom form not loaded')
    input_name.send_keys(name)
    input_interface = world.browser.find_element_by_id('it-protocol-interface', 'trunkcustom form not loaded')
    input_interface.send_keys('misdn//xivo')
    submit_form()


@step(u'When I remove the trunkcustom "([^"]*)"')
def when_i_remove_the_trunkcustom(step, name):
    open_url('trunkcustom', 'list')
    remove_line(name)
