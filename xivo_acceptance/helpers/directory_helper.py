# -*- coding: utf-8 -*-
# Copyright 2014-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

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
    sysutils.restart_service('wazo-dird')
    wait_for_dird_http()


def wait_for_dird_http():
    common.wait_until(world.dird_client.is_server_reachable, tries=10)
