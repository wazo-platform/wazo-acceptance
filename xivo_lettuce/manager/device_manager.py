# -*- coding: utf-8 -*-

from xivo_lettuce.common import open_url, remove_line
from xivo_lettuce import form
from selenium.common.exceptions import NoSuchElementException


def add_or_replace_device(info):
    delete_device(info)
    add_device(info)


def add_device(info):
    open_url('device', 'add')
    form.input.edit_text_field_with_id('it-devicefeatures-ip', info['ip'])
    form.input.edit_text_field_with_id('it-devicefeatures-mac', info['mac'])
    form.submit.submit_form()


def delete_device(info):
    search_device(info['mac'])
    try:
        remove_line(info['mac'])
    except NoSuchElementException:
        pass


def search_device(search):
    open_url('device')
    form.input.edit_text_field_with_id('it-toolbar-search', search)
    form.submit.submit_form('it-toolbar-subsearch')
