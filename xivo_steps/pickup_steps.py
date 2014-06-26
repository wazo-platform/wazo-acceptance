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

from lettuce import step, world

from xivo_acceptance.action.webi import pickup as pickup_action_webi
from xivo_lettuce import common

_PICKUP_PREFIX = '*8'


@step(u'Given there is no pickup "([^"]*)"$')
def given_there_is_no_pickup(step, search):
    common.remove_element_if_exist('pickup', search)


@step(u'Given there are pickups:$')
def given_there_are_pickup(step):
    for data in step.hashes:
        pickup_action_webi.add_pickup(**data)


@step(u'Then the directed pickup is successful')
def the_directed_pickup_is_successful(step):
    assert world.pickup_success
