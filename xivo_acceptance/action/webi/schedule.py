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
from functools import wraps


def edit_schedule(fn):
    @wraps(fn)
    def _fn(schedule_name, *args, **kwargs):
        common.open_url('schedule')
        common.edit_line(schedule_name)
        fn(*args, **kwargs)
        form.submit.submit_form()
    return _fn


@edit_schedule
def remove_closed_schedule(schedule_index):
    common.go_to_tab('Closed hours')
    _remove('closed', schedule_index)


@edit_schedule
def remove_opened_schedule(schedule_index):
    _remove('opened', schedule_index)


def _remove(status, schedule_index):
    if status == 'closed':
        xpath = '''.//*[@id='disp2']/tr[%s]/td[3]/a'''
    else:
        xpath = '''.//*[@id='disp']/tr[%s]/td[2]/a'''

    delete_button = world.browser.find_element_by_xpath(xpath % schedule_index)
    delete_button.click()
