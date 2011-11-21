# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world

def _login(user, password, language):
    input_login = world.browser.find_element_by_id('it-login')
    input_password = world.browser.find_element_by_id('it-password')
    input_login.send_keys(user)
    input_password.send_keys(password)
    language_option = world.browser.find_element_by_xpath('//option[@value="%s"]' % language)
    language_option.click()
    world.browser.find_element_by_id('it-submit').click()
    world.wait_for_id('loginbox', 'Cannot login as ' + user)

def waitForLoginPage():
    world.wait_for_id('it-login', 'login page not loaded', 30)


@step(u'When I login as (.*) with password (.*) in (.*)')
def when_i_login_the_webi(step, login, password, language):
    _login(login, password, language)

@step(u'Given I login as (.*) with password (.*) at (.*)')
def given_i_login_as_with_password_at(step, user, password, url):
    world.url = url
    world.browser.get(world.url)
    waitForLoginPage()
    _login(user, password, 'en')
