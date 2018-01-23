# -*- coding: utf-8 -*-

# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
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

from xivo_acceptance.helpers import trunkiax_helper
from xivo_acceptance.lettuce import common, form


@step(u'Given there is a trunkiax "([^"]*)"')
def given_there_is_a_trunkiax(step, name):
    trunkiax_helper.add_or_replace_trunkiax(name)


@step(u'Given there is no trunkiax "([^"]*)"')
def given_there_is_no_trunkiax(step, name):
    trunkiax_helper.delete_trunkiaxs_with_name(name)


@step(u'When I create a trunkiax with name "([^"]*)"')
def when_i_create_a_trunkiax_with_name_and_trunk(step, name):
    common.open_url('trunkiax', 'add')
    input_name = world.browser.find_element_by_id('it-protocol-name', 'trunkiax form not loaded')
    input_name.send_keys(name)
    form.submit.submit_form()


@step(u'When I remove the trunkiax "([^"]*)"')
def when_i_remove_the_trunkiax(step, name):
    common.open_url('trunkiax', 'list')
    common.remove_line(name)
