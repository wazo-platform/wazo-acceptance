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

from lettuce import step
from lettuce import world

from xivo_acceptance.lettuce import sysutils
from xivo_acceptance.lettuce import terrain


@step(u'I switch to the XiVO master')
def i_switch_to_the_xivo_master(step):
    terrain.set_xivo_target(extra_config='master')
    terrain._check_webi_login_root()


@step(u'I switch to the XiVO slave')
def i_switch_to_the_xivo_slave(step):
    terrain.set_xivo_target(extra_config='slave')
    terrain._check_webi_login_root()


@step(u'When I start the replication between master and slave')
def when_i_start_the_replication_between_master_and_slave(step):
    command = ['xivo-master-slave-db-replication', world.config['slave_host']]
    sysutils.send_command(command)
