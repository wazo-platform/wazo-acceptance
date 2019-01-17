# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

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
