# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+


from lettuce.registry import world


def provision_device_using_webi(provcode, device_ip):
    raise NotImplementedError


def add_or_replace_device(device):
    delete_similar_devices(device)
    return world.confd_client.devices.create(device)


def delete_similar_devices(device):
    if 'mac' in device:
        delete_device_with('mac', device['mac'])
    if 'ip' in device:
        delete_device_with('ip', device['ip'])


def delete_device_with(key, value):
    for device in find_devices_with(key, value):
        _delete_device(device['id'])


def find_devices_with(key, value):
    response = world.confd_client.devices.list(**{key: value})
    return response['items']


def _delete_device(device_id):
    world.confd_client.devices.autoprov(device_id)
    world.confd_client.devices.delete(device_id)
