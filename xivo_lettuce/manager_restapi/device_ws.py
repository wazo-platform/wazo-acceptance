# -*- coding: utf-8 -*-


from xivo_lettuce.restapi.v1_1 import ws_utils_session as ws_utils

DEVICES_URL = 'devices'


def create_device(parameters):
    return ws_utils.rest_post(DEVICES_URL, parameters)


def synchronize(device_id):
    return ws_utils.rest_get('%s/%s/synchronize' % (DEVICES_URL, device_id))


def reset_to_autoprov(device_id):
    return ws_utils.rest_get('%s/%s/autoprov' % (DEVICES_URL, device_id))
