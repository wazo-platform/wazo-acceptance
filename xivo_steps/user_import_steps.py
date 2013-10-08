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
from xivo_lettuce.manager_ws import user_import_manager_ws
from xivo_lettuce import func
from xivo_acceptance.helpers import line_helper, user_helper


@step(u'^When I import a list of users with voicemail:$')
def when_i_import_a_user_with_sip_line_and_voicemail(step):
    user_import_manager_ws.insert_adv_user_with_mevo(step.hashes)


@step(u'^When I import a list of users with incall:$')
def when_i_import_a_user_with_sip_line_and_incall(step):
    user_import_manager_ws.insert_adv_user_with_incall(step.hashes)


@step(u'^When I import a list of users with incall and voicemail - full:$')
def when_i_import_a_user_with_sip_line_and_incall_and_voicemail_full(step):
    user_import_manager_ws.insert_adv_user_full_infos(step.hashes)


@step(u'^When I import a list of users:$')
def when_i_import_a_list_of_users(step):
    user_import_manager_ws.insert_simple_user(step.hashes)


@step(u'Then user with name "([^"]*)" exists')
def then_user_with_name_exists(step, name):
    firstname, lastname = name.split(' ', 1)
    assert user_helper.is_user_with_name_exists(firstname, lastname)


@step(u'Then line with number "([^"]*)" exists')
def then_line_with_number_exists(step, extension):
    number, context = func.extract_number_and_context_from_extension(extension)
    assert line_helper.is_with_exten_context_exists(number, context)
