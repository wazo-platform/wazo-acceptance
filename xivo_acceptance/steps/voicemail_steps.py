# -*- coding: utf-8 -*-

# Copyright (C) 2013-2016 Avencall
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

from hamcrest import assert_that, has_entry, has_length
from lettuce import step, world

from xivo_acceptance.helpers import voicemail_helper
from xivo_acceptance.lettuce import common

FAKE_ID = 999999999


@step(u'Given I have the following voicemails:')
def given_have_the_following_voicemails(step):
    for row in step.hashes:
        voicemail_info = _extract_voicemail_info_to_confd(row)
        voicemail_helper.add_or_replace_voicemail(voicemail_info)


@step(u'Then I have a list with (\d+) results$')
def then_i_have_a_list_with_n_results(step, nb_list):
    nb_list = int(nb_list)
    assert_that(world.response.data, has_entry('items', has_length(nb_list)))


@step(u'Then I see the voicemail "([^"]*)" exists$')
def then_i_see_the_element_exists(step, name):
    common.open_url('voicemail')
    line = common.find_line(name)
    assert line is not None, 'voicemail: %s does not exist' % name


@step(u'Then I see the voicemail "([^"]*)" not exists$')
def then_i_see_the_element_not_exists(step, name):
    common.open_url('voicemail')
    line = common.find_line(name)
    assert line is None, 'voicemail: %s exist' % name


def _extract_voicemail_info_to_confd(row):
    voicemail = dict(row)

    if 'max_messages' in voicemail and voicemail['max_messages'] is not None and voicemail['max_messages'].isdigit():
        voicemail['max_messages'] = int(voicemail['max_messages'])

    for key in ['attach_audio', 'delete_messages', 'ask_password']:
        if key in voicemail:
            voicemail[key] = (voicemail[key] == 'true')

    return voicemail
