# -*- coding: utf-8 -*-
# Copyright (C) 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from lettuce import world

from hamcrest import assert_that
from hamcrest import is_not
from hamcrest import none
from requests.exceptions import HTTPError


def find_by_id(line_id):
    try:
        return get_by_id(line_id)
    except HTTPError:
        return None


def get_by_id(line_id):
    return world.confd_client.lines.get(line_id)


def find_with_exten_context(exten, context='default'):
    extensions = world.confd_client.extensions.list(exten=exten, context=context, recurse=True)['items']
    if not extensions or not extensions[0]['lines']:
        return None

    line_id = extensions[0]['lines'][0]['id']
    return world.confd_client.lines.get(line_id)


def get_with_exten_context(exten, context='default'):
    line = find_with_exten_context(exten, context)
    assert_that(line, is_not(none()),
                "line with extension %s@%s not found" % (exten, context))
    return line


def find_by_sip_username(username):
    endpoints_sip = world.confd_client.endpoints_sip.list(username=username)['items']
    if not endpoints_sip or not endpoints_sip[0]['line']:
        return None
    line_id = endpoints_sip[0]['line']['id']
    return world.confd_client.lines.get(line_id)
