# -*- coding: utf-8 -*-

# Copyright (C) 2013-2015 Avencall
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

from hamcrest import assert_that, is_in, equal_to

from xivo_acceptance.lettuce import postgres
from xivo_acceptance.action.confd import line_extension_collection_action_confd as collection_action
from xivo_acceptance.action.confd import user_line_action_confd as user_line_action
from xivo_acceptance.helpers import line_read_helper
from xivo_acceptance.helpers import line_sip_helper
from xivo_acceptance.helpers import line_sccp_helper
from xivo_acceptance.helpers import provd_helper


def add_line(parameters):
    line_params = _extract_line_params(parameters)
    line = line_sip_helper.create_line(line_params)
    _manage_device(line, parameters)


def _extract_line_params(parameters):
    parameters = dict(parameters)
    protocol = parameters.pop('protocol', 'sip')

    assert_that(protocol, equal_to("sip"),
                "Line helper can only create sip lines")

    for key in ['device_id', 'device_mac']:
        try:
            parameters.pop(key)
        except KeyError:
            pass

    if 'id' in parameters:
        parameters['id'] = int(parameters['id'])
    if 'device_slot' in parameters:
        parameters['device_slot'] = int(parameters['device_slot'])

    return parameters


def _manage_device(line, parameters):
    device_slot = int(parameters.get('device_slot', 1))

    if 'device_mac' in parameters:
        device = provd_helper.get_by_mac(parameters['device_mac'])
        _associate_device(line, device['mac'], device_slot)
    elif 'device_id' in parameters:
        _associate_device(line, parameters['device_id'], device_slot)


def _associate_device(line, device_id, device_slot):
    query = """
    UPDATE
        linefeatures
    SET
        device = :device_id,
        num = :device_slot
    WHERE
        id = :line_id
    """

    postgres.exec_sql_request(query,
                              line_id=line['id'],
                              device_id=device_id,
                              device_slot=device_slot)


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

    _delete_line_associations(line_id)
    _delete_line(line)


def _delete_line_associations(line_id):
    dissociate_device(line_id)
    dissociate_extensions(line_id)
    dissociate_users(line_id)


def dissociate_device(line_id):
    query = """
    UPDATE
        linefeatures
    SET
        device = NULL,
        num = 1
    WHERE
        id = :line_id
    """

    postgres.exec_sql_request(query, line_id=line_id)


def dissociate_extensions(line_id):
    response = collection_action.extensions_for_line(line_id)
    for line_extension in response.items():
        dissociation = collection_action.dissociate_extension(line_id,
                                                              line_extension['extension_id'])
        dissociation.check_status()


def dissociate_users(line_id):
    user_ids = _find_user_ids_for_line(line_id)
    for user_id in user_ids:
        response = user_line_action.delete_user_line(user_id, line_id)
        response.check_status()


def _find_user_ids_for_line(line_id):
    query = """
    SELECT
        user_line.user_id
    FROM
        user_line
    WHERE
        user_line.line_id = :line_id
    ORDER BY
        user_line.main_user ASC
    """

    result = postgres.exec_sql_request(query, line_id=line_id)
    return [row['user_id'] for row in result]


def _delete_line(line):
    if line['protocol'] == 'sccp':
        line_sccp_helper.delete_line(line['id'])
    elif line['protocol'] == 'sip':
        line_sip_helper.delete_line(line['id'])
