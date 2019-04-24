# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step, world

from xivo_acceptance.helpers import line_read_helper
from xivo_acceptance.helpers import line_write_helper
from xivo_acceptance.helpers import sip_config
from xivo_acceptance.helpers import sip_phone


@step(u'Given there are no SIP lines with username "([^"]*)"')
def given_there_are_no_sip_lines_with_infos(step, username):
    endpoints_sip = world.confd_client.endpoints_sip.list(username=username)['items']
    for endpoint_sip in endpoints_sip:
        world.confd_client.endpoints_sip.delete(endpoint_sip['id'])


@step(u'Given I have the following lines:')
def given_i_have_the_following_lines(step):
    for lineinfo in step.hashes:
        _delete_line(lineinfo)
        line_write_helper.add_line(lineinfo)


def _delete_line(lineinfo):
    if 'id' in lineinfo:
        line_write_helper.delete_line(int(lineinfo['id']))
    if 'username' in lineinfo:
        line = line_read_helper.find_by_sip_username(lineinfo['username'])
        if line:
            line_write_helper.delete_line(line['id'])


@step(u'Given a softphone is registered on SIP line "([^"]*)"')
def given_softphone_is_registered_on_sip_line(step, name):
    lines = world.confd_client.lines.list(name=name)
    line = [line for line in lines['items'] if line['name'] == name][0]
    line_endpoint = world.confd_client.lines(line['id']).get_endpoint_sip()
    endpoint = world.confd_client.endpoints_sip.get(line_endpoint['endpoint_id'])

    phone_config = sip_config.create_config(world.config, step.scenario.phone_register, endpoint)
    phone = sip_phone.register_line(phone_config)
    if phone:
        step.scenario.phone_register.add_registered_phone(phone, name)
