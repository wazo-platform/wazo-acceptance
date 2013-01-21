# -*- coding: utf-8 -*-

from lettuce.registry import world
from xivo_lettuce import form
from xivo_lettuce.common import open_url
from xivo_lettuce.manager_ws import meetme_manager_ws

def create_meetme(meetme):
    meetme_manager_ws.delete_meetme_with_confno(meetme['number'])
    open_url('meetme', 'add')

    form.input.set_text_field_with_id('it-meetmefeatures-name', meetme['name'])
    form.input.set_text_field_with_id('it-meetmefeatures-confno', meetme['number'])

    if 'context' in meetme:
        form.select.set_select_field_with_id('it-meetmefeatures-maxusers', meetme['context'])

    if 'max users' in meetme:
        form.input.set_text_field_with_id('it-meetmefeatures-maxusers', meetme['max users'])

    form.submit.submit_form()

