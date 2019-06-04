# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class HAHelper:

    def __init__(self, context):
        self._context = context

    def set(self, config):
        self._context.confd_client.ha.update(config)

    def get(self):
        return self._context.confd_client.ha.get()
