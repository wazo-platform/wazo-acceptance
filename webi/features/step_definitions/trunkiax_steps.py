# -*- coding: utf-8 -*-

from lettuce import step, world

from xivo_lettuce import form
from xivo_lettuce.common import open_url, remove_line
from xivo_lettuce.manager_ws import trunkiax_manager_ws


@step(u'Given there is a trunkiax "([^"]*)"')
def given_there_is_a_trunkiax(step, name):
    data = {'name': name,
            'context': 'default'}
    trunkiax_manager_ws.add_or_replace_iaxtrunk(data)


@step(u'Given there is no trunkiax "([^"]*)"')
def given_there_is_no_trunkiax(step, name):
    trunkiax_manager_ws.delete_iaxtrunk_with_name_if_exists(name)


@step(u'When I create a trunkiax with name "([^"]*)"')
def when_i_create_a_trunkiax_with_name_and_trunk(step, name):
    open_url('trunkiax', 'add')
    input_name = world.browser.find_element_by_id('it-protocol-name', 'trunkiax form not loaded')
    input_name.send_keys(name)
    form.submit_form()


@step(u'When I remove the trunkiax "([^"]*)"')
def when_i_remove_the_trunkiax(step, name):
    open_url('trunkiax', 'list')
    remove_line(name)
