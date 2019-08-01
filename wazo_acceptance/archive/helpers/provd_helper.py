# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import world
from hamcrest import assert_that, is_not, none, is_
from xivo_test_helpers import until
from wazo_provd_client import operation


def find_by_mac(mac):
    return _find_by('mac', mac)


def get_by_mac(mac):
    device = find_by_mac(mac)
    assert_that(device, is_not(none()), "Device %s does not exist" % mac)
    return device


def _find_by(key, value):
    device_manager = world.provd_client.devices
    devices = device_manager.list({key: value})['devices']
    return devices[0] if devices else None


def plugins_successfully_updated():
    with world.provd_client.plugins.update() as operation_progress:
        until.assert_(
            operation_successful, operation_progress, tries=20, interval=0.5
        )


def operation_successful(operation_ressource):
    operation_ressource.update()
    assert_that(operation_ressource.state, is_(operation.OIP_SUCCESS))
