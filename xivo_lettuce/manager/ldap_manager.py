
# -*- coding: utf-8 -*-

from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from xivo_lettuce.common import *


def type_ldap_name_and_host(name, host):
    input_name = world.browser.find_element_by_id('it-name', 'LDAP form  not loaded')
    input_host = world.browser.find_element_by_id('it-host', 'LDAP form  not loaded')
    input_name.send_keys(name)
    input_host.send_keys(host)
