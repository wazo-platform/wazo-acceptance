# -*- coding: utf-8 -*-

import time
import json
from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException
from webservices.webservices import WebServicesFactory
from xivo_lettuce.common import *
from xivo_lettuce.manager.context_manager import *
from xivo_lettuce.manager.voicemail_manager import *
from xivo_lettuce.manager.user_manager import *

USER_URL = '/service/ipbx/index.php/pbx_settings/users/%s'
WSU = WebServicesFactory('ipbx/pbx_settings/users')


def open_import_user_form():
    URL = USER_URL % '?act=import'
    world.browser.get('%s%s' % (world.url, URL))
    world.browser.find_element_by_id('it-import', 'User import form not loaded')


def insert_simple_user(firtname, lastname, linenumber):
    check_context_number_in_interval('default', 'user', linenumber)
    data = get_utils_file_content('import_user.csv')
    data = data  % {
                    'entityid': 1,
                    'firstname': firtname,
                    'lastname': lastname,
                    'language': 'en_US',
                    'phonenumber': linenumber,
                    'context': 'default',
                    'protocol': 'sip',
                    'mobilephonenumber': '0033123456789'
                    }
    response = WSU.custom({'act': 'import'}, data)
    assert(response.code == 200)


def insert_adv_user_with_mevo(firtname, lastname, linenumber):
    check_context_number_in_interval('default', 'user', linenumber)
    delete_voicemail_from_number(linenumber)
    delete_user(firtname, lastname)
    data = get_utils_file_content('import_user_with_mevo.csv')
    data = data  % {
                    'entityid': 1,
                    'firstname': firtname,
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
    print 'url:', response.url, '- code:', response.code
    print '=================================================='
    print response.data
    print '=================================================='
    assert(response.code == 200)
