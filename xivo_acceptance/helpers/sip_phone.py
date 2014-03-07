import subprocess
import sys
import time

from lettuce import world
from linphonelib import Session
from linphonelib import ExtensionNotFoundException
from linphonelib import LinphoneException
from linphonelib.commands import HookStatus


class CallResult(object):
    not_found = 'not_found'


class SipPhone(object):

    def __init__(self, sip_name, sip_passwd, hostname, local_port):
        if world.config.linphone_debug:
            logfile = sys.stdout
        else:
            logfile = None
        self._session = Session(sip_name, sip_passwd, hostname, local_port, logfile)
        self._call_result = None
        self.port = local_port

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
        except LinphoneException:
            print 'Not the good exception'

    def hangup(self):
        self._session.hangup()

    def register(self):
        self._session.register()

    def unregister(self):
        self._session.unregister()

    def last_call_result(self):
        if self._call_result:
            raise self._call_result

    def is_ringing(self):
        return self._session.hook_status() == HookStatus.RINGING


class _AvailableSipPortFinder(object):

    def __init__(self):
        port_range = world.config.linphone_port_range
        start, _, end = port_range.partition(',')
        self._ports = xrange(int(start), int(end))

    def get_available_port(self):
        for port in self._ports:
            if self._port_is_available(port):
                return port

        raise Exception('All sip ports are used')

    def _used_ports(self):
        for name_phone in getattr(world, 'sip_phones', {}).itervalues():
            for phone in name_phone.itervalues():
                yield phone.port

    def _port_is_available(self, port):
        return port not in self._used_ports() and not self._port_in_use(port)

    def _port_in_use(self, port):
        try:
            subprocess.check_call(['lsof', '-i', ':%s' % port])
            return True
        except subprocess.CalledProcessError:
            return False


def register_line(line_config, name):
    if line_config.protocol == 'sip':
        return _register_sip_line(name, line_config.name, line_config.secret)


def _register_sip_line(name, sip_name, sip_passwd):
    port = _AvailableSipPortFinder().get_available_port()
    phone = SipPhone(sip_name, sip_passwd, world.config.xivo_host, port)
    phone.register()
    return phone
