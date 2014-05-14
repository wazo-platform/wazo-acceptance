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
from xivo_acceptance.helpers import context_helper
from xivo_lettuce.common import open_url


@step(u'Given there is no context "([^"]*)"$')
def given_there_is_no_element(step, search):
    common.remove_element_if_exist('entity', search)


@step(u'^Given there are contexts with infos:$')
def given_there_are_contexts_with_infos(step):
    for context_data in step.hashes:
        context_helper.update_contextnumbers_user(context_data['name'],
                                                  context_data['range_start'],
                                                  context_data['range_end'],
                                                  entity_name=context_data['entity_name'])


@step(u'Then I see the context "([^"]*)" exists$')
def then_i_see_the_context_exists(step, name):
    open_url('context')
    line = common.find_line(name)
    assert line is not None, 'Context: %s does not exist' % name


@step(u'Then I see the context "([^"]*)" not exists$')
def then_i_see_the_context_not_exists(step, name):
    open_url('context')
    line = common.find_line(name)
    assert line is None, 'Context: %s exist' % name
