# -*- coding: utf-8 -*-

import time

from lettuce import step
from xivo_lettuce.common import webi_login, remove_element_if_exist, \
    element_is_in_list, element_is_not_in_list, go_to_tab
from xivo_lettuce import form
from selenium.common.exceptions import NoSuchElementException


@step(u'When I login as (.*) with password (.*) in (.*)')
def when_i_login_the_webi(step, login, password, language):
    webi_login(login, password, language)


@step(u'Given there is no ([a-z ]*) "([^"]*)"$')
def given_there_is_no_element(step, module, search):
    remove_element_if_exist(module, search)


@step(u'Then ([a-z ]*) "([^"]*)" is displayed in the list$')
def then_value_is_displayed_in_the_list(step, type, search):
    assert element_is_in_list(type, search)


@step(u'Then ([a-z ]*) "([^"]*)" is not displayed in the list$')
def then_value_is_not_displayed_in_the_list(step, type, search):
    assert element_is_not_in_list(type, search)


@step(u'I submit$')
def i_submit(step):
    time.sleep(1)
    form.submit.submit_form()


@step(u'Then I see no errors')
def then_i_see_no_errors(step):
    # this step is there mostly for test readability; it's a no-op in most cases
    # since it's already checked when a form is submitted
    try:
        error_element = form.submit.find_form_errors()
    except NoSuchElementException:
        pass
    else:
        raise form.submit.FormErrorException(error_element.text)


@step(u'Then I see errors')
def then_i_see_errors(step):
    form.submit.assert_form_errors()


@step('I go to the "([^"]*)" tab')
def i_go_to_the_1_tab(step, tab_text):
    go_to_tab(tab_text)
