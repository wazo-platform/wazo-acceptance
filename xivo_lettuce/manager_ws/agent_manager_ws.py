# -*- coding: utf-8 -*-

from lettuce import world
from xivo_ws import Agent


def add_agent(data_dict):
    agent = Agent()
    agent.firstname = data_dict['firstname']
    agent.number = data_dict['number']
    agent.context = data_dict['context']

    if 'lastname' in data_dict:
        agent.lastname = data_dict['lastname']
    if 'passwd' in data_dict:
        agent.passwd = data_dict['passwd']
    if 'wrapuptime' in data_dict:
        agent.wrapuptime = data_dict['wrapuptime']
    if 'users' in data_dict:
        agent.users = data_dict['users']

    world.ws.agents.add(agent)
    agent = world.ws.agents.find_one_by_number(data_dict['number'])
    return int(agent.id)


def add_or_replace_agent(data_dict):
    agent_number = data_dict['number']
    delete_agents_with_number(agent_number)

    return add_agent(data_dict)


def delete_agents_with_number(number):
    for agent in _search_agents_with_number(number):
        world.ws.agents.delete(agent.id)


def find_agent_id_with_number(number):
    agent = _find_agent_with_number(number)
    return agent.id


def find_agent_password_with_number(number):
    agent = _find_agent_with_number(number)
    return agent.password


def get_agent_with_number(number):
    agent = _find_agent_with_number(number)
    return world.ws.agents.view(agent.id)


def _find_agent_with_number(number):
    return world.ws.agents.find_one_by_number(number)


def _search_agents_with_number(number):
    return world.ws.agents.search_by_number(number)
