# -*- coding: UTF-8 -*-

from lettuce import step, world
from xivo_lettuce.manager_ws.line_manager_ws import find_line_with_extension
from xivo_lettuce.manager.call_manager import execute_n_calls_then_wait, \
    execute_pickup_call, execute_answer_then_wait

_PICKUP_PREFIX = '*8'


@step('I wait call then I do not answer')
def i_wait_call_then_i_do_not_answer(step):
    ring_time_ms = 600 * 1000
    execute_answer_then_wait(ring_time_ms)


@step(u'line "([^"]+)" calls number "(\d+)" then wait')
def line_calls_extension_then_wait(step, extension, number):
    calling_line = find_line_with_extension(extension)
    execute_n_calls_then_wait(1, number, calling_line.name, calling_line.secret)


@step(u'line "([^"]+)" pick up call at number "(\d+)"')
def line_pick_up_call_at_number(step, extension, number):
    calling_line = find_line_with_extension(extension)
    pickup_number = _PICKUP_PREFIX + number
    returncode = execute_pickup_call(pickup_number, calling_line.name, calling_line.secret)
    world.pickup_success = (returncode == 0)


@step(u'Then the directed pickup is successful')
def the_directed_pickup_is_successful(step):
    assert world.pickup_success
