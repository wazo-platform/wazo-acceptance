# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
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

from lettuce import world
from xivo_acceptance.lettuce import assets
from xivo_acceptance.lettuce.form.checkbox import Checkbox
from xivo_acceptance.lettuce.form import input


def type_file_name(file_name):
    input.set_text_field_with_id('it-configfile-filename', file_name)


def type_file_content(content):
    input.set_text_field_with_id('it-configfile-description', content)


def type_reload_dialplan(reload_dialplan):
    input_reload_dialplan = Checkbox(world.browser.find_element_by_id('it-configfile-reload-dialplan'))
    input_reload_dialplan.set_checked(reload_dialplan)


def type_file_to_import(file_name):
    input_file_name = world.browser.find_element_by_id('it-import')
    asset_full_path = assets.full_path(file_name)
    input_file_name.send_keys(asset_full_path)
