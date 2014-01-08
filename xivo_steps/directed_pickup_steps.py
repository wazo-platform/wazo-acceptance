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

from lettuce import step, world

from xivo_acceptance.helpers import line_helper, callgen_helper

_PICKUP_PREFIX = '*8'


@step('I wait call then I do not answer')
def i_wait_call_then_i_do_not_answer(step):
    ring_time_ms = 600 * 1000
    callgen_helper.execute_answer_then_wait(ring_time_ms)


@step(u'line "([^"]+)" calls number "(\d+)" then wait')
def line_calls_extension_then_wait(step, extension, number):
    calling_line = line_helper.find_with_extension(extension)
    callgen_helper.execute_n_calls_then_wait(1, number, calling_line.name, calling_line.secret)


@step(u'line "([^"]+)" pick up call at number "(\d+)"')
def line_pick_up_call_at_number(step, extension, number):
    calling_line = line_helper.find_with_extension(extension)
    pickup_number = _PICKUP_PREFIX + number
    returncode = callgen_helper.execute_pickup_call(pickup_number, calling_line.name, calling_line.secret)
    world.pickup_success = (returncode == 0)


@step(u'Then the directed pickup is successful')
def the_directed_pickup_is_successful(step):
    assert world.pickup_success
