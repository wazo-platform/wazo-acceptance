# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class EndpointSIP:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        sip = self._confd_client.endpoints_sip.create(body)
        self._context.add_cleanup(self._confd_client.endpoints_sip.delete, sip)
        return sip

    def update(self, body):
        with self._context.helpers.bus.wait_for_asterisk_reload(dialplan=True, pjsip=True):
            self._confd_client.endpoints_sip.update(body)

    def get_auth_option(self, endpoint_sip, wanted_option):
        for option in endpoint_sip['auth_section_options']:
            if option[0] == wanted_option:
                return option[1]
        raise Exception(f'Unable to find {wanted_option} in {endpoint_sip}')

    def get_template_by(self, **kwargs):
        template = self._find_template_by(**kwargs)
        if not template:
            raise Exception(f'EndpointSIPTemplate not found: {kwargs}')
        return template

    def _find_template_by(self, **kwargs):
        templates = self._confd_client.endpoints_sip_templates.list(**kwargs)['items']
        for template in templates:
            return template

    def generate_form(self, raw_name, webrtc=None):
        template = self.get_template_by(label='global')
        name = ''.join([c if ord(c) < 128 else 'X' for c in raw_name])
        endpoint_section_options = [['webrtc', webrtc]] if webrtc is not None else []
        return {
            'name': name,
            'auth_section_options': [
                ['username', name],
                ['password', 'password'],
            ],
            'endpoint_section_options': endpoint_section_options,
            'templates': [template],
        }
