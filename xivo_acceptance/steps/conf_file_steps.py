# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from itertools import ifilter

from hamcrest import assert_that, contains
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
