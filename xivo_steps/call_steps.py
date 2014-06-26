# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
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

import time

from hamcrest import assert_that
from hamcrest import has_items
from hamcrest import equal_to
from lettuce import step

from xivo_acceptance.helpers import line_helper, callgen_helper, agent_helper, cti_helper, \
    asterisk_helper
from xivo_lettuce import common
from xivo_lettuce import form, func
from xivo_lettuce.form.checkbox import Checkbox
from xivo_lettuce.logs import search_str_in_asterisk_log

from linphonelib import ExtensionNotFoundException


@step(u'When a call is started:')
def when_a_call_is_started(step):

    def _call(caller, callee, hangup, dial, talk_time=0, ring_time=0):
        caller_phone = step.scenario.phone_register.get_user_phone(caller)
        callee_phone = step.scenario.phone_register.get_user_phone(callee)
        first_to_hangup = caller_phone if hangup == 'caller' else callee_phone

        caller_phone.call(dial)
        time.sleep(int(ring_time))
        callee_phone.answer()
        time.sleep(int(talk_time))
        first_to_hangup.hangup()

    for call_info in step.hashes:
        _call(**call_info)


@step(u'Then I should see the following caller id:')
def then_i_should_see_the_following_caller_id(step):
    caller_id_info = step.hashes[0]
    expected = [
        {'Variable': 'xivo-calleridname',
         'Value': caller_id_info['Name']},
        {'Variable': 'xivo-calleridnum',
         'Value': caller_id_info['Number']},
    ]
    assert_that(cti_helper.get_sheet_infos(), has_items(*expected))


@step(u'When chan_test calls "([^"]*)"$')
def when_chan_test_calls(step, extension):
    number, context = func.extract_number_and_context_from_extension(extension)
    cmd = 'test new %s %s' % (number, context)
    asterisk_helper.send_to_asterisk_cli(cmd)


@step(u'When chan_test calls "([^"]*)" with id "([^"]*)"$')
def when_chan_test_calls_with_id(step, extension, channelid):
    number, context = func.extract_number_and_context_from_extension(extension)
    cmd = 'test newid %s %s %s' % (channelid, number, context)
    asterisk_helper.send_to_asterisk_cli(cmd)


@step(u'When chan_test hangs up "([^"]*)"$')
def when_chan_test_hangs_up(step, channelid):
    cmd = 'channel request hangup Test/%s' % channelid
    asterisk_helper.send_to_asterisk_cli(cmd)


@step(u'When "([^"]*)" calls "([^"]*)"$')
def when_a_calls_exten(step, name, exten):
    phone = step.scenario.phone_register.get_user_phone(name)
    phone.call(exten)


@step(u'When "([^"]*)" answers')
def when_a_answers(step, name):
    phone = step.scenario.phone_register.get_user_phone(name)
    phone.answer()


@step(u'When "([^"]*)" hangs up')
def when_a_hangs_up(step, name):
    phone = step.scenario.phone_register.get_user_phone(name)
    phone.hangup()


@step(u'When "([^"]*)" and "([^"]*)" talk for "([^"]*)" seconds')
def when_a_and_b_talk_for_n_seconds(step, _a, _b, n):
    time.sleep(float(n))


@step(u'Then "([^"]*)" last dialed extension was not found')
def then_user_last_dialed_extension_was_not_found(step, name):
    phone = step.scenario.phone_register.get_user_phone(name)
    try:
        phone.last_call_result()
    except ExtensionNotFoundException:
        pass
    else:
        raise AssertionError('ExtensionNotFound was not raised')


@step(u'Then "([^"]*)" is ringing')
def then_user_is_ringing(step, user):
    phone = step.scenario.phone_register.get_user_phone(user)
    assert_that(phone.is_ringing())


@step(u'Then "([^"]*)" is hungup')
def then_group1_is_hungup(step, user):
    phone = step.scenario.phone_register.get_user_phone(user)
    assert_that(phone.is_hungup())


@step(u'Then "([^"]*)" is talking')
def then_group1_is_talking(step, user):
    phone = step.scenario.phone_register.get_user_phone(user)
    assert_that(phone.is_talking())


@step(u'Then "([^"]*)" hears a ringback tone')
def then_user_hears_a_ringback_tone(step, user):
    phone = step.scenario.phone_register.get_user_phone(user)
    assert_that(phone.is_ringback_tone())


@step(u'Then "([^"]*)" sees callerid "([^"]*)"$')
def then_i_see_called_from_callerid(step, user, callerid):
    phone = step.scenario.phone_register.get_user_phone(user)
    assert_that(phone.remote_caller_id(), equal_to(callerid))


@step(u'When a call from "([^"]*)" is received on did "([^"]*)" for "([^"]*)"')
def when_a_call_from_number_to_is_received(step, number, did, name):
    firstname, lastname = name.split(' ', 1)
    vars = {
        'name': name,
        'number': number,
        'login': firstname.lower(),
        'password': lastname.lower(),
        'did': did,
    }
    step.given('Given there is an incall "%(did)s" in context "from-extern" to the "User" "%(name)s"' % vars)
    step.given('Given there is a SIP trunk "%(number)s" in context "from-extern"' % vars)
    step.when('When I start the XiVO Client')
    step.when('When I enable screen pop-up')
    step.when('When I log in the XiVO Client as "%(login)s", pass "%(password)s"' % vars)
    step.given('Given there are no calls running')
    step.given('Given I wait 5 seconds for the dialplan to be reloaded')
    step.given('Given I register extension "%(did)s"' % vars)
    step.given('Given I wait call then I answer then I hang up after "3s"')
    step.when('When there is 1 calls to extension "%(did)s@from-extern" on trunk "%(number)s" and wait' % vars)
    step.given('Given I wait 10 seconds for the call processing')


