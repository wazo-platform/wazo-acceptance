# -*- coding: utf-8 -*-
# Copyright (C) 2013-2016 Avencall
# SPDX-License-Identifier: GPL-3.0+

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
