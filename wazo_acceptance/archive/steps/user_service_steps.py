# -*- coding: utf-8 -*-
# Copyright (C) 2016 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later


from lettuce import step
from lettuce.registry import world

from xivo_acceptance.helpers import user_helper


@step(u'Given user "([^"]*)" has (enabled|disabled) "([^"]*)" service')
def given_user_has_service(step, fullname, enabled, service_name):
    user_uuid = user_helper.get_user_by_name(fullname)['uuid']
    service = {'enabled': enabled == 'enabled'}
    world.confd_client.users(user_uuid).update_service(service_name, service)
