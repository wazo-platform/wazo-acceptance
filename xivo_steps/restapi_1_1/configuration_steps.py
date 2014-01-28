# -*- coding: utf-8 -*-
#
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
from lettuce.decorators import step
from xivo_acceptance.action.restapi import configuration_action_restapi
from lettuce.registry import world
from hamcrest.library.collection.isdict_containing import has_entry
from hamcrest.core import assert_that


@step(u'When I ask for the live reload state')
def when_i_ask_for_the_live_reload_state(step):
    world.response = configuration_action_restapi.get_live_reload_state()


@step(u'Then I get a response with live reload enabled')
def then_i_get_a_response_with_live_reload_enabled(step):
    content = world.response.data
    assert_that(content, has_entry('enabled', True))
