# -*- coding: utf-8 -*-

import time
import json
from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException
from webservices.webservices import WebServicesFactory
from xivo_lettuce.common import *

USER_URL = '/service/ipbx/index.php/pbx_settings/users/%s'
WSU = WebServicesFactory('ipbx/pbx_settings/users')
WSG = WebServicesFactory('ipbx/pbx_settings/groups')


def open_add_user_form():
    URL = USER_URL % '?act=add'
    world.browser.get('%s%s' % (world.url, URL))
    world.browser.find_element_by_id('it-userfeatures-firstname', 'User add form not loaded')


def open_edit_user_form(id):
    URL = USER_URL % '?act=edit&id=%d'
    world.browser.get('%s%s' % (world.url, URL % id))
    world.browser.find_element_by_id('it-userfeatures-firstname', 'User edit form not loaded')


def open_list_user_url():
    URL = USER_URL % '?act=list'
    world.browser.get('%s%s' % (world.url, URL))
    world.browser.find_element_by_id('table-main-listing', 'User list not loaded')


def type_user_names(firstName, lastName):
    world.browser.find_element_by_id('it-userfeatures-firstname', 'User form not loaded')
    input_firstName = world.browser.find_element_by_id('it-userfeatures-firstname')
    input_lastName = world.browser.find_element_by_id('it-userfeatures-lastname')
    input_firstName.clear()
    input_firstName.send_keys(firstName)
    input_lastName.clear()
    input_lastName.send_keys(lastName)


def type_user_in_group(groupName):
    group = world.browser.find_element_by_xpath("//li[@id='dwsm-tab-7']//a[@href='#groups']")
    group.click()
    world.browser.find_element_by_id('sb-part-groups', 'Group tab not loaded')
    select_group = world.browser.find_element_by_xpath('//select[@id="it-grouplist"]//option[@value="%s"]' % groupName)
    select_group.click()
    add_button = world.browser.find_element_by_id('bt-ingroup')
    add_button.click()


def user_is_saved(firstname, lastname):
    open_list_user_url()
    try:
        user = world.browser.find_element_by_xpath("//table[@id='table-main-listing']//tr[contains(.,'%s %s')]" % (firstname, lastname))
        return user is not None
    except NoSuchElementException:
        return False


def insert_user(firstname, lastname):
    jsoncontent = WSU.get_json_file_content('userwithline')
    datajson = jsoncontent  % {'firstname': firstname,
                                         'lastname': lastname}
    data = json.loads(datajson)
    WSU.add(data)


def delete_user(firstname, lastname):
    for id in find_user_id(firstname, lastname):
        WSU.delete(id)


def delete_all_users():
    WSU.clear()


def find_user_id(firstname, lastname):
    user_list = WSU.list()
    if user_list:
        return [userinfo['id'] for userinfo in user_list if
                userinfo['firstname'] == firstname and userinfo['lastname'] == lastname]
    return []


def is_in_group(group_name, user_id):
    group_list = WSG.list()
    group_id = [group['id'] for group in group_list if group['name'] == group_name]
    if len(group_id) > 0:
        group_view = WSG.view(group_id[0])
        for user in group_view['user']:
            if user['userid'] == user_id:
                return True
    return False


def insert_group_with_user(group_name, user_list=[]):
    data = WSG.get_json_file_content('group')
    users = ""
    if len(user_list) > 0:
        users = r', "user": [%s]' % ', '.join(['"%s"' % str(id) for id in user_list])
    data = data % {'user_list': users,
                   'groupname': group_name}
    data = json.loads(data)
    WSG.clear()
    WSG.add(data)


def user_form_add_line(linenumber):
    go_to_tab('Lines')
    add_button = world.browser.find_element_by_id('lnk-add-row')
    add_button.click()
    input_linenumber = world.browser.find_elements_by_id('linefeatures-number')[-2]
    input_linenumber.send_keys(linenumber)
    go_to_tab('General')
