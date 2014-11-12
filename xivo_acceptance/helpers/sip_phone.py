import logging
import sys
import time

from lettuce import world

from linphonelib import ExtensionNotFoundException
from linphonelib import LinphoneException
from linphonelib import Session
from linphonelib.commands import HookStatus

logger = logging.getLogger(__name__)


class CallResult(object):
    not_found = 'not_found'


class SipPhone(object):

    def __init__(self, config):
        if world.config['debug']['linphone']:
            logfile = sys.stdout
        else:
            logfile = None
        self._session = Session(config.sip_name,
                                config.sip_passwd,
                                config.sip_host,
                                config.sip_port,
                                config.rtp_port,
                                logfile)
        self._call_result = None
        self.sip_port = config.sip_port
        self.rtp_port = config.rtp_port

    def answer(self, timeout=2):
        start = time.time()
        exception = None
        while time.time() - start < timeout:
            try:
                self._session.answer()
            except LinphoneException as e:
                exception = e
            else:
                return
        if exception:
            raise exception

    def call(self, exten):
        try:
            self._session.call(exten)
            self._call_result = None
        except ExtensionNotFoundException as e:
            self._call_result = e
        except LinphoneException as e:
            logger.exception(e)

    def hangup(self):
        self._session.hangup()

    def register(self):
        self._session.register()

    def unregister(self):
        self._session.unregister()

    def last_call_result(self):
        if self._call_result:
            raise self._call_result

    def is_ringback_tone(self):
        return self._session.hook_status() == HookStatus.RINGBACK_TONE

    def is_talking(self):
        return self._session.hook_status() == HookStatus.ANSWERED

    def is_ringing(self):
        return self._session.hook_status() == HookStatus.RINGING

    def is_hungup(self):
        return self._session.hook_status() == HookStatus.OFFHOOK


def register_line(sip_config):
    phone = SipPhone(sip_config)
    phone.register()
    return phone
