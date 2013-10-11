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

from xivo_acceptance.helpers import meetme_helper
from xivo_lettuce import common, form


def create_meetme(meetme):
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
        form.select.set_select_field_with_id('it-meetmefeatures-maxusers', meetme['context'])

    if 'max users' in meetme:
        form.input.set_text_field_with_id('it-meetmefeatures-maxusers', meetme['max users'])

    if 'pin code' in meetme:
        form.input.set_text_field_with_id('it-meetmeroom-pin', meetme['pin code'])
