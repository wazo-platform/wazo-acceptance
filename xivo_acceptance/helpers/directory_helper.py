# -*- coding: utf-8 -*-

# Copyright 2014-2016 The Wazo Authors  (see the AUTHORS file)
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

from lettuce import world

from xivo_acceptance.action.webi import directory as directory_action_webi
from xivo_acceptance.lettuce import common
from xivo_acceptance.lettuce import sysutils


def configure_internal_directory():
    directory_action_webi.add_or_replace_directory(
        name='internal',
        directory='wazo',
        direct_match='firstname,lastname',
        reverse_match='',
        fields={'firstname': '{firstname}',
                'lastname': '{lastname}',
                'display_name': '{firstname} {lastname}',
                'phone': '{exten}'}
    )


def restart_dird():
    sysutils.restart_service('xivo-dird')
    wait_for_dird_http()


def wait_for_dird_http():
    common.wait_until(world.dird_client.is_server_reachable, tries=10)
