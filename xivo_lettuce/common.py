# -*- coding: utf-8 -*-

import urllib
import subprocess
import os
import socket

from lettuce import before, after
from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from checkbox import Checkbox
from xivo_lettuce import urls
from webservices.webservices import WebServicesFactory

UTILS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils'))

class FormErrorException(Exception):
    pass


def run_xivoclient():
    xc_path = os.environ['XC_PATH'] + '/'
    env = os.environ
    env['LD_LIBRARY_PATH'] = '.'
    world.xc_process = subprocess.Popen('./xivoclient',
                                        cwd = xc_path,
                                        env = env)


def xivoclient_step(f):
    """Decorator that sends the function name to the XiVO Client."""
    def xivoclient_decorator(step, *kargs):
        world.xc_socket.send('%s,%s\n' % (f.__name__, ','.join(kargs)))
        world.xc_response = str(world.xc_socket.recv(1024))
        print 'XC response:', f.__name__, world.xc_response
        f(step, *kargs)
    return xivoclient_decorator


def xivoclient(f):
    """Decorator that sends the function name to the XiVO Client."""
    def xivoclient_decorator(*kargs):
        world.xc_socket.send('%s,%s\n' % (f.__name__, ','.join(kargs)))
        world.xc_response = str(world.xc_socket.recv(1024))
        print 'XC response:', f.__name__, world.xc_response
        f(*kargs)
    return xivoclient_decorator


@before.each_scenario
def setup_xivoclient_rc(scenario):
    world.xc_process = None
    world.xc_socket = socket.socket(socket.AF_UNIX)


@after.each_scenario
def clean_xivoclient_rc(scenario):
    if world.xc_process:
        world.xc_process.poll()
        if world.xc_process.returncode is None:
            i_stop_the_xivo_client()


@xivoclient
def i_stop_the_xivo_client():
    assert world.xc_response == "OK"


def get_utils_file_content(filename):
    abs_file_path = os.path.join(UTILS_DIR, filename);
    with open(abs_file_path) as fobj:
        filecontent = fobj.read()
    return filecontent


def webi_login(user, password, language):
    input_login = world.browser.find_element_by_id('it-login')
    input_password = world.browser.find_element_by_id('it-password')
    input_login.send_keys(user)
    input_password.send_keys(password)
    language_option = world.browser.find_element_by_xpath('//option[@value="%s"]' % language)
    language_option.click()
    submit_form()
    world.browser.find_element_by_id('loginbox', 'Cannot login as ' + user)


def waitForLoginPage():
    world.browser.find_element_by_id('it-login', 'login page not loaded', 30)


def the_option_is_checked(option_label, checkstate, **kwargs):
    """Reads or write the value of a checkbox, selected by its label text.
       Use given = True if you want to set the checkbox"""
    # If given, then we set the option.
    # If not given, we assert the option is in checkstate.
    if 'given' in kwargs:
        given = kwargs['given']
    else:
        given = False

    # Get the webelement.
    world.last_option_label = option_label
    option = world.browser.find_element_by_label(option_label)

    # Determine the action to do.
    goal_checked = (checkstate is None)
    if not given:
        assert Checkbox(option).is_checked() == goal_checked
    else:
        Checkbox(option).set_checked(goal_checked)


def find_form_errors():
    """Find the box containing form errors."""
    return world.browser.find_element_by_id('report-xivo-error')


def submit_form():
    """Every (?) submit button in the Webi has the same id."""
    submit_button = world.browser.find_element_by_id('it-submit')
    submit_button.click()
    try:
        error_element = find_form_errors()
    except NoSuchElementException:
        pass
    else:
        raise FormErrorException(error_element.text)


def get_webservices(module):
    return WebServicesFactory(urls.URLS[module]['ws'])


def element_is_in_list(type, search, qry={}):
    open_url(type, 'list', qry)
    try:
        find_line(search)
    except NoSuchElementException:
        return None
    return True


def element_is_not_in_list(type, search, qry={}):
    open_url(type, 'list', qry)
    try:
        find_line(search)
    except NoSuchElementException:
        return True
    return None


def open_url(module, act=None, qry={}):
    list_url = urls.URLS
    if act:
        qry.update({'act': act})
    if module in list_url:
        uri = list_url[module]['web']
    elif module in urls.ALIAS:
        module_alias = urls.ALIAS[module]['module']
        if 'qry' in urls.ALIAS[module]:
            qry.update(urls.ALIAS[module]['qry'])
        uri = list_url[module_alias]['web']

    qry_encode = urllib.urlencode(qry)
    url = '%s%s?%s' % (world.url, uri, qry_encode)
    world.browser.get(url)


def find_line(line_substring):
    """Return the tr webelement of a list table."""
    return world.browser.find_element_by_xpath(
        "//table[@id='table-main-listing']//tr[contains(.,'%s')]" % line_substring)


def remove_element_if_exist(module, search):
    open_url(module, 'list')
    try:
        remove_line(search)
    except NoSuchElementException, ElementNotVisibleException:
        pass


def remove_all_elements(module, search):
    open_url(module, 'list')
    try:
        while True:
            remove_line(search)
    except NoSuchElementException, ElementNotVisibleException:
        pass


def remove_line(line_substring):
    """Remove a line in a list table."""
    table_line = find_line(line_substring)
    delete_button = table_line.find_element_by_xpath(".//a[@title='Delete']")
    delete_button.click()
    alert = world.browser.switch_to_alert()
    alert.accept()


def edit_line(line_substring):
    """Edit an element of a list table."""
    table_line = find_line(line_substring)
    edit_button = table_line.find_element_by_xpath(".//a[@title='Edit']")
    edit_button.click()


def go_to_tab(tab_label):
    """Click a tab button."""
    tab_button = world.browser.find_element_by_xpath(
        "//div[@class='tab']//a[contains(.,'%s')]" % tab_label)
    tab_button.click()


def go_to_tab_href(tab_href):
    sb_menu = world.browser.find_element_by_class_name('sb-smenu')
    sb_part = sb_menu.find_element_by_xpath(".//li[contains(@onclick,'sb-part-%s')]" % (tab_href))
    href = sb_part.find_element_by_xpath(".//a[@href='#%s']" % (tab_href))
    href.click()


def get_host_address():
    host = world.host
    host = host.rstrip('/')
    host = host.partition('//')[2]
    return host

