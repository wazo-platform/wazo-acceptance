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

import time

from hamcrest import assert_that
from hamcrest import equal_to
from hamcrest import has_items
from hamcrest import is_
from hamcrest import not_
from lettuce import step
from lettuce import world

from xivo_acceptance.helpers import cti_helper
from xivo_acceptance.helpers import asterisk_helper
from xivo_acceptance.helpers import line_sip_helper
from xivo_acceptance.helpers import sip_config
from xivo_acceptance.helpers import sip_phone
from xivo_acceptance.helpers import user_helper
from xivo_acceptance.lettuce import common
from xivo_acceptance.lettuce import form, func
from xivo_acceptance.lettuce.form.checkbox import Checkbox

from linphonelib import ExtensionNotFoundException


@step(u'Given there is "([^"]*)" activated in extenfeatures page')
def given_there_is_group1_activated_in_extensions_page(step, option_label):
    common.open_url('extenfeatures')
    option = Checkbox.from_label(option_label)
    option.check()
    form.submit.submit_form()


@step(u'When a call is started:')
def when_a_call_is_started(step):

    def _call(caller, callee, hangup, dial, talk_time=0, ring_time=0):
        caller_phone = step.scenario.phone_register.get_user_phone(caller)
        callee_phone = step.scenario.phone_register.get_user_phone(callee)
        first_to_hangup = caller_phone if hangup == 'caller' else callee_phone

        caller_phone.call(dial)
        _sleep(ring_time)
        callee_phone.answer()
        _sleep(talk_time)
        first_to_hangup.hangup()

    for call_info in step.hashes:
        _call(**call_info)


@step(u'When chan_test calls "([^"]*)"$')
def when_chan_test_calls(step, extension):
    number, context = func.extract_number_and_context_from_extension(extension)
    cmd = 'test new %s %s chan-test-num chan-test-name SIP' % (number, context)
    asterisk_helper.send_to_asterisk_cli(cmd)


@step(u'When chan_test calls "([^"]*)" with id "([^"]*)"$')
def when_chan_test_calls_with_id(step, extension, channelid):
    number, context = func.extract_number_and_context_from_extension(extension)
    cmd = 'test newid %s %s %s chan-test-num chan-test-name SIP' % (channelid, number, context)
    asterisk_helper.send_to_asterisk_cli(cmd)


@step(u'When chan_test calls "([^"]*)" with id "([^"]*)" and calleridname "([^"]*)" and calleridnum "([^"]*)"$')
def when_chan_test_calls_with_id_calleridname_calleridnum(step, extension, channelid, calleridname, calleridnum):
    number, context = func.extract_number_and_context_from_extension(extension)
    cmd = 'test newid %s %s %s %s %s SIP' % (channelid, number, context, calleridnum, calleridname)
    asterisk_helper.send_to_asterisk_cli(cmd)


@step(u'chan_test hangs up "([^"]*)"$')
def when_chan_test_hangs_up(step, channelid):
    cmd = 'channel request hangup SIP/auto-%s' % channelid
    asterisk_helper.send_to_asterisk_cli(cmd)


@step(u'(?:When|Given) "([^"]*)" calls "([^"]*)"$')
def a_calls_exten(step, name, exten):
    phone = step.scenario.phone_register.get_user_phone(name)
    phone.call(exten)


@step(u'(?:Given|When) "([^"]*)" calls "([^"]*)" and waits until the end$')
def when_a_calls_exten_and_waits_until_the_end(step, name, exten):
    phone = step.scenario.phone_register.get_user_phone(name)
    phone.call(exten)
    common.wait_until(phone.is_hungup, tries=10)


@step(u'When "([^"]*)" calls "([^"]*)" and wait for "([^"]*)" seconds')
def when_someone_calls_an_exten_and_wait_for_n_seconds(step, name, exten, tries):
    phone = step.scenario.phone_register.get_user_phone(name)
    phone.call(exten)
    common.wait_until(phone.is_hungup, tries=int(tries))


@step(u'When "([^"]*)" transfers to "([^"]*)"')
def when_alice_transfers_to_exten(step, name, exten):
    phone = step.scenario.phone_register.get_user_phone(name)
    phone.transfer(exten)


@step(u'(?:When|Given) "([^"]*)" answers')
def a_answers(step, name):
    phone = step.scenario.phone_register.get_user_phone(name)
    phone.answer()


@step(u'When "([^"]*)" hangs up')
def when_a_hangs_up(step, name):
    phone = step.scenario.phone_register.get_user_phone(name)
    phone.hangup()


