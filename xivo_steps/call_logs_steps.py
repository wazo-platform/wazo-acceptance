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


from lettuce import step
from xivo_lettuce import common, form, sysutils
from xivo_lettuce.manager import cel_manager, call_logs_manager
from xivo_lettuce.manager_dao import call_logs_manager_dao


@step(u'Given there are no calls between "([^"]*)" and "([^"]*)"')
def given_there_are_no_calls_between(step, start, end):
    cel_manager.delete_entries_between(start, end)
    call_logs_manager_dao.delete_entries_between(start, end)


@step(u'Given there are no calls')
def given_there_are_no_cel(step):
    cel_manager.delete_all()
    call_logs_manager_dao.delete_all()


@step(u'Given I have the following CEL entries:')
def given_i_have_the_following_cel_entries(step):
    cel_manager.insert_entries(step.hashes)


@step(u'When I generate call logs$')
def when_i_generate_call_logs(step):
    command = ['xivo-call-logs']
    sysutils.send_command(command)


@step(u'When I request call logs in the webi with dates:')
def when_i_request_call_logs_in_the_webi_with_dates(step):
    common.open_url('cel')
    form_info = step.hashes[0]
    call_logs_manager.type_dates(form_info['start'], form_info['end'])
    form.submit.submit_form()


@step(u'When I generate call logs using the last \d CEL entries$')
def when_i_generate_call_logs_using_the_last_1_cel_entries(step, cel_count):
    command = ['xivo-call-logs', '-c', cel_count]
    sysutils.send_command(command)


@step(u'Then I should have the following call logs:')
def then_i_should_have_the_following_call_logs(step):
    for entry in step.hashes:
        assert call_logs_manager_dao.has_call_log(entry), "Corresponding call_log entry was not found : %s" % entry


@step(u'Then I have the last call log matching:')
def then_i_have_the_last_call_log_matching(step):
    entry = step.hashes[0]
    assert call_logs_manager_dao.matches_last_call_log(entry), "The last call_log entry did not match : %s" % entry


@step(u'Then I should not have the following call logs:')
def then_i_should_not_have_the_following_call_logs(step):
    for entry in step.hashes:
        assert not call_logs_manager_dao.has_call_log(entry), "Corresponding call_log entry was found : %s" % entry
