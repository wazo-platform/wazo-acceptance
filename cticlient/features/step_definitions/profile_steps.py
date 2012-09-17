# -*- coding: utf-8 -*-

from lettuce import step
from xivo_lettuce.common import open_url
from xivo_lettuce.manager.profile_manager import remove_all_services, add_xlet, \
    delete_profile
from selenium.common.exceptions import NoSuchElementException


@step(u'Given there is no profile "([^"]*)"')
def given_there_is_no_profile_1(step, profile_label):
    try:
        delete_profile(profile_label)
    except NoSuchElementException:
        pass


@step(u'Given I add a profile')
def given_i_add_a_profile(step):
    open_url('profile', 'add')


@step(u'Given I remove all services')
def given_i_remove_all_services(step):
    remove_all_services()


@step(u'Given I add a XLet "([^"]*)"')
def given_i_add_a_xlet_1(step, xlet_label):
    add_xlet(xlet_label)
