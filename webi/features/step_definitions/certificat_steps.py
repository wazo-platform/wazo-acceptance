# -*- coding: utf-8 -*-
from lettuce import step, world

from xivo_lettuce.common import find_line, open_url, remove_line, submit_form, \
    remove_line, remove_element_if_exist, remove_all_elements


def create_basic_certificat(name, email, validity_dt):
    open_url('certificat', 'add')
    input_name = world.browser.find_element_by_id('it-name')
    input_name.send_keys(name)
    autosign_check = world.browser.find_element_by_id('it-autosigned')
    autosign_check.click()
    input_date = world.browser.find_element_by_id('it-validity-end')
    input_date.send_keys(validity_dt)
    input_email = world.browser.find_element_by_id('it-subject-emailAddress')
    input_email.send_keys(email)

@step(u'Given There are no certificats named "([^"]*)"')
def given_there_are_no_certificats_named_group1(step, name):
    remove_all_elements('certificat', name)

@step(u'When i create a certificat with name "([^"]*)" and with email "([^"]*)" and validity date "([^"]*)"')
def when_i_create_a_certificat_with_name_group1_and_with_email_group2_and_validity_date_group3(step, name, email, validity_dt):
    create_basic_certificat(name, email, validity_dt)

