# -*- coding: utf-8 -*-

from lettuce.registry import world
from xivo_ws import Agent


def get_agent_password_with_number(number):
    agent = world.ws.agents.find_one_by_number(number)
    return agent.password


def get_agent_id_with_number(number):
    agent = world.ws.agents.find_one_by_number(number)
    return agent.id


def delete_agent_with_number(number):
    agents = world.ws.agents.search_by_number(number)
    for agent in agents:
        world.ws.agents.delete(agent.id)


def add_agent(firstname, lastname, number, passwd, context='default', user_id=[]):
    try:
        agent = world.ws.agents.find_one_by_number(number)
    except Exception:
        agent = Agent()
    else:
        delete_agent_with_number(number)
    agent.firstname = firstname
    agent.lastname = lastname
    agent.password = passwd
    agent.number = number
    agent.context = context
    if user_id:
        agent.users = user_id
    world.ws.agents.add(agent)
    agent = world.ws.agents.find_one_by_number(number)
    return agent.id
