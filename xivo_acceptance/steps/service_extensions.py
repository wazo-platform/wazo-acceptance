# -*- coding: utf-8 -*-

# Copyright (C) 2014-2016 Avencall
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

from xivo_acceptance.lettuce import common
from xivo_acceptance.lettuce import form
from xivo_acceptance.lettuce.form.checkbox import Checkbox
from xivo_acceptance.lettuce.form.input import set_text_field_with_id

_EXTENSIONS = {
    'Enable forwarding on no-answer': {
        'tab': ['General', 'Forwards'],
        'checkbox_id': 'it-extenfeatures-enable-fwdrna',
        'text_id': 'it-extenfeatures-fwdrna',
    },
    'Enable forwarding on busy': {
        'tab': ['General', 'Forwards'],
        'checkbox_id': 'it-extenfeatures-enable-fwdbusy',
        'text_id': 'it-extenfeatures-fwdbusy',
    },
    'Enable unconditional forwarding': {
        'tab': ['General', 'Forwards'],
        'checkbox_id': 'it-extenfeatures-enable-fwdunc',
        'text_id': 'it-extenfeatures-fwdunc',
    },
    'Do not disturb': {
        'tab': ['General'],
        'checkbox_id': 'it-extenfeatures-enable-enablednd',
        'test_id': 'it-extenfeatures-enablednd',
    },
    'Incoming call filtering': {
        'tab': ['General'],
        'checkbox_id': 'it-extenfeatures-enable-incallfilter',
        'test_id': 'it-extenfeatures-incallfilter',
    },
}


@step(u'Given the "([^"]*)" extension is (disabled|enabled)')
def given_the_extension_is_disabled(step, exten_name, state):
    extension = _EXTENSIONS[exten_name]
    _open_url_and_go_to_tab(extension)
    if state == 'enabled':
        Checkbox.from_id(extension['checkbox_id']).check()
    else:
        Checkbox.from_id(extension['checkbox_id']).uncheck()
    form.submit.submit_form()


@step(u'Given the "([^"]*)" extension is set to "([^"]*)"')
def given_the_extension_is_set_to(step, exten_name, exten_value):
    extension = _EXTENSIONS[exten_name]
    _open_url_and_go_to_tab(extension)
    Checkbox.from_id(extension['checkbox_id']).check()
    set_text_field_with_id(extension['text_id'], exten_value)
    form.submit.submit_form()


def _open_url_and_go_to_tab(extension):
    common.open_url('extensions')
    common.go_to_tab(*extension['tab'])
