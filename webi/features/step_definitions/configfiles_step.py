# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world

from xivo_lettuce.common import *


@step(u'When I create a configfiles "([^"]*)" with content "([^"]*)"')
def when_i_create_configfiles_with_content(step, filename, content):
    open_url('configfiles', 'add')
    input_filename = world.browser.find_element_by_id('it-configfile-filename')
    input_filename.clear()
    input_filename.send_keys(filename)
    input_description = world.browser.find_element_by_id('it-configfile-description')
    input_description.clear()
    input_description.send_keys(content)
    submit_form()
