# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_acceptance.helpers import meetme_helper
from xivo_acceptance.lettuce import common, form


def add_or_replace_meetme(meetme):
    meetme_helper.delete_meetme_with_confno(meetme['number'])
    common.open_url('meetme', 'add')
    fill_form(meetme)
    form.submit.submit_form()


def update_meetme(meetme):
    common.open_url('meetme', 'list')
    common.edit_line(meetme['name'])
    fill_form(meetme)
    form.submit.submit_form()


def fill_form(meetme):
    form.input.set_text_field_with_id('it-meetmefeatures-name', meetme['name'])
    form.input.set_text_field_with_id('it-meetmefeatures-confno', meetme['number'])

    if 'context' in meetme:
        form.select.set_select_field_with_id_containing('it-meetmefeatures-context', meetme['context'])

    if 'max users' in meetme:
        form.input.set_text_field_with_id('it-meetmefeatures-maxusers', meetme['max users'])

    if 'pin code' in meetme:
        form.input.set_text_field_with_id('it-meetmeroom-pin', meetme['pin code'])
