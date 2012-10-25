# -*- coding: utf-8 -*-

from lettuce import step
from utils.func import extract_number_and_context_from_extension
from xivo_lettuce.manager_ws import user_import_manager_ws
from xivo_lettuce.manager_ws.line_manager_ws import is_line_with_number_exists
from xivo_lettuce.manager_ws.user_manager_ws import is_user_with_name_exists


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
    assert is_user_with_name_exists(firstname, lastname)


@step(u'Then line with number "([^"]*)" exists')
def then_line_with_number_exists(step, extension):
    number, context = extract_number_and_context_from_extension(extension)
    assert is_line_with_number_exists(number, context)