@step(u'Given there is "([^"]*)" activated in extenfeatures page')
def given_there_is_group1_activated_in_extensions_page(step, option_label):
    common.open_url('extenfeatures')
    option = Checkbox.from_label(option_label)
    option.check()
    form.submit.submit_form()


@step(u'Given the agent "([^"]*)" will answer a call and hangup after (\d+) seconds')
def given_the_agent_will_answer_a_call_and_hangup_after_10_seconds(step, agent_number, seconds):
    call_duration_ms = int(seconds) * 1000
    callgen_helper.execute_answer_then_hangup(call_duration_ms)


@step(u'I register extension "([^"]*)"')
def i_register_extension(step, extension):
    line = line_helper.find_with_extension(extension)
    callgen_helper.execute_sip_register(line.name, line.secret)


@step(u'Given there are no calls running')
def given_there_are_no_calls_running(step):
    callgen_helper.killall_process_sipp()


@step(u'there is ([0-9]+) calls to extension "([^"]+)" and wait$')
def there_is_n_calls_to_extension_and_wait(step, count, extension):
    callgen_helper.execute_n_calls_then_wait(count, extension)


@step(u'When there is ([0-9]+) calls to extension "([^"]+)" on trunk "([^"]+)" and wait$')
def given_there_is_n_calls_to_extension_on_trunk_and_wait(step, count, extension, trunk_name):
    callgen_helper.execute_n_calls_then_wait(count,
                                             extension,
                                             username=trunk_name,
                                             password=trunk_name)


@step(u'When I call extension "([^"]+)"$')
def when_i_call_extension(step, extension):
    callgen_helper.execute_n_calls_then_wait(1, extension)


@step(u'Given there is ([0-9]+) calls to extension "([^"]+)"$')
def given_there_is_n_calls_to_extension_and_hangup(step, count, extension):
    callgen_helper.execute_n_calls_then_hangup(count, extension)


@step(u'Given there is ([0-9]+) calls to extension "([^"]*)" then i hang up after "([0-9]+)s"')
def given_there_is_n_calls_to_extension_then_i_hangup_after_n_seconds(step, count, extension, call_duration):
    call_duration_ms = int(call_duration) * 1000
    callgen_helper.execute_n_calls_then_hangup(count, extension, duration=call_duration_ms)


@step(u'Given extension (\d+) will answer a call and wait')
def given_extension_will_answer_a_call_and_wait(step, extension):
    line = line_helper.find_with_extension(extension)
    callgen_helper.execute_sip_register(line.name, line.secret)
    time.sleep(1)
    callgen_helper.execute_answer_then_wait()
    time.sleep(1)


@step(u'Given extension (\d+) will answer a call, wait (\d+) seconds and hangup')
def given_extension_will_answer_a_call_wait_seconds_and_hangup(step, extension, seconds):
    line = line_helper.find_with_extension(extension)
    callgen_helper.execute_sip_register(line.name, line.secret)
    time.sleep(1)
    callgen_helper.execute_answer_then_hangup()
    time.sleep(1)


@step(u'Given I wait call then I answer and wait')
def given_i_wait_call_then_i_answer_then_i_answer_and_wait(step):
    callgen_helper.execute_answer_then_wait()


@step(u'Given I wait call then I answer then I hang up after "([0-9]+)s"')
def given_i_wait_call_then_i_answer_then_hangup_after_n_seconds(step, call_duration):
    call_duration_ms = int(call_duration) * 1000
    callgen_helper.execute_answer_then_hangup(call_duration_ms)


@step(u'Given I wait call then I answer after "([0-9]+)s" then I wait')
def given_i_wait_then_i_answer_after_n_second_then_i_wait(step, ring_time):
    ring_time_ms = int(ring_time) * 1000
    callgen_helper.execute_answer_then_wait(ring_time_ms)


@step(u'I wait (\d+) seconds')
def given_i_wait_n_seconds(step, count):
    time.sleep(int(count))


@step(u'When I call extension "([^"]*)" from trunk "([^"]*)"')
def when_i_call_extension_from_trunk(step, extension, trunk_name):
    callgen_helper.execute_n_calls_then_wait(1,
                                             extension,
                                             username=trunk_name,
                                             password=trunk_name)


@step(u'Then I see no recording file of this call in monitoring audio files page')
def then_i_not_see_recording_file_of_this_call_in_monitoring_audio_files_page(step):
    now = int(time.time())
    search = 'user-1100-1101-%d.wav'
    nbtries = 0
    maxtries = 5
    while nbtries < maxtries:
        file_name = search % (now - nbtries)
        assert not common.element_is_in_list('sounds', file_name, {'dir': 'monitor'})
        nbtries += 1


@step(u'Then I see rejected call to extension "([^"]+)" in asterisk log')
def then_i_see_rejected_call_in_asterisk_log(step, extension):
    number, context = func.extract_number_and_context_from_extension(extension)
    expression = "to extension '%s' rejected because extension not found in context '%s'" % (number, context)
    assert search_str_in_asterisk_log(expression)
