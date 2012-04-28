# -*- coding: utf-8 -*-

import json
from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException
from xivo_lettuce.common import *

WSA = get_webservices('agent')


def insert_agent(firstname, lastname, number, passwd):
    jsoncontent = WSA.get_json_file_content('agent')
    datajson = jsoncontent  % {
                               'firstname': firstname,
                               'lastname': lastname,
                               'number': number,
                               'passwd': passwd,
                               'userlist': ', "user-select" : []'
                               }
    data = json.loads(datajson)
    WSA.add(data)


def delete_agent(number):
    for id in find_agent_id_from_number(number):
        WSA.delete(id)


def find_agent_id_from_number(number):
    query = {'number': number}
    agent_list = WSA.search(query)
    if agent_list:
        return agent_list
    else:
        return []
