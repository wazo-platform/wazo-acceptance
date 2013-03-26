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

from lettuce import step, world
from xivo_lettuce.xivoclient import xivoclient_step
from hamcrest import assert_that, equal_to

@step(u'Then the agent list xlet shows agent "([^"]*)" as not in use')
@xivoclient_step
def then_the_agent_list_xlet_shows_agent_as_not_in_use(step, agent_number):
    assert_that(world.xc_response, equal_to('OK'))


@step(u'Then the agent list xlet shows agent "([^"]*)" as unlogged')
@xivoclient_step
def then_the_agent_list_xlet_shows_agent_as_unlogged(step, agent_number):
    assert_that(world.xc_response, equal_to('OK'))
