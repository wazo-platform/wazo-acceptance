from xivo_lettuce.restapi.v1_1 import ws_utils_session as ws_utils

DEVICES_URL = 'devices'


def create_device(parameters):
    return ws_utils.rest_post(DEVICES_URL, parameters)


def get_device(device_id):
    return ws_utils.rest_get("%s/%s" % (DEVICES_URL, device_id))


def device_list(parameters={}):
    return ws_utils.rest_get(DEVICES_URL, params=parameters)
