# -*- coding: utf-8 -*-

# Copyright (C) 2014 Avencall
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

from lettuce import step

from xivo_lettuce import common
from xivo_lettuce import form
from xivo_lettuce.form.checkbox import Checkbox

_exten_url_map = {
    'Enable forwarding on no-answer': 'forward_extension',
    'Enable forwarding on busy': 'forward_extension',
}


@step(u'Given the "([^"]*)" extension is "([^"]*)"')
def given_the_extension_is_enabled_disabled(step, exten_name, enabled_disabled):
    enabled = enabled_disabled == 'enabled'
    _set_exten(exten_name, enabled)


def _set_exten(exten_name, enabled):
    common.open_url(_exten_url_map[exten_name])
    Checkbox.from_label(exten_name).set_checked(enabled)
    form.submit.submit_form()
