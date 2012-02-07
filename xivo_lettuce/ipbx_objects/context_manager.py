# -*- coding: utf-8 -*-

import json
from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException
from webservices.webservices import WebServicesFactory

CONTEXT_URL = '/service/ipbx/index.php/system_management/context/%s'
WSCTX = WebServicesFactory('context')

def open_add_context_form():
    URL = CONTEXT_URL % '?act=add'
    world.browser.get('%s%s' % (world.url, URL))
    world.browser.find_element_by_id('it-context-name', 'context add form not loaded')


def open_edit_context_form(id):
    URL = CONTEXT_URL % '?act=edit&id=%d'
    world.browser.get('%s%s' % (world.url, URL % id))
    world.browser.find_element_by_id('it-context-namee', 'context edit form not loaded')


def open_list_context_url():
    URL = CONTEXT_URL % '?act=list'
    world.browser.get('%s%s' % (world.url, URL))
    world.browser.find_element_by_id('table-main-listing', 'context list not loaded')


def delete_context(name):
    WSCTX.delete(name)


def delete_all_contexts():
    WSCTX.clear()


def _add_incall_context(name, displayname, numberbeg, numberend, didlength):
    contextnumbers_incall = '"incall": [{"numberbeg": "%s", "numberend": "%s", didlength: "%s"}]' % (numberbeg, numberend, didlength)
    return _add_context(name, displayname, 'internal', contextnumbers_incall)


def _add_context(name, displayname, contexttype, 
                 contextnumbers_user='', 
                 contextnumbers_group='', 
                 contextnumbers_meetme='', 
                 contextnumbers_queue='', 
                 contextnumbers_incall=''):
    var_context = {
                  "name": name,
                  "displayname" : displayname,
                  "entity" : 'avencall',
                  "contexttype": contexttype,
                  "contextinclude": '[]',
                  "contextnumbers_user": '',
                  "contextnumbers_group": '',
                  "contextnumbers_meetme": '',
                  "contextnumbers_queue": '',
                  "contextnumbers_incall": ''
                  }
    
    # '"user": [{"numberbeg": "600", "numberend": "699"}]'
    if contextnumbers_user:
        var_context["contextnumbers_user"] = contextnumbers_user 
    if contextnumbers_group:
        var_context["contextnumbers_group"] = contextnumbers_group 
    if contextnumbers_meetme:
        var_context["contextnumbers_meetme"] = contextnumbers_meetme 
    if contextnumbers_queue:
        var_context["contextnumbers_queue"] = contextnumbers_queue 
    if contextnumbers_incall:
        var_context["contextnumbers_incall"] = contextnumbers_incall 
    
    jsonfilecontent = WSCTX.get_json_file_content('context');
    jsonstr = jsonfilecontent % (var_context)
    content = json.loads(jsonstr)

    response = WSCTX.add(content)
    return (response.code == 200)

