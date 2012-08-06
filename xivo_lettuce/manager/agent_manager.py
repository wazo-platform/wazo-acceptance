# -*- coding: utf-8 -*-

from lettuce.registry import world
from xivo_ws import Agent
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


def get_password(number):
    agent = world.ws.agents.search_one_agent_by_number(number)
    return agent.password


def insert_agent(firstname, lastname, number, passwd):
    agent = Agent()
    agent.firstname = firstname
    agent.lastname = lastname
    agent.password = passwd
    agent.number = number
    agent.context = 'default'
    world.ws.agents.add(agent)


def delete_agent_by_number(number):
    agents = world.ws.agents.search_agents_by_number(number)
    for agent in agents:
        world.ws.agents.delete(agent.id)


def find_agent_id_from_number(number):
    agent = world.ws.agents.search_one_agent_by_number(number)
    return agent.id
