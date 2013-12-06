import subprocess

from lettuce import world
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


def register_line(line_config, name):
    return _register_sip_line(name, line_config.name, line_config.secret)


def _register_sip_line(name, sip_name, sip_passwd):
    # XXX find a way to wait for the sip reload
    port = _get_available_sip_port()
    phone = SipPhone(sip_name, sip_passwd, world.config.xivo_host, port)
    phone.register()
    return phone


def _port_in_use(port):
    try:
        subprocess.check_call(['lsof', '-i', ':%s' % port])
        return False
    except subprocess.CalledProcessError:
        return True


def _used_ports():
    for name_phone in getattr(world, 'sip_phones', {}).itervalues():
        for phone in name_phone.itervalues():
            yield phone.port


def _port_is_available(port):
    return port not in _used_ports() and _port_in_use(port)


def _get_available_sip_port():
    # XXX add a configuration option
    ports = xrange(5061, 5070)

    for port in ports:
        if _port_is_available(port):
            return port

    raise Exception('All sip ports are used')
