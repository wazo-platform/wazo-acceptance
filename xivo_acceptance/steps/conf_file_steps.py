# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, contains_string, contains, is_not
from itertools import ifilter
from lettuce.decorators import step

from xivo_acceptance.helpers import user_helper, asterisk_helper


@step(u'Then the sccp.conf file should contain "([^"]*)" function keys for "([^"]*)" "([^"]*)" sorted by key number')
def then_the_sccp_conf_file_should_contain_function_keys_sorted_by_key_number(step, count, firstname, lastname):
    user = user_helper.get_by_firstname_lastname(firstname, lastname)
    expected_speeddials = ['speeddial = %s-%s' % (user['id'], n) for n in xrange(1, int(count) + 1)]
    sccp_conf_content = asterisk_helper.get_confgen_file('sccp.conf')
    pattern = 'speeddial = %s-' % user['id']
    users_speeddial = ifilter(lambda line: pattern in line, sccp_conf_content.split('\n'))
    assert_that(users_speeddial, contains(*expected_speeddials), 'Configured speeddials')


@step(u'Then the "([^"]*)" file should contain peer "([^"]*)"')
def then_the_conf_file_should_contain_peer(step, file_name, peer_name):
    pattern = u'[%s]' % peer_name
    file_content = asterisk_helper.get_confgen_file(file_name)
    assert_that(file_content, contains_string(pattern))


@step(u'Then the "([^"]*)" file should not contain peer "([^"]*)"')
def then_the_conf_file_should_not_contain_peer(step, file_name, peer_name):
    pattern = u'[%s]' % peer_name
    file_content = asterisk_helper.get_confgen_file(file_name)
    assert_that(file_content, is_not(contains_string(pattern)))
