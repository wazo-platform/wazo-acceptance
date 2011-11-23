# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world

# To be made more reusable...
@step(u'I go on the General Settings > IAX Protocol page, tab Advanced')
def i_go_on_the_general_settings_iax_protocol_page_tab_advanced(step):
    world.browser.get(world.url + 'service/ipbx/index.php/general_settings/iax/#advanced')
