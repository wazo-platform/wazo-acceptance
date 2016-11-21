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
from xivo_acceptance.action.webi import high_availability as high_availability_action


@step(u'I switch to the XiVO master')
def i_switch_to_the_xivo_master(step):
    terrain.set_xivo_target(extra_config='master')


@step(u'I switch to the XiVO slave')
def i_switch_to_the_xivo_slave(step):
    terrain.set_xivo_target(extra_config='slave')


@step(u'Given the HA is enabled as master')
def given_the_ha_is_enabled_as_master(step):
    high_availability_action.set_ha_config(
        mode='Master',
        remote=world.config['slave_host']
    )


@step(u'Given the HA is enabled as slave')
def given_the_ha_is_enabled_as_slave(step):
    high_availability_action.set_ha_config(
        mode='Slave',
        remote=world.config['master_host']
    )


@step(u'When I start the replication between master and slave')
def when_i_start_the_replication_between_master_and_slave(step):
    command = ['xivo-master-slave-db-replication', world.config['slave_host']]
    sysutils.send_command(command)


@step(u'When I disable the HA')
def when_i_disable_the_ha(step):
    high_availability_action.set_ha_config_ignore_errors(
        mode='Disabled'
    )


@step(u'When I enable the HA as master')
def when_i_enable_the_ha_as_master(step):
    high_availability_action.set_ha_config(
        mode='Master',
        remote=world.config['slave_host']
    )


@step(u'When I enable the HA as slave')
def when_i_enable_the_ha_as_slave(step):
    high_availability_action.set_ha_config(
        mode='Slave',
        remote=world.config['master_host']
    )
