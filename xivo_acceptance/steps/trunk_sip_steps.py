# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
# Copyright (C) 2016 Proformatique Inc.
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

from lettuce import step, world

from xivo_acceptance.helpers import trunksip_helper
from xivo_acceptance.lettuce import common, form


@step(u'Given there is no trunksip "([^"]*)"')
def given_there_is_no_trunksip(step, name):
    trunksip_helper.delete_trunksips_with_name(name)


@step(u'Given there is a trunksip "([^"]*)"')
def given_there_is_a_trunksip(step, name):
    trunksip_helper.add_or_replace_trunksip('192.168.32.1', name)


@step(u'When I create a trunksip with name "([^"]*)"')
def when_i_create_a_trunksip_with_name_and_trunk(step, name):
    endpoint_sip = world.confd_client.endpoints_sip.create({'username': name})
    trunk = world.confd_client.trunks.create({})
    world.confd_client.trunks(trunk).add_endpoint_sip(endpoint_sip)


@step(u'When I remove the trunksip "([^"]*)"')
def when_i_remove_the_trunksip(step, name):
    trunksip_helper.delete_trunksips_with_name(name)


@step(u'When I create a trunksip with name "([^"]*)" in the webi')
def when_i_create_a_trunksip_with_name_and_trunk_in_the_webi(step, name):
    common.open_url('trunksip', 'add')
    input_name = world.browser.find_element_by_id('it-protocol-name', 'trunksip form not loaded')
    input_name.send_keys(name)
    form.submit.submit_form()


@step(u'When I remove the trunksip "([^"]*)" in the webi')
def when_i_remove_the_trunksip_in_the_webi(step, name):
    common.open_url('trunksip', 'list')
    common.remove_line(name)
