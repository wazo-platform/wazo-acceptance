# -*- coding: utf-8 -*-

# Copyright (C) 2013-2016 Avencall
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

from hamcrest import assert_that, is_not, none

from lettuce import step, world
from xivo_acceptance.action.confd import line_extension_action_confd as line_extension_action
from xivo_acceptance.helpers import extension_helper
from xivo_acceptance.helpers import line_sip_helper


@step(u'Given SIP line "([^"]*)" is associated to extension "(\d+)@([\w_-]+)"')
def given_line_with_username_group1_is_associated_to_extension_group2(step, username, exten, context):
    line = line_sip_helper.find_by_username(username)
    assert_that(line, is_not(none()), "Line with username {} not found".format(username))
    extension = extension_helper.find_extension_by_exten_context(exten, context)
    assert_that(extension, is_not(none()), "Extension {}@{} not found".format(exten, context))
    world.response = line_extension_action.associate(line['id'], extension['id'])
