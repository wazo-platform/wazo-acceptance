# -*- coding: utf-8 -*-

from lettuce.registry import world


USER_URL = '/service/ipbx/index.php/pbx_settings/users/%s'


def open_import_user_form():
    URL = USER_URL % '?act=import'
    world.browser.get('%s%s' % (world.host, URL))
    world.browser.find_element_by_id('it-import', 'User import form not loaded')
