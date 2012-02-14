# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world

from xivo_lettuce.common import *
from xivo_lettuce.manager import queue_manager
from xivo_lettuce.manager import line_manager


@step(u'Given there is no queue "([^"]*)"')
def given_there_is_no_queue_1(step, queue_displayname):
    queue_manager.delete_queue_from_displayname(queue_displayname)


@step(u'Given there is no queue with number "([^"]*)"')
def given_there_is_no_queue_with_number_1(step, queue_number):
    queue_manager.delete_queue_from_number(queue_number)


@step(u'When I add a queue')
def when_i_add_a_queue(step):
    queue_manager.open_add_queue_form()


@step(u'Then I see the queue "([^"]*)" in the list')
def then_i_see_the_queue_1_in_the_list(step, queue_displayname):
    queue_manager.open_list_queue_url()
    find_line(queue_displayname)
