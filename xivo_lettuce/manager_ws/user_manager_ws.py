# -*- coding: utf-8 -*-

import json
import voicemail_manager_ws
from lettuce.registry import world
from xivo_lettuce.common import get_webservices


WSU = get_webservices('user')
WSG = get_webservices('group')


def _fill_json_user_data(jsoncontent, data_dict):
    if 'firstname' not in data_dict:
        data_dict['firstname'] = 'firstname'
    if 'lastname' not in data_dict:
        data_dict['lastname'] = 'lastname'
    if 'agentid' not in data_dict:
        data_dict['agentid'] = ''

    return jsoncontent % data_dict


def add_user_with_no_line(firstname, lastname, agentid=''):
    jsoncontent = WSU.get_json_file_content('user')
    data_dict = {'firstname': firstname,
                 'lastname': lastname,
                 'agentid': agentid}
    datajson = _fill_json_user_data(jsoncontent, data_dict)
    data = json.loads(datajson)
    WSU.add(data)


def add_user(firstname, lastname, agentid=''):
    jsoncontent = WSU.get_json_file_content('userwithline')
    data_dict = {'firstname': firstname,
                 'lastname': lastname,
                 'agentid': agentid}
    datajson = _fill_json_user_data(jsoncontent, data_dict)
    data = json.loads(datajson)
    WSU.add(data)


def delete_user_with_firstname_lastname(firstname, lastname):
    users = world.ws.user.search('%s %s' % (firstname, lastname))
    for user in users:
        if user.voicemail:
            voicemail_manager_ws.delete_voicemail_with_id(user.voicemail.id)
        world.ws.user.delete(user.id)


def find_user_id_with_firstname_lastname(firstname, lastname):
    user_list = WSU.list()
    if user_list:
        return [userinfo['id'] for userinfo in user_list if
                userinfo['firstname'] == firstname and userinfo['lastname'] == lastname]
    return []


def user_id_is_in_group_name(group_name, user_id):
    group_list = WSG.list()
    group_id = [group['id'] for group in group_list if group['name'] == group_name]
    if len(group_id) > 0:
        group_view = WSG.view(group_id[0])
        for user in group_view['user']:
            if user['userid'] == user_id:
                return True
    return False
