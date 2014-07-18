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


from lettuce.decorators import step

from xivo_lettuce import common
from xivo_acceptance.helpers import entity_helper


@step(u'Given there is no entity "([^"]*)"$')
def given_there_is_no_element(step, search):
    common.remove_element_if_exist('entity', search)


@step(u'^Given there are entities with infos:$')
def given_there_are_elements_with_infos(step):
    for data in step.hashes:
        entity_helper.add_entity(data['name'], data['display_name'])
