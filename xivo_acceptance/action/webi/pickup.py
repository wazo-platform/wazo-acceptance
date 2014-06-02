# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from lettuce import world
from selenium.webdriver.support.select import Select
from xivo_lettuce import common
from xivo_lettuce.form import submit


def type_pickup_entity(name):
    input_name = Select(world.browser.find_element_by_id('it-pickup-entity_id', 'Pickup form not loaded'))
    input_name.select_by_visible_text(name)


def type_pickup_name(name):
    input_name = world.browser.find_element_by_id('it-pickup-name', 'Pickup form not loaded')
    input_name.send_keys(name)


def add_pickup(**data):
    common.open_url('pickup', 'add')
    if 'entity' in data and data['entity']:
        type_pickup_entity(data['entity'])
    type_pickup_name(data['name'])
    submit.submit_form()
