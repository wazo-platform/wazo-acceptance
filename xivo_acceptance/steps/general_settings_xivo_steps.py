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

from hamcrest import assert_that, contains_string, has_item, is_not
from lettuce import step

from xivo_acceptance.action.webi import general_settings_xivo as general_settings_xivo_action_webi
from xivo_acceptance.lettuce import logs


@step(u'Then i see live reload request in sysconfd log file')
def then_i_see_messages_in_sysconfd_log_file(step):
    expression = "'POST /exec_request_handlers HTTP/1.1' 200"
    log_lines = logs.find_line_in_xivo_sysconfd_log()
    assert_that(log_lines, has_item(contains_string(expression)))


@step(u'Then i see no live reload request in sysconfd log file')
def then_i_see_no_messages_in_sysconfd_log_file(step):
    expression = "'POST /exec_request_handlers HTTP/1.1' 200"
    log_lines = logs.find_line_in_xivo_sysconfd_log()
    assert_that(log_lines, is_not(has_item(contains_string(expression))))
    general_settings_xivo_action_webi.enable_live_reload()
