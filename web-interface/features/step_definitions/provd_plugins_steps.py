# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException

# original URL: http://provd.xivo.fr/plugins/1/stable/

PP_URL = '/xivo/configuration/index.php/provisioning/plugin/%s'


def _open_list_url():
    URL = PP_URL % ''
    world.browser.get('%s%s' % (world.url, URL))
    world.browser.find_element_by_id('table-main-listing', 'Plugin list page not loaded')


def _plugins_successfully_updated():
    try:
        div = world.browser.find_element_by_id('report-xivo-info')
        return div is not None
    except NoSuchElementException, ElementNotVisibleException:
        return False


def _plugins_error_during_update():
    try:
        div = world.browser.find_element_by_id('report-xivo-error')
        return div is not None
    except NoSuchElementException, ElementNotVisibleException:
        return False


@step(u'Given a update plugins provd with good url')
def given_a_update_plugins_provd(step):
    import provd_general_steps as provdg
    provdg.update_plugin_server_url('http://provd.xivo.fr/plugins/1/stable/')
    _open_list_url()
    world.browser.find_element_by_id('toolbar-bt-update').click()
    world.browser.find_element_by_xpath("//div[@class[contains(.,'xivo-messages')]]")


@step(u'Given a update plugins provd with bad url')
def given_a_update_plugins_provd_with_bad_url(step):
    import provd_general_steps as provdg
    provdg.update_plugin_server_url('http://provd.xivo.fr/plugins/1/lol/')
    _open_list_url()
    world.browser.find_element_by_id('toolbar-bt-update').click()
    world.browser.find_element_by_xpath("//div[@class[contains(.,'xivo-messages')]]")


@step(u'Then plugins list successfully updated')
def then_plugins_list_successfully_updated(step):
    assert _plugins_successfully_updated()


@step(u'Then plugins list has a error during update')
def then_plugins_list_has_error_during_update(step):
    assert _plugins_error_during_update()
    import provd_general_steps as provdg
    provdg.update_plugin_server_url('http://provd.xivo.fr/plugins/1/stable/')
