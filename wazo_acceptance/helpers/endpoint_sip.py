# Copyright 2019-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class EndpointSIP:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        options = []
        webrtc = body.get('webrtc')
        if webrtc is not None:
            options.append(('webrtc', webrtc))

        if options:
            body['options'] = options

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
            raise Exception('EndpointSIPTemplate not found: {}'.format(kwargs))
        return template

    def _find_template_by(self, **kwargs):
        templates = self._confd_client.endpoints_sip_templates.list(**kwargs)['items']
        for template in templates:
            return template
