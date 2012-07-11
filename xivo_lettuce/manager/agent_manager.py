# -*- coding: utf-8 -*-

import json
from lettuce.registry import world
from xivo_lettuce.common import get_webservices, edit_text_field, open_url


WSA = get_webservices('agent')


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
    agent_id = find_agent_id_from_number(number)
    open_url('agent', 'editagent', {'group': '1', 'id': agent_id})
    current_password_item = world.browser.find_element_by_id('it-agentfeatures-passwd')
    return current_password_item.get_attribute('value')


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
    agent_id = find_agent_id_from_number(number)
    if agent_id is None:
        return
    if not WSA.delete(agent_id):
        raise Exception('Unable to delete agent %s' % agent_id)


def find_agent_id_from_number(number):
    agent_list = WSA.search(number)
    if agent_list is not None:
        for agent in agent_list:
            return agent['id']
    return None
