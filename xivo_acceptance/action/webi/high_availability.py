# -*- coding: utf-8 -*-

# Copyright (C) 2016 Proformatique Inc.
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

from xivo_acceptance.lettuce import common
from xivo_acceptance.lettuce.form import submit, input, select


def set_ha_config(mode, remote=None):
    common.open_url('ha')
    type_ha_config(mode, remote)
    submit.submit_form()


def set_ha_config_ignore_errors(mode, remote=None):
    common.open_url('ha')
    type_ha_config(mode, remote)
    submit.submit_form_ignore_errors()


def type_ha_config(mode, remote=None):
    select.set_select_field_with_label("Type of this node", mode)
    if remote:
        input.set_text_field_with_label("Remote address", remote)
