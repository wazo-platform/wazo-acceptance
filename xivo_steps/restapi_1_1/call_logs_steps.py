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

from StringIO import StringIO
from hamcrest import any_of, assert_that, equal_to, greater_than, has_entries, has_length
from lettuce import step, world
from xivo.unicode_csv import UnicodeDictReader
from xivo_lettuce.manager_dao import call_logs_manager_dao
from xivo_lettuce.manager_restapi import call_logs_ws


@step(u'Given there are only the following call logs:')
def given_there_are_only_the_following_call_logs(step):
    call_logs_manager_dao.delete_all()
    call_logs_manager_dao.create_call_logs(step.hashes)


@step(u'When I get the list of call logs$')
def when_i_get_the_list_of_call_logs(step):
    world.response = call_logs_ws.call_logs_list()


@step(u'When I get the list of call logs with arguments:')
def when_i_get_the_list_of_call_logs_with_arguments(step):
    args = step.hashes[0]
    world.response = call_logs_ws.call_logs_list_interval(args)
    world.status = world.response.status


@step(u'Then I get the following call logs in CSV format:')
def then_i_get_the_following_call_logs_in_csv_format(step):
    assert_that(world.response.status, equal_to(200))
    assert_that(world.response.headers['Content-Type'], equal_to('text/csv; charset=utf8'))

    call_logs_response = world.response.data.encode('utf-8')
    assert_that(call_logs_response, has_length(greater_than(0)))

    reader = UnicodeDictReader(StringIO(call_logs_response))
    row_matchers = [has_entries(expected_row) for expected_row in step.hashes]
    csv_rows = [csv_row for csv_row in reader]
    assert_that(csv_rows, has_length(len(step.hashes)))
    for csv_row_dict in csv_rows:
        assert_that(csv_row_dict, any_of(*row_matchers))
