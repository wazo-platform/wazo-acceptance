# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from collections import namedtuple
import subprocess


SIPConfig = namedtuple('SIPConfig', ('sip_port', 'rtp_port', 'sip_name', 'sip_passwd', 'sip_host'))


class _AbstractAvailablePortFinder:

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

    def __init__(self, sip_port_range):
        start, end = self._port_range(sip_port_range)
        self._ports = range(start, end)

    def _port_from_phone(self, phone):
        return phone.sip_port

    def _port_in_use(self, port):
        try:
            subprocess.check_call(['lsof', '-i', ':%s' % port])
            return True
        except subprocess.CalledProcessError:
            return False


class _AvailableRTPPortFinder(_AbstractAvailablePortFinder):

    def __init__(self, rtp_port_range):
        start, end = self._port_range(rtp_port_range)

        # RTP port must be an even number
        # RTCP will use the higher odd number
        self._ports = range(start, end, 2)

    def _port_from_phone(self, phone):
        return phone.rtp_port

    def _port_in_use(self, port):
        try:
            subprocess.check_call(['lsof', '-i', ':{rtp_port},{rtcp_port}'.format(rtp_port=port, rtcp_port=port + 1)])
            return True
        except subprocess.CalledProcessError:
            return False


class SIPConfigGenerator:

    def __init__(self, host, config, phone_register, sip_helper):
        self._host = host
        self._rtp_port_range = config['rtp_port_range']
        self._sip_port_range = config['sip_port_range']
        self._phone_register = phone_register
        self._sip_helper = sip_helper

    def create(self, endpoint_sip):
        existing_phones = self._phone_register.phones()
        sip_port = _AvailableSipPortFinder(self._sip_port_range).get_available_port(existing_phones)
        rtp_port = _AvailableRTPPortFinder(self._rtp_port_range).get_available_port(existing_phones)
        sip_name = self._sip_helper.get_auth_option(endpoint_sip, 'username')
        sip_passwd = self._sip_helper.get_auth_option(endpoint_sip, 'password')
        sip_host = self._host
        return SIPConfig(sip_port, rtp_port, sip_name, sip_passwd, sip_host)
