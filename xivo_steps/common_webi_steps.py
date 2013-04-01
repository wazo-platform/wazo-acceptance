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
from xivo_lettuce.common import webi_login, remove_element_if_exist, \
    element_is_in_list, element_is_not_in_list, go_to_tab
from xivo_lettuce import form
from selenium.common.exceptions import NoSuchElementException


@step(u'When I login as (.*) with password (.*) in (.*)')
def when_i_login_the_webi(step, login, password, language):
    webi_login(login, password, language)


@step(u'Given there is no ([a-z _]*) "([^"]*)"$')
def given_there_is_no_element(step, module, search):
    remove_element_if_exist(module, search)


@step(u'Then ([a-z ]*) "([^"]*)" is displayed in the list$')
def then_value_is_displayed_in_the_list(step, type, search):
    assert element_is_in_list(type, search)


@step(u'Then ([a-z ]*) "([^"]*)" is not displayed in the list$')
def then_value_is_not_displayed_in_the_list(step, type, search):
    assert element_is_not_in_list(type, search)


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
