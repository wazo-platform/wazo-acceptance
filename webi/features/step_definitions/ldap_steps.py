# -*- coding: utf-8 -*-

from lettuce import step, world
from xivo_lettuce.common import open_url, element_is_not_in_list, \
    submit_form
from xivo_lettuce.manager import ldap_manager as ldap_man


@step(u'I create an LDAP server with name "([^"]*)" and host "([^"]*)"')
def i_create_an_ldap_server_with_name_1_and_host_2(step, name, host):
    open_url('ldapserver', 'add')
    ldap_man.type_ldap_name_and_host(name, host)
    submit_form()


@step(u'Given there is a LDAP server with name "([^"]*)" and with host "([^"]*)"')
def given_there_is_a_ldap_server_with_name_1_and_with_host_2(step, name, host):
    if element_is_not_in_list('ldapserver', name):
        step.given('I create an LDAP server with name "test-ldap-server" and host "test-ldap-server"')


@step(u'When I go on the add LDAP filter page')
def when_i_go_on_the_add_ldap_filter_page(step):
    open_url('ldapfilter', 'add')


@step(u'When I set the display name to "([^"]*)"')
def when_i_set_the_display_name_to_1(step, display_name):
    add_button = world.browser.find_element_by_id('bt-ldapfilter-attrdisplayname-add')
    add_button.click()
    alert = world.browser.switch_to_alert()
    alert.send_keys(display_name)
    alert.accept()


@step(u'When I set the phone number to "([^"]*)"')
def when_i_set_the_phone_number_to_1(step, phone_number):
    add_button = world.browser.find_element_by_id('bt-ldapfilter-attrphonenumber-add')
    add_button.click()
    alert = world.browser.switch_to_alert()
    alert.send_keys(phone_number)
    alert.accept()
