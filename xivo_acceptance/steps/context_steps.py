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

from xivo_acceptance.helpers import context_helper
from xivo_acceptance.lettuce import common
from xivo_acceptance.lettuce.common import open_url


@step(u'^Given there are contexts with infos:$')
def given_there_are_contexts_with_infos(step):
    for context_data in step.hashes:
        entity_name = context_data.get('entity_name', world.config['default_entity'])
        if context_data['type'] == 'user':
            context_helper.update_contextnumbers_user(context_data['name'],
                                                      context_data['range_start'],
                                                      context_data['range_end'],
                                                      entity_name=entity_name)
        elif context_data['type'] == 'group':
            context_helper.update_contextnumbers_group(context_data['name'],
                                                       context_data['range_start'],
                                                       context_data['range_end'],
                                                       entity_name=entity_name)
        elif context_data['type'] == 'meetme':
            context_helper.update_contextnumbers_meetme(context_data['name'],
                                                        context_data['range_start'],
                                                        context_data['range_end'])
        elif context_data['type'] == 'incall':
            context_helper.update_contextnumbers_incall(context_data['name'],
                                                        context_data['range_start'],
                                                        context_data['range_end'],
                                                        entity_name=entity_name,
                                                        didlength=context_data['didlength'])
        elif context_data['type'] == 'queue':
            context_helper.update_contextnumbers_queue(context_data['name'],
                                                       context_data['range_start'],
                                                       context_data['range_end'],
                                                       entity_name=entity_name)


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
