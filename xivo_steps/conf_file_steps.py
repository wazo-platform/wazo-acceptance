# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
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

from hamcrest import *
from itertools import ifilter
from lettuce.decorators import step

from xivo_acceptance.helpers import user_helper, asterisk_helper
from xivo_lettuce import sysutils


@step(u'Then cti configuration file correctly generated')
def then_cti_configuration_file_correctly_generated(step):
    CTI_INI_FILE = '/etc/pf-xivo/xivo-web-interface/cti.ini'
    CTI_INI_CONTENT_RESULT = """\
[general]
datastorage = "postgresql://xivo:proformatique@localhost/xivo?charset=utf8"

[queuelogger]
datastorage = "postgresql://asterisk:proformatique@localhost/asterisk?charset=utf8"
"""
    cti_ini_content = sysutils.get_content_file(CTI_INI_FILE)
    assert cti_ini_content == CTI_INI_CONTENT_RESULT


@step(u'Then the sccp.conf file should contain "([^"]*)" function keys for "([^"]*)" "([^"]*)" sorted by key number')
def then_the_sccp_conf_file_should_contain_function_keys_sorted_by_key_number(step, count, firstname, lastname):
    user_id = user_helper.find_user_id_with_firstname_lastname(firstname, lastname)
    expected_speeddials = ['speeddial = %s-%s' % (user_id, n) for n in xrange(1, int(count) + 1)]
    sccp_conf_content = asterisk_helper.get_confgen_file('sccp.conf')
    pattern = 'speeddial = %s-' % user_id
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
