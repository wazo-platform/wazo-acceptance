# -*- coding: utf-8 -*-

from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from webservices.webservices import WebServicesFactory
from xivo_lettuce.common import *


# original URL: http://provd.xivo.fr/plugins/1/stable/
PP_URL = '/xivo/configuration/index.php/provisioning/plugin/%s'


def open_provd_plugin_list_url():
    URL = PP_URL % ''
    world.browser.get('%s%s' % (world.url, URL))
    world.browser.find_element_by_id('table-main-listing', 'Plugin list page not loaded')


def plugins_successfully_updated():
    try:
        div = world.browser.find_element_by_id('report-xivo-info')
        return div is not None
    except NoSuchElementException, ElementNotVisibleException:
        return False


def plugins_error_during_update():
    try:
        div = world.browser.find_element_by_id('report-xivo-error')
        return div is not None
    except NoSuchElementException, ElementNotVisibleException:
        return False
