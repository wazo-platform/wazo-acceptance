# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0+

from hamcrest import assert_that, is_in, equal_to

from lettuce import world
from requests.exceptions import HTTPError

from xivo_acceptance.helpers import line_read_helper
from xivo_acceptance.helpers import line_sccp_helper


def add_line(parameters):
    line_params = _extract_line_params(parameters)
    endpoint_sip = world.confd_client.endpoints_sip.create(line_params)
    line = world.confd_client.lines.create(line_params)
    world.confd_client.lines(line).add_endpoint_sip(endpoint_sip)


def _extract_line_params(parameters):
    parameters = dict(parameters)
    protocol = parameters.pop('protocol', 'sip')

    assert_that(protocol, equal_to("sip"),
                "Line helper can only create sip lines")

    if 'device_slot' in parameters:
        parameters['position'] = int(parameters['device_slot'])

    return parameters


def delete_similar_lines(exten):
    line_ids = line_sccp_helper.find_all_line_ids_by_exten(exten)
    for line_id in line_ids:
        delete_line(line_id)


def delete_line(line_id):
    line = line_read_helper.find_by_id(line_id)
    if not line:
        return

    assert_that(line['protocol'], is_in(['sip', 'sccp']),
                "Acceptance cannot delete line with protocol '%s'" % line['protocol'])

    _delete_line_associations(line)
    _delete_line(line)


def _delete_line_associations(line):
    dissociate_device(line)
    dissociate_extensions(line)
    dissociate_users(line)


def dissociate_device(line):
    if not line['device_id']:
        return

    try:
        world.confd_client.lines(line).remove_device(line['device_id'])
    except HTTPError:
        pass


def dissociate_extensions(line):
    for extension in line['extensions']:
        world.confd_client.lines(line).remove_extension(extension)


def dissociate_users(line):
    for user in line['users']:
        world.confd_client.users(user['uuid']).remove_line(line)


def _delete_line(line):
    if line['protocol'] == 'sccp':
        line_sccp_helper.delete_line(line['id'])
    elif line['protocol'] == 'sip':
        if line['endpoint_sip']:
            world.confd_client.endpoints_sip.delete(line['endpoint_sip']['id'])
        world.confd_client.lines.delete(line['id'])
