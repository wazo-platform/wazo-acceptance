# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException

from common.common import *
from checkbox import Checkbox

@step(u'Given the option "([^"]*)" is (not )?checked')
def given_the_option_is_checked(step, option_name, checkstate):
    the_option_is_checked(option_name, checkstate, given = True)

@step(u'Then the option "([^"]*)" is (not )?checked')
def then_the_option_is_checked(step, option_name, checkstate):
    the_option_is_checked(option_name, checkstate)

@step(u'When I (un)?check this option')
def when_i_check_this_option(step, checkstate):
    option = world.browser.find_element_by_label(world.last_option_label)
    goal_checked = (checkstate is None)
    Checkbox(option).set_checked(goal_checked)

@step(u'When I submit')
def when_i_submit(step):
    submit_form()

@step(u'Then this option is (not )?checked')
def then_this_option_is_checked(step, checkstate):
    the_option_is_checked(world.last_option_label, checkstate)
