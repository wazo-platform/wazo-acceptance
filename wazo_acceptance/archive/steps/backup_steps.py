# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step, world


@step(u'Then executing "([^"]*)" should complete without errors')
def when_i_execute_without_error(step, command):
    world.ssh_client_xivo.call([command])
