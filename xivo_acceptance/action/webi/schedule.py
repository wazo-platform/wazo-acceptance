# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0+

from lettuce.registry import world
from xivo_acceptance.lettuce import common
from xivo_acceptance.lettuce import form
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
