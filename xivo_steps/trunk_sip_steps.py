# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
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

import socket

from lettuce import step, world

from xivo_acceptance.helpers import trunksip_helper
from xivo_lettuce import form
from xivo_lettuce.common import open_url, remove_line


@step(u'Given there is no trunksip "([^"]*)"')
def given_there_is_no_trunksip(step, name):
    trunksip_helper.delete_trunksips_with_name(name)


@step(u'Given there is a trunksip "([^"]*)"')
def given_there_is_a_trunksip(step, name):
    trunksip_helper.delete_trunksips_with_name(name)
    trunksip_helper.add_trunksip('192.168.32.1', name)


@step(u'Given there is a SIP trunk "([^"]*)" in context "([^"]*)"$')
def given_there_is_a_siptrunk_with_callerid(step, name, context):
    callgen_ip = socket.gethostbyname(world.config.callgen_host),
    trunksip_helper.add_or_replace_trunksip(callgen_ip, name, context)


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
