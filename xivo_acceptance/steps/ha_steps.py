# -*- coding: utf-8 -*-

# Copyright (C) 2016 Avencall
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

from contextlib import contextmanager
from hamcrest import assert_that
from hamcrest import equal_to
from hamcrest import has_entries
from lettuce import step
from lettuce import world

from xivo_acceptance.action.webi import user as user_action_webi
from xivo_acceptance.helpers import user_line_extension_helper as ule_helper
from xivo_acceptance.helpers import user_helper
from xivo_acceptance.lettuce import common
from xivo_acceptance.lettuce import sysutils
from xivo_acceptance.lettuce import terrain


@contextmanager
def xivo_server_slave():
    terrain.initialize(extra_config='slave')
    terrain._check_webi_login_root()
    yield
    terrain.initialize(extra_config='default')


@contextmanager
def xivo_server_master():
    terrain.initialize(extra_config='master')
    terrain._check_webi_login_root()
    yield
    terrain.initialize(extra_config='default')


@step(u'Given there is no user on the slave "([^"]*)" "([^"]*)"$')
def given_there_is_no_user_on_the_slave(step, firstname, lastname):
    with xivo_server_slave():
        ule_helper.delete_user_line_extension_voicemail(firstname, lastname)


@step(u'Given there are users on the master with infos:$')
def given_there_are_users_on_the_master_with_infos(step):
    with xivo_server_master():
        for user_data in step.hashes:
            user_helper.add_user_with_infos(user_data, step=step)


@step(u'When I start the replication between master and slave')
def when_i_start_the_replication_between_master_and_slave(step):
    with xivo_server_master():
        command = ['xivo-master-slave-db-replication', world.config['slave_host']]
        sysutils.send_command(command)


@step(u'Then I see a user on the slave with infos:')
def then_i_see_a_user_on_the_slave_with_infos(step):
    with xivo_server_slave():
        user_expected_properties = step.hashes[0]
        fullname = user_expected_properties['fullname']
        common.open_url('user', 'search', {'search': '%s' % fullname})
        user_actual_properties = user_action_webi.get_user_list_entry(fullname)
        assert_that(fullname, equal_to(user_expected_properties['fullname']))
        assert_that(user_actual_properties, has_entries(user_expected_properties))
        common.open_url('user', 'search', {'search': ''})
