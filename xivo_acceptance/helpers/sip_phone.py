from linphonelib import Session
from linphonelib import ExtensionNotFoundException
from linphonelib import LinphoneException


class CallResult(object):
    not_found = 'not_found'


class SipPhone(object):

    def __init__(self, sip_name, sip_passwd, hostname, local_port):
        self._session = Session(sip_name, sip_passwd, hostname, local_port)
        self._call_result = None

    def call(self, exten):
        try:
            self._session.call(exten)
            self._call_result = None
        except ExtensionNotFoundException as e:
            self._call_result = e
        except LinphoneException:
            print 'Not the good exception'

    def register(self):
        self._session.register()

    def unregister(self):
        self._session.unregister()

    def last_call_result(self):
        if self._call_result:
            raise self._call_result
