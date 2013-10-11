# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from lettuce import step, world
from xivo_lettuce import common, form


@step(u'Given no config file "([^"]*)"')
def given_no_config_file_1(step, config_file_name):
    common.remove_element_if_exist('configfiles', config_file_name)


@step(u'When I create a configfiles "([^"]*)" with content "([^"]*)"')
def when_i_create_configfiles_with_content(step, filename, content):
    common.open_url('configfiles', 'add')
    input_filename = world.browser.find_element_by_id('it-configfile-filename')
    input_filename.clear()
    input_filename.send_keys(filename)
    input_description = world.browser.find_element_by_id('it-configfile-description')
    input_description.clear()
    input_description.send_keys(content)
    form.submit.submit_form()
