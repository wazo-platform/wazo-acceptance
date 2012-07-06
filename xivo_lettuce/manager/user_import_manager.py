# -*- coding: utf-8 -*-

from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException
from webservices.webservices import WebServicesFactory
from xivo_lettuce.common import *
from xivo_lettuce.manager.context_manager import *
from xivo_lettuce.manager.voicemail_manager import *
from xivo_lettuce.manager.user_manager import *
from xivo_lettuce.manager.line_manager import *
from xivo_lettuce.manager.incall_manager import *

USER_URL = '/service/ipbx/index.php/pbx_settings/users/%s'
WSU = WebServicesFactory('ipbx/pbx_settings/users')


def open_import_user_form():
    URL = USER_URL % '?act=import'
    world.browser.get('%s%s' % (world.host, URL))
    world.browser.find_element_by_id('it-import', 'User import form not loaded')


def insert_simple_user(firstname, lastname, linenumber):
    check_context_number_in_interval('default', 'user', linenumber)
    data = get_utils_file_content('import_user.csv')
    data = data  % {
                    'entityid': 1,
                    'firstname': firstname,
                    'lastname': lastname,
                    'language': 'en_US',
                    'phonenumber': linenumber,
                    'context': 'default',
                    'protocol': 'sip',
                    'mobilephonenumber': '0033123456789'
                    }
    response = WSU.custom({'act': 'import'}, data)
    assert(response.code == 200)


def insert_adv_user_with_mevo(firstname, lastname, linenumber):
    check_context_number_in_interval('default', 'user', linenumber)
    delete_voicemail_from_number(linenumber)
    delete_user(firstname, lastname)
    delete_line_from_number(linenumber)
    data = get_utils_file_content('import_user_with_mevo.csv')
    data = data  % {
                    'entityid': 1,
                    'firstname': firstname,
                    'lastname': lastname,
                    'language': 'en_US',
                    'phonenumber': linenumber,
                    'context': 'default',
                    'protocol': 'sip',
                    'mobilephonenumber': '0033123456789',
                    'mailbox_passwd': '1234',
                    'mailbox_mail': 'dev@avencall.com'
                    }
    response = WSU.custom({'act': 'import'}, data)
    assert(response.code == 200)


def insert_adv_user_with_incall(firstname, lastname, linenumber, incallexten):
    check_context_number_in_interval('default', 'user', linenumber)
    check_context_number_in_interval('from-extern', 'incall', incallexten)
    delete_voicemail_from_number(linenumber)
    delete_user(firstname, lastname)
    delete_line_from_number(linenumber)
    remove_incall_with_did(incallexten)
    data = get_utils_file_content('import_user_with_incall.csv')
    data = data  % {
                    'entityid': 1,
                    'firstname': firstname,
                    'lastname': lastname,
                    'language': 'en_US',
                    'phonenumber': linenumber,
                    'context': 'default',
                    'protocol': 'sip',
                    'mobilephonenumber': '0033123456789',
                    'incallexten': incallexten,
                    'incallcontext': 'from-extern'
                    }
    response = WSU.custom({'act': 'import'}, data)
    assert(response.code == 200)


def insert_adv_user_full_infos(firstname, lastname, linenumber, incallexten):
    check_context_number_in_interval('default', 'user', linenumber)
    check_context_number_in_interval('from-extern', 'incall', incallexten)
    delete_voicemail_from_number(linenumber)
    delete_line_from_number(linenumber)
    delete_user(firstname, lastname)
    remove_incall_with_did(incallexten)
    data = get_utils_file_content('import_user_full_infos.csv')
    data = data  % {
                    'entityid': 1,
                    'firstname': firstname,
                    'lastname': lastname,
                    'language': 'en_US',
                    'outcallerid': 'outcallerid',
                    'enableclient': True,
                    'username': 'username',
                    'password': 'password',
                    'profileclient': 'client',
                    'enablehint': True,
                    'agentnumber': '2000',
                    'mobilephonenumber': '0033123456789',
                    'bosssecretary': '',
                    'phonenumber': linenumber,
                    'context': 'default',
                    'protocol': 'sip',
                    'linename': '123456',
                    'linesecret': '654321',
                    'incallexten': incallexten,
                    'incallcontext': 'from-extern',
                    'mailbox_passwd': '1234',
                    'mailbox_mail': 'dev@avencall.com'
                    }
    response = WSU.custom({'act': 'import'}, data)
    assert(response.code == 200)
