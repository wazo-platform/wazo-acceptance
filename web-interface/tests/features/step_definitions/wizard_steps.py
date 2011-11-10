# -*- coding: utf-8 -*-

from lettuce import step
from lettuce import world


@step(u'Given that there is a XiVO installed at (.*)')
def given_that_there_is_a_xivo_installed_at(step, ip):
    world.ip = ip


@step(u'When I start the wizard')
def when_i_start_the_wizard(step):
    world.browser.get(world.ip)


@step(u'Then I should see the welcome message (.*)')
def then_i_see_the_welcome_message(step, message):
    assert message in world.browser.page_source

@step(u'When I select (.*)')
def when_i_select(step, language):
    language_select = world.browser.find_element_by_id('it-language')
    language_select.send_keys(language)
    language_select.click()


@step(u'When I click next')
def when_i_click_next(step):
    world.browser.find_element_by_id('it-next').click()
