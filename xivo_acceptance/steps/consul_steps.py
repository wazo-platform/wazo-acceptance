# -*- coding: utf-8 -*-

# Copyright (C) 2015 Avencall
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
from consul import Consul
from hamcrest import assert_that, equal_to


def _client():
    return Consul(host=world.config['xivo_host'],
                  token=world.config['consul_token'])


@step(u'When I create a consul key "([^"]*)" with value "([^"]*)"')
def when_i_create_a_consul_key_group1_with_value_group2(step, key, value):
    _client().kv.put(key, value)


@step(u'Then the consul key "([^"]*)" equals to "([^"]*)"')
def then_the_consul_key_group1_equals_to_group2(step, key, value):
    result = _client().kv.get(key)

    assert_that(result[1]['Value'], equal_to(value))
