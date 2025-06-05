
from wazo_acceptance.helpers import sip_phone


        existing_phones = self._phone_register.phones()
        sip_port = _AvailableSipPortFinder(self._sip_port_range).get_available_port(existing_phones)
        rtp_port = _AvailableRTPPortFinder(self._rtp_port_range).get_available_port(existing_phones)
        sip_name = self._sip_helper.get_auth_option(endpoint_sip, 'username')
        sip_passwd = self._sip_helper.get_auth_option(endpoint_sip, 'password')
        sip_host = self._host
        return SIPConfig(sip_port, rtp_port, sip_name, sip_passwd, sip_host)