# -*- coding: utf-8 -*-

from lettuce.registry import world
from xivo_lettuce.common import find_line, remove_line, open_url
from xivo_lettuce import form
from selenium.common.exceptions import NoSuchElementException


def _check_if_in_edit_page():
    world.browser.find_element_by_id('it-agentfeatures-firstname', 'Agent form not loaded')


def type_agent_info(firstName, lastName, number):
    _check_if_in_edit_page()
    form.input.edit_text_field_with_id('it-agentfeatures-firstname', firstName)
    form.input.edit_text_field_with_id('it-agentfeatures-lastname', lastName)
    form.input.edit_text_field_with_id('it-agentfeatures-number', number)


def change_password(password):
    _check_if_in_edit_page()
    form.input.edit_text_field_with_id('it-agentfeatures-passwd', password)


def remove_agent_group_if_exist(agent_group):
    try:
        remove_line(agent_group)
    except NoSuchElementException:
        pass


def select_agent_group_list(agent_group_list):
    for agent_group in agent_group_list:
        table_line = _get_agent_group_webelement_line(agent_group.strip())
        element = table_line.find_element_by_xpath(".//input[@name='agentgroups[]']")
        element.click()


def is_agent_in_agent_group(agent_group, agent_name):
    go_to_agent_group_page_list(agent_group)
    form.input.edit_text_field_with_id('it-toolbar-search', agent_name)
    form.submit.submit_form('it-toolbar-subsearch')
    try:
        find_line(agent_name)
    except NoSuchElementException:
        return False
    return True


def go_to_agent_group_page_list(agent_group):
    open_url('agent', 'list')
    table_line = _get_agent_group_webelement_line(agent_group)
    url_agent_group = table_line.find_element_by_xpath(".//a[@title='%s']" % agent_group)
    url_agent_group.click()


def get_agent_group_id(agent_group):
    open_url('agent', 'list')
    table_line = _get_agent_group_webelement_line(agent_group)
    agent_group_id = int(table_line.find_element_by_xpath(".//input[@name='agentgroups[]']").get_attribute('value'))
    return agent_group_id


def get_nb_agents_in_group(agent_group):
    open_url('agent', 'list')
    table_line = _get_agent_group_webelement_line(agent_group)
    nb_agent = int(table_line.find_element_by_xpath(".//td[3]").text)
    return nb_agent


def _get_agent_group_webelement_line(agent_group):
    try:
        return find_line(agent_group)
    except NoSuchElementException:
        return False
