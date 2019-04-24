# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, is_not, none
from lettuce import step, world


@step(u'Then server has uuid')
def then_server_has_uuid(step):
    assert_that(world.confd_client.infos.get()['uuid'], is_not(none()))
