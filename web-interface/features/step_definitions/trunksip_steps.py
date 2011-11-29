# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world

from common.common import *
from ipbx_objects.user_manager import *

TRUNKSIP_URL = 'service/ipbx/index.php/trunk_management/sip/%s'

def _open_add_trunksip_url():
    URL = TRUNKSIP_URL % '?act=add'
    world.browser.get('%s%s' % (world.url, URL))

def _open_list_trunksip_url():
    URL = TRUNKSIP_URL % ('?act=list')
    world.browser.get('%s%s' % (world.url, URL))

@step(u'Given there is a SIP trunk "([^"]*)"')
def given_there_is_a_sip_trunk(step, name):
    _open_list_trunksip_url()
    try:
        find_line(name)
    except NoSuchElementException:
        _open_add_trunksip_url()
        input_name = world.browser.find_element_by_id('it-protocol-name', 'SIP trunk form not loaded')
        input_name.send_keys(name)
        submit_form()
