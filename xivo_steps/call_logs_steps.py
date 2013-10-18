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

from hamcrest import all_of, assert_that, equal_to, has_property, has_item
from lettuce import step, world

from xivo_acceptance.action.webi import call_logs as call_logs_action_webi
from xivo_acceptance.helpers import call_logs_helper, cel_helper
from xivo_lettuce import common, form, sysutils


@step(u'Given there are no call logs$')
def given_there_are_no_call_logs(step):
    call_logs_helper.delete_all()


@step(u'Given I have only the following CEL entries:')
def given_i_have_only_the_following_cel_entries(step):
    cel_helper.delete_all()
    cel_helper.insert_entries(step.hashes)


@step(u'When I generate call logs$')
def when_i_generate_call_logs(step):
    command = ['xivo-call-logs']
    sysutils.send_command(command)


@step(u'When I request call logs in the webi with dates:')
def when_i_request_call_logs_in_the_webi_with_dates(step):
    common.open_url('cel')
    form_info = step.hashes[0]
    call_logs_action_webi.type_dates(form_info['start'], form_info['end'])
    form.submit.submit_form()


@step(u'When I generate call logs using the last (\d+) unprocessed CEL entries$')
def when_i_generate_call_logs_using_the_last_unprocessed_1_cel_entries(step, cel_count):
    command = ['xivo-call-logs', '-c', cel_count]
    sysutils.send_command(command)


@step(u'When I generate call logs twice in parallel')
def when_i_generate_call_logs_twice_in_parallel(step):
    command = ['xivo-call-logs', '&', 'xivo-call-logs']
    world.command_output = sysutils.output_command(command)


@step(u'When I ask for the list of CEL via WebService:')
def when_i_ask_for_the_list_of_cel_via_webservice(step):
    list_infos = step.hashes[0]
    start_date = list_infos['start date']
    end_date = list_infos['end date']
    world.response = world.ws.cels.search_by_date(start_date, end_date)


@step(u'Then I get a list with the following CEL:')
def then_i_get_a_list_with_the_following_cel(step):
    for cel in step.hashes:
        assert_that(world.response, has_item(_is_cel(cel)))


def _is_cel(cel):
    matchers = [has_property(key, value) for (key, value) in cel.iteritems()]
    return all_of(*matchers)


@step(u'Then I see that call log generation is already running')
def then_i_see_that_call_log_generation_is_already_running(step):
    assert_that(world.command_output.rstrip(), equal_to('xivo-call-logs is already running'))


@step(u'Then I should have the following call logs:')
def then_i_should_have_the_following_call_logs(step):
    for entry in step.hashes:
        assert call_logs_helper.has_call_log(entry), "Corresponding call_log entry was not found : %s" % entry


@step(u'Then I have the last call log matching:')
def then_i_have_the_last_call_log_matching(step):
    entry = step.hashes[0]
    assert call_logs_helper.matches_last_call_log(entry), "The last call_log entry did not match : %s" % entry


@step(u'Then I should not have the following call logs:')
def then_i_should_not_have_the_following_call_logs(step):
    for entry in step.hashes:
        assert not call_logs_helper.has_call_log(entry), "Corresponding call_log entry was found : %s" % entry
