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

from hamcrest import assert_that
from hamcrest import contains
from hamcrest import equal_to
from lettuce import step

from xivo_acceptance.action.webi import directory as directory_action_webi
from xivo_acceptance.action.webi import queue as queue_action_webi
from xivo_acceptance.action.webi import user as user_action_webi
from xivo_acceptance.helpers import (bus_helper, user_helper, context_helper, cti_helper, incall_helper)
from xivo_acceptance.lettuce import func, common, sysutils


_switchboard_events = {
    'SwitchboardEnteredEvent': 'switchboard-switchboard.__switchboard/counter-entered',
    'SwitchboardCompletedEvent': 'switchboard-switchboard.__switchboard/counter-completed',
    'SwitchboardAbandonedEvent': 'switchboard-switchboard.__switchboard/counter-abandoned',
    'SwitchboardWaitTimeEvent': 'switchboard-switchboard.__switchboard/gauge-wait',
}


@step(u'Given a configured switchboard with an operator with infos:')
def given_a_configured_switchboard_with_an_operator_with_infos(step):
    switchboard_agents = ['{agent_number}@{context}'.format(**data) for data in step.hashes]
    agent_names = ['{firstname} {lastname}'.format(**data)]
    for data in step.hashes:
        user_helper.add_user_with_infos(data, step=step)

    for agent_name in agent_names:
        user_action_webi.switchboard_config_for_user(agent_name)

    queue_action_webi.add_or_replace_switchboard_queue('__switchboard', '3009',
                                                       'default', switchboard_agents)
    queue_action_webi.add_or_replace_switchboard_hold_queue('__switchboard_hold', '3010', 'default')

    for data in step.hashes:
        agent_name = '{firstname} {lastname}'.format(**data)
        agent_number = data['agent_number']
        phone = step.scenario.phone_register.get_user_phone(agent_name)
        phone.call('*31{}'.format(agent_number))
        common.wait_until(phone.is_hungup, tries=20)

    bus_helper.add_binding('switchboard_stats', 'collectd.switchboard', 'collectd')


@step(u'Then I should receive the following switchboard statistics:')
def then_i_should_receive_the_following_switchboard_statistics(step):
    events = bus_helper.get_messages_from_bus('switchboard_stats')

    for line in step.hashes:
        pattern = _switchboard_events[line['Event']]
        for event in events:
            if pattern in event:
                break
        else:
            assert False, 'No event matched {} in:\n{}'.format(line['Event'], events)


@step(u'Given the switchboard is configured for internal directory lookup')
def given_the_switchboard_is_configured_for_internal_directory_lookup(step):
    context_helper.add_or_replace_context('__switchboard_directory', 'Switchboard', 'internal')
    directory_action_webi.add_or_replace_directory(
        'xivodirswitchboard',
        'http://localhost/service/ipbx/json.php/private/pbx_services/phonebook',
        'phonebook.firstname,phonebook.lastname,phonebook.displayname,phonebook.society,phonebooknumber.office.number',
        '',
        {'name': '{phonebook.displayname}',
         'number': '{phonebooknumber.office.number}',
         'mobile': '{phonebooknumber.mobile.number}'}
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
    sysutils.restart_service('xivo-dird')


@step(u'Given the user "([^"]*)" is configured for switchboard use')
def given_the_user_group1_is_configured_for_switchboard_use(step, user):
    user_action_webi.switchboard_config_for_user(user)


@step(u'Given there is a switchboard configured as:')
def given_there_is_a_switchboard_configured_as(step):
    for config in step.hashes:
        queue_action_webi.add_or_replace_switchboard_queue(
            config['incalls queue name'],
            config['incalls queue number'],
            config['incalls queue context'],
            config['agents'])

        queue_action_webi.add_or_replace_switchboard_hold_queue(
            config['hold calls queue name'],
            config['hold calls queue number'],
            config['hold calls queue context'])

        incall_helper.add_or_replace_incall(number=config['incalls queue number'],
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
