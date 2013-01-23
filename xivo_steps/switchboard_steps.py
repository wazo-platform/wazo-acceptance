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

from lettuce import world, step
from hamcrest import assert_that, equal_to
from xivo_lettuce.xivoclient import xivoclient, xivoclient_step


@step(u'When I search a transfer destination "([^"]*)"')
@xivoclient_step
def when_i_search_a_transfer_destination_1(step, group1):
    assert_that(world.xc_response, equal_to('OK'))


@step(u'Then I see transfer destinations:')
def then_i_see_transfer_destinations(step):
    for entry in step.hashes:
        assert_directory_has_entry(entry['display_name'], entry['phone'])


@xivoclient
def assert_directory_has_entry(name, phone_number):
    assert_that(world.xc_response, equal_to('OK'))
