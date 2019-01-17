# -*- coding: utf-8 -*-
# Copyright (C) 2016 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later


from lettuce import step
from lettuce.registry import world

from xivo_acceptance.helpers import user_helper


@step(u'Given user "([^"]*)" has (enabled|disabled) "([^"]*)" forward to "([^"]*)"')
def given_user_has_forward_to(step, fullname, enabled, forward_name, destination):
    user_uuid = user_helper.get_user_by_name(fullname)['uuid']
    forward = {'enabled': enabled == 'enabled', 'destination': destination}
    world.confd_client.users(user_uuid).update_forward(forward_name, forward)
