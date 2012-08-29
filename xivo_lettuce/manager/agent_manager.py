# -*- coding: utf-8 -*-

from lettuce.registry import world
from xivo_lettuce.common import edit_text_field


def _check_if_in_edit_page():
    world.browser.find_element_by_id('it-agentfeatures-firstname', 'Agent form not loaded')


def type_agent_info(firstName, lastName, number):
    _check_if_in_edit_page()
    edit_text_field('it-agentfeatures-firstname', firstName)
    edit_text_field('it-agentfeatures-lastname', lastName)
    edit_text_field('it-agentfeatures-number', number)


def change_password(password):
    _check_if_in_edit_page()
    edit_text_field('it-agentfeatures-passwd', password)
