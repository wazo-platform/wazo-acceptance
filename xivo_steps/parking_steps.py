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

from lettuce import step

from xivo_lettuce.manager import parking_manager


@step(u'When I change the parking configuration to be:')
def when_i_change_the_parking_configuration_to_be(step):
    parking_configuration = step.hashes[0]
    parking_manager.set_parking_config(parking_configuration)


@step(u'Then I should have to following lines in "([^"]*)":')
def then_i_should_have_to_following_lines_in_group1(step, group1):
    expected_parking_info = step.hashes[0]
    parking_manager.check_parking_info(expected_parking_info)
