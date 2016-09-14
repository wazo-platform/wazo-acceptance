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
from lettuce.registry import world

from xivo_acceptance.helpers import user_helper


@step(u'Given user "([^"]*)" has (enabled|disabled) "([^"]*)" service')
def given_user_has_service(step, fullname, enabled, service_name):
    user_uuid = user_helper.get_user_by_name(fullname)['uuid']
    service = {'enabled': enabled == 'enabled'}
    world.confd_client.users(user_uuid).update_service(service_name, service)