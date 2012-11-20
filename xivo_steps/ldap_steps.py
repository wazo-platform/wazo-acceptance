# -*- coding: utf-8 -*-

from lettuce import step, world
from xivo_lettuce import form
from xivo_lettuce.common import open_url, element_is_not_in_list, go_to_tab
from xivo_lettuce.manager import ldap_manager as ldap_man
from selenium.webdriver.support.select import Select


@step(u'I create an LDAP server with name "([^"]*)" and host "([^"]*)"')
def i_create_an_ldap_server_with_name_1_and_host_2(step, name, host):
    open_url('ldapserver', 'add')
    ldap_man.type_ldap_name_and_host(name, host)
    form.submit.submit_form()


@step(u'Given there is a LDAP server with name "([^"]*)" and with host "([^"]*)"')
def given_there_is_a_ldap_server_with_name_1_and_with_host_2(step, name, host):
    if element_is_not_in_list('ldapserver', name):
        step.given('I create an LDAP server with name "test-ldap-server" and host "test-ldap-server"')


@step(u'I create an LDAP filter with name "([^"]*)" and server "([^"]*)"')
def i_create_an_ldap_filter_with_name_and_server(step, name, server):
    open_url('ldapfilter', 'add')
    text_input = world.browser.find_element_by_label("Name")
    text_input.clear()
    text_input.send_keys(name)
    text_input = world.browser.find_element_by_label("Base DN")
    text_input.clear()
    text_input.send_keys("dc=lan-quebec,dc=avencall,dc=com")
    select_input = world.browser.find_element_by_label("LDAP Server")
    Select(select_input).select_by_visible_text(server)
    go_to_tab("Attributes")
    add_button = world.browser.find_element_by_id('bt-ldapfilter-attrdisplayname-add')
    add_button.click()
    alert = world.browser.switch_to_alert()
    alert.send_keys("sn")
    alert.accept()
    add_button = world.browser.find_element_by_id('bt-ldapfilter-attrphonenumber-add')
    add_button.click()
    alert = world.browser.switch_to_alert()
    alert.send_keys("telephoneNumber")
    alert.accept()
    form.submit.submit_form()


@step(u'Given there exist an LDAP entry "([^"]*)" on ldap server "([^"]*)"')
def given_there_exist_an_ldap_entry_on_ldap_server(step, dn, server):
    commands = ['slapcat | grep "cn=foobar state,ou=people,dc=lan-quebec,dc=avencall,dc=com"']
    ret = world.ssh_client_xivo.out_call(commands)
    assert False, ret


@step(u'When I search "([^"]*)" on an aastra phone')
def when_i_search_group1_on_an_aastra_phone(step, group1):
    assert False, 'This step must be implemented'


@step(u'Then result "([^"]*)" is present')
def then_result_group1_is_present(step, group1):
    assert False, 'This step must be implemented'

@step(u'Given there is an LDAP filter with name "([^"]*)" and with server "([^"]*)"')
def given_there_is_an_ldap_filter_with_name_and_with_server(step, name, server):
    if element_is_not_in_list('ldapfilter', name):
        step.given('I create an LDAP filter with name "%s" and server "%s"' % (name,server))


#@step(u'When I go on the add LDAP filter page')
#def when_i_go_on_the_add_ldap_filter_page(step):
#    open_url('ldapfilter', 'add')
#
#
#@step(u'When I set the display name to "([^"]*)"')
#def when_i_set_the_display_name_to_1(step, display_name):
#    add_button = world.browser.find_element_by_id('bt-ldapfilter-attrdisplayname-add')
#    add_button.click()
#    alert = world.browser.switch_to_alert()
#    alert.send_keys(display_name)
#    alert.accept()
#
#
#@step(u'When I set the phone number to "([^"]*)"')
#def when_i_set_the_phone_number_to_1(step, phone_number):
#    add_button = world.browser.find_element_by_id('bt-ldapfilter-attrphonenumber-add')
#    add_button.click()
#    alert = world.browser.switch_to_alert()
#    alert.send_keys(phone_number)
#    alert.accept()
