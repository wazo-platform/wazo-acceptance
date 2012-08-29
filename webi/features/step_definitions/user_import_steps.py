# -*- coding: utf-8 -*-

from lettuce import step

from xivo_lettuce.manager_ws import user_import_manager_ws


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
