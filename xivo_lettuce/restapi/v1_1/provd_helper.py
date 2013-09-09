# -*- coding: UTF-8 -*-


from xivo_lettuce.remote_py_cmd import remote_exec, remote_exec_with_result


def total_devices():
    return remote_exec_with_result(_total_devices)


def _total_devices(channel):
    from xivo_dao.helpers import provd_connector

    device_manager = provd_connector.device_manager()
    total = len(device_manager.find())
    channel.send(total)


def device_config_has_properties(device, properties):
    remote_exec(_device_config_has_properties, config=device.config, properties=dict(properties[0]))


def _device_config_has_properties(channel, config, properties):
    from xivo_dao.helpers import provd_connector

    provd_config_manager = provd_connector.config_manager()
    config = provd_config_manager.get(config)
    sip_lines = config['raw_config']['sip_lines']

    sip_line = sip_lines['1']

    keys = [u'username', u'auth_username', u'display_name', u'password', u'number']
    for key in keys:
        message = u"Invalid %s ('%s' instead of '%s')" % (key, sip_line[key], properties[key])
        message = message.encode('utf8')
        assert sip_line[key] == properties[key], message


def add_or_replace_device_template(properties):
    remote_exec(_add_or_replace_device_template, properties=dict(properties))


def _add_or_replace_device_template(channel, properties):
    from xivo_dao.helpers import provd_connector
    config_manager = provd_connector.config_manager()

    if 'id' in properties:
        existing = config_manager.find({'X_type': 'device', 'id': properties['id']})
        if len(existing) > 0:
            return

    default_properties = {
        'X_type': 'device',
        'deletable': True,
        'parent_ids': [],
        'raw_config': {}
    }

    properties.update(default_properties)

    config_manager.add(properties)


def delete_device_with_mac(mac):
    remote_exec(_delete_device_with_mac, mac=mac)


def _delete_device_with_mac(channel, mac):
    from xivo_dao.helpers import provd_connector
    config_manager = provd_connector.config_manager()
    device_manager = provd_connector.device_manager()

    for device in device_manager.find({'mac': mac}):
        device_manager.remove(device['id'])
        if 'config' in device:
            config_manager.remove(device['config'])


def delete_device_with_id(device_id):
    remote_exec(_delete_device_with_id, device_id=device_id)


def _delete_device_with_id(channel, device_id):
    from xivo_dao.helpers import provd_connector
    config_manager = provd_connector.config_manager()
    device_manager = provd_connector.device_manager()

    for device in device_manager.find({'id': device_id}):
        device_manager.remove(device['id'])
        if 'config' in device:
            config_manager.remove(device['id'])


def remove_devices_over(max_devices):
    remote_exec(_remove_devices_over, max_devices=max_devices)


def _remove_devices_over(channel, max_devices):
    from xivo_dao.helpers import provd_connector
    config_manager = provd_connector.config_manager()
    device_manager = provd_connector.device_manager()

    all_devices = device_manager.find()
    extra_devices = all_devices[max_devices:]

    for device in extra_devices:
        device_manager.remove(device['id'])
        if 'config' in device:
            config_manager.remove(device['id'])
