# -*- coding: utf-8 -*-

import json
from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException
from xivo_lettuce.common import *

WSA = get_webservices('agent')

def type_agent_info(firstName, lastName, number):
    world.browser.find_element_by_id('it-agentfeatures-firstname', 'Agent form not loaded')
    input_firstName = world.browser.find_element_by_id('it-agentfeatures-firstname')
    input_lastName = world.browser.find_element_by_id('it-agentfeatures-lastname')
    input_number = world.browser.find_element_by_id('it-agentfeatures-number')
    input_firstName.clear()
    input_firstName.send_keys(firstName)
    input_lastName.clear()
    input_lastName.send_keys(lastName)
    input_number.clear()
    input_number.send_keys(number)


def insert_agent(firstname, lastname, number, passwd):
    jsoncontent = WSA.get_json_file_content('agent')
    datajson = jsoncontent % {
                               'firstname': firstname,
                               'lastname': lastname,
                               'number': number,
                               'passwd': passwd,
                               'userlist': ', "user-select" : []'
                               }
    data = json.loads(datajson)
    WSA.add(data)


def delete_agent(number):
    for agent in find_agent_id_from_number(number):
        if not WSA.delete(agent['id']):
            raise Exception('Unable to delete agent %s' % agent['id'])


def find_agent_id_from_number(number):
    agent_list = WSA.search(number)
    if agent_list:
        return agent_list
    else:
        return []
