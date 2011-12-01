# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world

from common.common import *

@step(u'I go on the General Settings > IAX Protocol page, tab "([^"]*)"')
def i_go_on_the_general_settings_iax_protocol_page_tab(step, tab):
    world.browser.get(world.url + 'service/ipbx/index.php/general_settings/iax/')
    go_to_tab(tab)
