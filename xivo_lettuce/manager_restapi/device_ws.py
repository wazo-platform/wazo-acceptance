from xivo_lettuce.restapi.v1_1 import ws_utils_session as ws_utils

DEVICES_URL = 'devices'


def create_device(parameters):
    return ws_utils.rest_post(DEVICES_URL, parameters)
