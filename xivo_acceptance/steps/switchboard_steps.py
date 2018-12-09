# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from hamcrest import assert_that
from hamcrest import contains
from hamcrest import equal_to
from lettuce import step, world

from xivo_acceptance.action.webi import directory as directory_action_webi
from xivo_acceptance.action.webi import user as user_action_webi
from xivo_acceptance.action.webi import phonebook as phonebook_action_webi
from xivo_acceptance.helpers import (
    context_helper,
    cti_helper,
    incall_helper,
    directory_helper,
    queue_helper,
)
from xivo_acceptance.lettuce import func, common


@step(u'Given the switchboard is configured for internal directory lookup')
def given_the_switchboard_is_configured_for_internal_directory_lookup(step):
    context_helper.add_or_replace_context('__switchboard_directory', 'Switchboard', 'others')
    phonebook_action_webi.remove_directory_if_exists('acceptance-switchboard-phonebook')
    phonebook_action_webi.create_local_dird_directory('acceptance-switchboard-phonebook',
                                                      'wazo',
                                                      world.config['default_entity'])
    directory_action_webi.add_or_replace_directory(
        'xivodirswitchboard',
        'acceptance-switchboard-phonebook',
        'firstname,lastname,displayname,society,number_office',
        '',
        {'name': '{displayname}',
         'number': '{number_office}',
         'mobile': '{number_mobile}'}
    )
    directory_action_webi.add_or_replace_display(
        'switchboard',
        [('Icon', 'status', ''),
         ('Name', 'name', 'name'),
         ('Number', 'number_office', 'number'),
         ('Number', 'number_mobile', 'mobile')]
    )
    directory_action_webi.assign_filter_and_directories_to_context(
        '__switchboard_directory',
        'switchboard',
        ['xivodirswitchboard']
    )
    directory_helper.restart_dird()


@step(u'Given the user "([^"]*)" is configured for switchboard use')
def given_the_user_group1_is_configured_for_switchboard_use(step, user):
    user_action_webi.switchboard_config_for_user(user)


@step(u'Given there is a switchboard configured as:')
def given_there_is_a_switchboard_configured_as(step):
    for config in step.hashes:
        incall_queue = {
            'name': config['incalls queue name'],
            'number': config['incalls queue number'],
            'context': config['incalls queue context'],
            'agents': config['agents'],
        }
        queue_helper.add_or_replace_queue(incall_queue)

        hold_queue = {
            'name': config['hold calls queue name'],
            'number': config['hold calls queue number'],
            'context': config['hold calls queue context'],
        }
        queue_helper.add_or_replace_queue(hold_queue)

        incall_helper.add_or_replace_incall(exten=config['incalls queue number'],
                                            context='from-extern',
                                            dst_type='queue',
                                            dst_name=config['incalls queue name'])


@step(u'When I search a transfer destination "([^"]*)"')
def when_i_search_a_transfer_destination_1(step, search):
    cti_helper.set_search_for_directory(search)


@step(u'When the switchboard "([^"]*)" selects the incoming call from "([^"]*)" number "([^"]*)"')
def when_the_switchboard_1_selects_the_incoming_call_from_2_number_3(step, switchboard, cid_name, cid_num):
    def _switchboard_has_incoming_call(cid_name, cid_num):
        incomings = cti_helper.get_switchboard_incoming_calls_infos()['incoming_calls']
        return [incoming for incoming in incomings
                if incoming['cid_name'] == cid_name
                and incoming['cid_num'] == cid_num]

    common.wait_until(_switchboard_has_incoming_call, cid_name, cid_num, tries=10)
    cti_helper.switchboard_answer_incoming_call(cid_name, cid_num)


@step(u'When the switchboard "([^"]*)" hangs up')
def when_the_switchboard_group1_hangs_up(step, switchboard):
    cti_helper.switchboard_hang_up()


@step(u'Then the switchboard "([^"]*)" is not talking to anyone')
def then_the_switchboard_1_is_not_talking_to_anyone(step, switchboard):
    def assert_switchboard_is_empty():
        current_call = cti_helper.get_switchboard_current_call_infos()
        assert_that(current_call['caller_id'], equal_to(""))

    common.wait_until_assert(assert_switchboard_is_empty, tries=3)

    def assert_switchboard_phone_is_hungup():
        phone = step.scenario.phone_register.get_user_phone(switchboard)
        assert_that(phone.is_hungup(), equal_to(True))

    common.wait_until_assert(assert_switchboard_phone_is_hungup, tries=10)


@step(u'Then the switchboard is talking to "([^"]*)" number "([^"]*)"')
def then_the_switchboard_is_talking_to_1_number_2(step, cid_name, cid_num):
    def _switchboard_has_current_call(cid_name, cid_num):
        current_call = cti_helper.get_switchboard_current_call_infos()
        assert_that(current_call['caller_id'], equal_to("%s <%s>" % (cid_name, cid_num)))

    common.wait_until_assert(_switchboard_has_current_call, cid_name, cid_num, tries=10)


@step(u'Then I see transfer destinations:')
def then_i_see_transfer_destinations(step):
    res = cti_helper.get_switchboard_infos()
    assert_res = func.has_subsets_of_dicts(step.hashes, res['return_value']['content'])
    assert_that(assert_res, equal_to(True))


@step(u'Then I see no transfer destinations')
def then_i_see_no_transfer_destinations(step):
    def _switchboard_has_no_transfer_destination():
        res = cti_helper.get_switchboard_infos()
        assert_that(res['return_value']['content'], contains())

    common.wait_until_assert(_switchboard_has_no_transfer_destination, tries=10)
