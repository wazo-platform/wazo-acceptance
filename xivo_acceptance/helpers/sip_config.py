from collections import namedtuple
import subprocess


SIPConfig = namedtuple('SIPConfig', ('sip_port', 'rtp_port', 'sip_name', 'sip_passwd', 'sip_host'))


class _AbstractAvailablePortFinder(object):
    def _port_range(self, port_range):
        start, _, end = port_range.partition(',')
        return int(start), int(end)

    def get_available_port(self, existing_phones):
        for port in self._ports:
            if self._port_is_available(port, existing_phones):
                return port

        raise Exception('All ports are used')

    def _port_is_available(self, port, existing_phones):
        return port not in self._used_ports(existing_phones) and not self._port_in_use(port)

    def _used_ports(self, existing_phones):
        for phone in existing_phones:
            yield self._port_from_phone(phone)


class _AvailableSipPortFinder(_AbstractAvailablePortFinder):

    def __init__(self, world_config):
        start, end = self._port_range(world_config['linphone']['sip_port_range'])
        self._ports = xrange(start, end)

    def _port_from_phone(self, phone):
        return phone.sip_port

    def _port_in_use(self, port):
        try:
            subprocess.check_call(['lsof', '-i', ':%s' % port])
            return True
        except subprocess.CalledProcessError:
            return False


class _AvailableRTPPortFinder(_AbstractAvailablePortFinder):

    def __init__(self, world_config):
        start, end = self._port_range(world_config['linphone']['rtp_port_range'])

        # RTP port must be an even number
        # RTCP will use the higher odd number
        self._ports = xrange(start, end, 2)

    def _port_from_phone(self, phone):
        return phone.rtp_port

    def _port_in_use(self, port):
        try:
            subprocess.check_call(['lsof', '-i', ':{rtp_port},{rtcp_port}'.format(rtp_port=port, rtcp_port=port + 1)])
            return True
        except subprocess.CalledProcessError:
            return False


def create_config(world_config, phone_register, line_config):
    if line_config.protocol != 'sip':
        raise NotImplementedError('Line protocol must be SIP')

    existing_phones = phone_register.phones().values()
    sip_port = _AvailableSipPortFinder(world_config).get_available_port(existing_phones)
    rtp_port = _AvailableRTPPortFinder(world_config).get_available_port(existing_phones)
    sip_name = line_config.name
    sip_passwd = line_config.secret
    sip_host = world_config['xivo_host']

    return SIPConfig(sip_port, rtp_port, sip_name, sip_passwd, sip_host)
