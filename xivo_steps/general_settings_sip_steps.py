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

from lettuce import step

from xivo_acceptance.helpers import asterisk_helper
from xivo_lettuce import form
from xivo_lettuce.form.checkbox import Checkbox
from xivo_lettuce.common import go_to_tab, open_url


@step(u'I go on the General Settings > SIP Protocol page, tab "([^"]*)"')
def i_go_on_the_general_settings_sip_protocol_page_tab(step, tab):
    open_url('general_sip')
    go_to_tab(tab)


@step(u'When I enable the "([^"]*)" option')
def when_i_enable_the_sip_encryption_option(step, label):
    option = _get_sip_option_from_label(label)
    option.check()
    form.submit.submit_form()


@step(u'When I disable the "([^"]*)" option')
def when_i_disable_the_sip_encryption_option(step, label):
    option = _get_sip_option_from_label(label)
    option.uncheck()
    form.submit.submit_form()


@step(u'^Then I should see "([^"]*)" to "([^"]*)" in "([^"]*)"$')
def then_i_see_sip_encryption_in_file(step, var_name, expected_var_val, file):
    var_val = asterisk_helper.get_asterisk_conf(file, var_name)
    assert(expected_var_val == var_val)


def _get_sip_option_from_label(label):
    option = Checkbox.from_label(label)
    return option
