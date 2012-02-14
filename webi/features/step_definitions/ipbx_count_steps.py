# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world
from xivo_lettuce.manager.trunksip_manager import *

IPBX_COUNT_URL = '/service/ipbx/index.php'
SIP_TRUNK_STAT_XPATH = "//div[@id='ipbx-stats']//tr[8]//td[%d]"

ENABLED_INDEX = 2
DISABLED_INDEX = 3
TOTAL_INDEX = 4


def _open_ipbx_count_url():
    world.browser.get('%s%s' % (world.url, IPBX_COUNT_URL))

def _sip_trunk_enabled_xpath():
    return SIP_TRUNK_STAT_XPATH % ENABLED_INDEX

def _sip_trunk_disabled_xpath():
    return SIP_TRUNK_STAT_XPATH % DISABLED_INDEX

def _sip_trunk_total_xpath():
    return SIP_TRUNK_STAT_XPATH % TOTAL_INDEX

def _get_enabled_sip_trunk_count():
    element = world.browser.find_element_by_xpath(_sip_trunk_enabled_xpath())
    return int(element.text)

def _get_disabled_sip_trunk_count():
    element = world.browser.find_element_by_xpath(_sip_trunk_disabled_xpath())
    return int(element.text)

def _get_total_sip_trunk_count():
    element = world.browser.find_element_by_xpath(_sip_trunk_total_xpath())
    return int(element.text)

@step (u'Given I have (\d+) enabled trunk')
def given_i_have_trunk(step, count):
    for i in range(int(count)):
        add_trunksip('trunk_%s' % i)

@step (u'When I open the ibpx count page')
def when_i_open_the_ipbx_count_page(step):
    _open_ipbx_count_url()

@step (u'Then I should have (\d+) ([a-z]+) sip trunk')
def then_i_should_have_enable_sip_trunk(step, count, status):
    if status == 'enabled':
        assert (int(count) == _get_enabled_sip_trunk_count())
    elif status == 'disabled':
        assert (int(count) == _get_disabled_sip_trunk_count())
    else:
        assert(False)

@step (u'Then I should have (\d+) sip trunk')
def then_i_should_have_x_sip_trunk(step, count):
    assert(int(count) == _get_total_sip_trunk_count())
