# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import re

from lettuce import step, world

from xivo_acceptance.helpers import line_read_helper
from xivo_acceptance.helpers import line_write_helper
from xivo_acceptance.helpers import sip_config
from xivo_acceptance.helpers import sip_phone


@step(u'Given there are no custom lines with interface beginning with "([^"]*)"')
def given_there_are_no_custom_lines_with_interface_beginning_with_1(step, interface_start):
    pass


@step(u'Given there are no SIP lines with username "([^"]*)"')
def given_there_are_no_sip_lines_with_infos(step, username):
    endpoints_sip = world.confd_client.endpoints_sip.list(username=username)['items']
    for endpoint_sip in endpoints_sip:
        world.confd_client.endpoints_sip.delete(endpoint_sip['id'])


@step(u'(?:Given|When) I set the following options in line "(\d+)@(\w+)":')
def given_i_set_the_following_options_in_line_1(step, line_number, line_context):
    pass


@step(u'Given the line "(\d+)@(\w+)" is disabled')
def given_the_line_group1_is_disabled(step, extension, context):
    pass


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


@step(u'When I customize line "([^"]*)" codecs to:')
def when_i_customize_line_codecs_to(step, number):
    pass


@step(u'When I disable line codecs customization for line "([^"]*)"')
def when_i_disable_line_codecs_customization_for_line(step, number):
    pass


@step(u'When I add a SIP line with infos:')
def when_i_add_a_sip_line_with_infos(step):
    pass


@step(u'When I add a custom line with infos:')
def when_i_add_a_custom_line(step):
    pass


@step(u'When I disable custom codecs for this line')
def when_i_disable_custom_codecs_for_this_line(step):
    pass


@step(u'When I remove this line')
def when_i_remove_this_line(step):
    pass


@step(u'When I edit the line "([^"]*)"')
def when_i_edit_the_line_1(step, linenumber):
    pass


@step(u'Then I see a line with infos:')
def then_i_see_a_line_with_infos(step):
    pass


def check_codec_for_sip_line(peer, codec):
    command = ['asterisk', '-rx', '"pjsip show endpoint %s"' % peer]
    output = world.ssh_client_xivo.out_call(command)
    codec_line = [x for x in output.split("\n") if 'allow' in x][0]
    codec_list = re.match(r"\s+allow\s+:\s+\(([\w\|]*?)\)", codec_line).group(1).split('|')
    return codec in codec_list


@step(u'Then the codec "([^"]*)" appears after typing \'sip show peer\' in asterisk')
def then_the_codec_appears_after_typing_sip_show_peer_in_asterisk(step, codec):
    assert check_codec_for_sip_line(world.id, codec) is True


@step(u'Then the codec "([^"]*)" does not appear after typing \'sip show peer\' in asterisk')
def then_the_codec_does_not_appear_after_typing_sip_show_peer_in_asterisk(step, codec):
    assert check_codec_for_sip_line(world.id, codec) is False


@step(u'Then this line is displayed in the list')
def then_this_line_is_displayed_in_the_list(step):
    pass


@step(u'Then this line is not displayed in the list')
def then_this_line_is_not_displayed_in_the_list(step):
    pass


@step(u'Then I see the line "([^"]*)" exists$')
def then_i_see_the_element_exists(step, name):
    pass


@step(u'Then I see the line "([^"]*)" not exists$')
def then_i_see_the_element_not_exists(step, name):
    pass
