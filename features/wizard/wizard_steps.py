# -*- coding: utf-8 -*-

from lettuce import step, world
from xivo_lettuce.common import waitForLoginPage


@step(u'Given there is XiVO not configured')
def given_there_is_xivo_not_configured(step):
    cmd = ['rm', '-f', '/etc/pf-xivo/web-interface/xivo.ini']
    world.ssh_client_xivo.check_call(cmd)


@step(u'When I open the url')
def when_i_open_the_url(step):
    world.browser.get(world.host)


@step(u'When I start the wizard')
def when_i_start_the_wizard(step):
    world.browser.get(world.host)


@step(u'Then I should see the welcome message (.*)')
def then_i_see_the_welcome_message(step, message):
    assert message in world.browser.page_source


@step(u'When I select language (.*)')
def when_i_select(step, language):
    language_option = world.browser.find_element_by_xpath('//option[@value="%s"]' % language)
    language_option.click()


@step(u'When I click next')
def when_i_click_next(step):
    world.browser.find_element_by_id('it-next').click()


@step(u'When I click validate')
def when_i_click_validate(step):
    world.browser.find_element_by_id('validate').click()


@step(u'When I accept the terms of the licence')
def when_i_accept_the_terms_of_the_licence(step):
    accept_box = world.browser.find_element_by_id('it-license-agree')
    accept_box.click()


@step(u'Then I should be on the (.*) page')
def then_i_should_be_on_page(step, page):
    divid = 'xivo-wizard-step-%s' % page
    div = world.browser.find_element_by_id(divid, '%s page not loaded' % page, timeout=10)
    assert div is not None


@step(u'Then I see the license')
def then_i_see_the_license(step):
    license_textbox = world.browser.find_element_by_id('it-license')
    license_text = license_textbox.text.strip()
    assert license_text.startswith('GNU GENERAL PUBLIC LICENSE')
    assert license_text.endswith('http://www.gnu.org/philosophy/why-not-lgpl.html>.')


@step(u'When I fill hostname (.*), domain (.*), password (.*) in the configuration page')
def when_i_fill_the_configuration_page(step, hostname, domain, password):
    input_hostname = world.browser.find_element_by_id('it-mainconfig-hostname')
    input_domain = world.browser.find_element_by_id('it-mainconfig-domain')
    input_password = world.browser.find_element_by_id('it-mainconfig-adminpasswd')
    input_password_confirm = world.browser.find_element_by_id('it-mainconfig-confirmadminpasswd')
    input_hostname.send_keys(hostname)
    input_domain.send_keys(domain)
    input_password.send_keys(password)
    input_password_confirm.send_keys(password)


@step(u'When I fill entity (.*), start (.*), end (.*)')
def when_i_fill_the_entity_context_page(step, entity, start, end):
    input_entity = world.browser.find_element_by_id('it-entity-displayname')
    input_start = world.browser.find_element_by_id('it-context-internal-numberbeg')
    input_end = world.browser.find_element_by_id('it-context-internal-numberend')
    input_entity.send_keys(entity)
    input_start.send_keys(start)
    input_end.send_keys(end)


@step(u'Then I should be redirected to the login page')
def then_i_should_be_redirected_to_the_login_page(step):
    waitForLoginPage()
    assert world.browser.find_element_by_id('it-login') is not None


@step(u'Then I should be in the monitoring window')
def then_i_should_be_in_the_monitoring_window(step):
    div = world.browser.find_element_by_id('system-infos', 'Could not load the system info page')
    assert div is not None
