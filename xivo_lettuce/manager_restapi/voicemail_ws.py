
from xivo_lettuce.restapi.v1_1 import ws_utils_session as ws_utils

VOICEMAIL_URL = 'voicemails'


def get_voicemail(voicemail_id):
    return ws_utils.rest_get('/%s/%s' % (VOICEMAIL_URL, voicemail_id))


def voicemail_list(parameters={}):
    return ws_utils.rest_get('%s' % VOICEMAIL_URL, params=parameters)
