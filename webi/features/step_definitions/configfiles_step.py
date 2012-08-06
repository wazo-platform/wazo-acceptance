# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world
from xivo_lettuce.common import open_url, submit_form, remove_element_if_exist


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


@step(u'Given no config file "([^"]*)"')
def given_no_config_file_1(step, config_file_name):
    remove_element_if_exist('configfiles', config_file_name)
