# -*- coding: utf-8 -*-
# Copyright 2016-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step
from lettuce import world

from xivo_acceptance.lettuce import sysutils
from xivo_acceptance.lettuce import terrain


@step(u'When I start the replication between master and slave')
def when_i_start_the_replication_between_master_and_slave(step):
    command = ['xivo-master-slave-db-replication', world.config['slave_host']]
    sysutils.send_command(command)
