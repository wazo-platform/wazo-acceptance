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

from xivo_lettuce.restapi.v1_1 import device_helper
from xivo_lettuce.manager_restapi import device_ws

from hamcrest import assert_that, has_entries
from lettuce import step, world


@step(u'Given I have no devices')
def given_there_are_no_devices(step):
    device_helper.delete_all()


@step(u'Given I only have the following devices:')
def given_there_are_the_following_devices(step):
    device_helper.delete_all()
    for deviceinfo in step.hashes:
        device_helper.create_device(deviceinfo)


@step(u'When I create an empty device')
def when_i_create_an_empty_device(step):
    world.response = device_ws.create_device({})


@step(u'When I create the following devices:')
def when_i_create_the_following_devices(step):
    for device_info in step.hashes:
        world.response = device_ws.create_device(device_info)


@step(u'Then the created device has the following parameters:')
def then_the_created_device_has_the_following_parameters(step):
    device_response = world.response.data
    expected_device = step.hashes[0]

    assert_that(device_response, has_entries(expected_device))