@step(u'When "([^"]*)" puts (?:his|her) call on hold')
def when_a_puts_his_call_on_hold(step, name):
    phone = step.scenario.phone_register.get_user_phone(name)
    phone.hold()


@step(u'When "([^"]*)" resumes (?:his|her) call')
def when_a_resumes_his_call(step, name):
    phone = step.scenario.phone_register.get_user_phone(name)
    phone.resume()


@step(u'I wait (\d+) seconds')
def given_i_wait_n_seconds(step, seconds):
    _sleep(seconds)


@step(u'When "([^"]*)" waits for (\d+) seconds')
def when_a_waits_for_n_seconds(step, _waiter, seconds):
    _sleep(seconds)


@step(u'When I reconfigure the phone "([^"]*)" on line (\d+)@(\w+)')
def when_i_reconfigure_the_phone_1_on_line_2_3(step, name, exten, context):
    step.scenario.phone_register.remove(name)
    line = line_sip_helper.find_with_exten_context(exten, context)
    phone_config = sip_config.create_config(world.config, step.scenario.phone_register, line)

    def phone_is_registered():
        return sip_phone.register_line(phone_config)

    phone = common.wait_until(phone_is_registered)
    assert_that(phone, is_(not_(None)))
    step.scenario.phone_register.add_registered_phone(phone, name)


@step(u'Then "([^"]*)" last dialed extension was not found')
def then_user_last_dialed_extension_was_not_found(step, name):
    phone = step.scenario.phone_register.get_user_phone(name)
    try:
        phone.last_call_result()
    except ExtensionNotFoundException:
        pass
    else:
        raise AssertionError('ExtensionNotFound was not raised')


@step(u'(?:Given|Then) "([^"]*)" is ringing')
def user_is_ringing(step, user):
    phone = step.scenario.phone_register.get_user_phone(user)
    common.wait_until(phone.is_ringing, tries=3)


@step(u'When "([^"]*)" transfers "([^"]*)" to "([^"]*)" with timeout "([^"]*)" via xivo-ctid-ng')
def when_1_transfers_2_to_3_with_timeout_4_via_xivo_ctid_ng(self, initiator, transferred, recipient_exten, timeout):
    transferred_uuid = user_helper.get_user_by_name(transferred)['uuid']
    initiator_uuid = user_helper.get_user_by_name(initiator)['uuid']

    calls = world.ctid_ng_client.calls.list_calls()['items']

    transferred_calls = [call for call in calls if call['user_uuid'] == transferred_uuid]
    try:
        transferred_call_id = transferred_calls[0]['call_id']
    except KeyError:
        raise Exception('No call found for user {} with UUID {}'.format(transferred, transferred_uuid))
    initiator_calls = [call for call in calls if call['user_uuid'] == initiator_uuid]
    try:
        initiator_call_id = initiator_calls[0]['call_id']
    except KeyError:
        raise Exception('No call found for user {} with UUID {}'.format(initiator, initiator_uuid))

    world.ctid_ng_client.transfers.make_transfer(transferred=transferred_call_id,
                                                 initiator=initiator_call_id,
                                                 context='default',
                                                 exten=recipient_exten,
                                                 timeout=int(timeout))


@step(u'Then "([^"]*)" is hungup')
def then_group1_is_hungup(step, user):
    phone = step.scenario.phone_register.get_user_phone(user)
    common.wait_until(phone.is_hungup, tries=3)


@step(u'Then "([^"]*)" is talking')
def then_group1_is_talking(step, user):
    phone = step.scenario.phone_register.get_user_phone(user)
    common.wait_until(phone.is_talking, tries=3)


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


@step(u'Then I should see the following caller id:')
def then_i_should_see_the_following_caller_id(step):
    caller_id_info = step.hashes[0]
    expected = [
        {'Variable': 'xivo-calleridname',
         'Value': caller_id_info['Name']},
        {'Variable': 'xivo-calleridnum',
         'Value': caller_id_info['Number']},
    ]

    def assertion():
        assert_that(cti_helper.get_sheet_infos(), has_items(*expected))

    common.wait_until_assert(assertion, tries=4)


@step(u'Then "([^"]*)" call "([^"]*)" is "([^"]*)"')
def then_name_call_field_is_value(step, name, field, value):
    user_uuid = user_helper.get_user_by_name(name)['uuid']

    def assertion():
        calls = world.ctid_ng_client.calls.list_calls()
        for call in calls['items']:
            if call['user_uuid'] == user_uuid:
                assert_that(call[field], equal_to(eval(value)))
                break
        else:
            assert False, 'Found no call for {}'.format(name)

    common.wait_until_assert(assertion, tries=3)


def _sleep(seconds):
    time.sleep(float(seconds))
