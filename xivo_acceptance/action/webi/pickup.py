# -*- coding: utf-8 -*-
# Copyright (C) 2013-2016 Avencall
# SPDX-License-Identifier: GPL-3.0+

from lettuce import world
from xivo_acceptance.lettuce.form.list_pane import ListPane
from selenium.webdriver.support.select import Select
from xivo_acceptance.lettuce import common
from xivo_acceptance.lettuce.form import submit


def type_pickup_entity(name):
    input_name = Select(world.browser.find_element_by_id('it-pickup-entity_id', 'Pickup form not loaded'))
    input_name.select_by_visible_text(name)


def type_pickup_name(name):
    input_name = world.browser.find_element_by_id('it-pickup-name', 'Pickup form not loaded')
    input_name.send_keys(name)


def add_pickup(data):
    common.open_url('pickup', 'add')

    if 'entity' in data and data['entity']:
        type_pickup_entity(data['entity'])
    type_pickup_name(data['name'])

    common.go_to_tab('Interceptors')
    _select('interceptoruser', data.get('intercepting users'))
    _select('interceptorgroup', data.get('intercepting groups'))
    _select('interceptorqueue', data.get('intercepting queues'))

    common.go_to_tab('Intercepted')
    _select('intercepteduser', data.get('intercepted users'))
    _select('interceptedgroup', data.get('intercepted groups'))
    _select('interceptedqueue', data.get('intercepted queues'))

    submit.submit_form()


def _select(category, items):
    if not items:
        return

    listname = '{}list'.format(category)
    list_pane = ListPane.from_id(listname)
    for item in items.split(', '):
        list_pane.add_contains(item)
