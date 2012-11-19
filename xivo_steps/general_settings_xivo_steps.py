# -*- coding: utf-8 -*-

from lettuce import step
from xivo_lettuce import form
from xivo_lettuce.common import open_url
from xivo_lettuce.manager import general_settings_xivo_manager
from xivo_lettuce.logs import search_str_in_daemon_log


@step(u'Given a live reload configuration is enable')
def given_a_live_reload_configuration_is_enable(step):
    general_settings_xivo_manager.enable_live_reload()


@step(u'When i edit extenfeatures page')
def when_i_edit_extenfeatures_page(step):
    open_url('extenfeatures')
    form.submit.submit_form()


@step(u'When i disable live reload configuration')
def when_i_enable_live_reload_configuration(step):
    general_settings_xivo_manager.disable_live_reload()


@step(u'Then i see live reload request in daemon log file')
def then_i_see_messages_in_daemon_log_file(step):
    expression = "'POST /exec_request_handlers HTTP/1.1' 200"
    assert search_str_in_daemon_log(expression)


@step(u'Then i see no live reload request in daemon log file')
def then_i_see_no_messages_in_daemon_log_file(step):
    expression = "'POST /exec_request_handlers HTTP/1.1' 200"
    assert not search_str_in_daemon_log(expression)
    general_settings_xivo_manager.enable_live_reload()
