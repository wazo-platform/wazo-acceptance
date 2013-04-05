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

from lettuce.registry import world
from xivo_lettuce import common
from xivo_lettuce import form


def remove_closed_schedule(name, order):
    common.open_url('schedule')
    common.edit_line(name)
    common.go_to_tab('Closed hours')
    _remove_closed_schedule(order)
    form.submit.submit_form()


def _remove_closed_schedule(order):
    delete_button = world.browser.find_element_by_xpath('''.//*[@id='disp2']/tr[%s]/td[3]/a''' % order)
    delete_button.click()
