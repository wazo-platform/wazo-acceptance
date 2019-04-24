# -*- coding: utf-8 -*-
# Copyright 2014-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import world

from xivo_acceptance.lettuce import common
from xivo_acceptance.lettuce import sysutils


def configure_internal_directory():
    pass


def restart_dird():
    sysutils.restart_service('wazo-dird')
    wait_for_dird_http()


def wait_for_dird_http():
    common.wait_until(world.dird_client.is_server_reachable, tries=10)
