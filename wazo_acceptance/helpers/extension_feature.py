# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class ExtensionFeature:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def get_by(self, **kwargs):
        user = self.find_by(**kwargs)
        if not user:
            raise Exception('ExtensionFeature not found: {}'.format(kwargs))
        return user

    def find_by(self, **kwargs):
        extensions_features = self._confd_client.extensions_features.list(**kwargs)['items']
        for extension in extensions_features:
            return extension

    def update(self, extension_feature):
        old_feature = self._confd_client.extensions_features.get(extension_feature['id'])

        with self._context.helpers.bus.wait_for_asterisk_reload(dialplan=True):
            self._confd_client.extensions_features.update(extension_feature)

        self._context.add_cleanup(self._confd_client.extensions_features.update, old_feature)

    def enable(self, feature, extension=None):
        feature = self.get_by(search=feature)
        feature['enabled'] = True
        if extension:
            feature['exten'] = '_{}.'.format(extension)
        self.update(feature)
