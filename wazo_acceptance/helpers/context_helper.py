# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class ContextHelper:

    def __init__(self, confd_client):
        self._confd_client = confd_client

    def update_contextnumbers_user(self, name, range_start, range_end):
        context = self._find_context_by(name=name)
        range_ = {'start': str(range_start), 'end': str(range_end)}
        if not context:
            context = {'name': name, 'label': name, 'type': 'internal', 'user_range': range_}
            self._confd_client.contexts.create(context)
        else:
            context['user_ranges'] = [range_]
            self._confd_client.contexts.update(context)

    def update_contextnumbers_group(self, name, range_start, range_end):
        context = self._find_context_by(name=name)
        range_ = {'start': str(range_start), 'end': str(range_end)}
        if not context:
            context = {'name': name, 'label': name, 'type': 'internal', 'group_range': range_}
            self._confd_client.contexts.create(context)
        else:
            context['group_ranges'] = [range_]
            self._confd_client.contexts.update(context)

    def update_contextnumbers_queue(self, name, range_start, range_end):
        context = self._find_context_by(name=name)
        range_ = {'start': str(range_start), 'end': str(range_end)}
        if not context:
            context = {'name': name, 'label': name, 'type': 'internal', 'queue_range': range_}
            self._confd_client.contexts.create(context)
        else:
            context['queue_ranges'] = [range_]
            self._confd_client.contexts.update(context)

    def update_contextnumbers_conference(self, name, range_start, range_end):
        context = self._find_context_by(name=name)
        range_ = {'start': str(range_start), 'end': str(range_end)}
        if not context:
            context = {'name': name, 'label': name, 'type': 'internal', 'conference_range': range_}
            self._confd_client.contexts.create(context)
        else:
            context['conference_ranges'] = [range_]
            self._confd_client.contexts.update(context)

    def update_contextnumbers_incall(self, name, range_start, range_end, did_length):
        context = self._find_context_by(name=name)
        range_ = {'start': str(range_start), 'end': str(range_end), 'did_length': did_length}
        if not context:
            context = {'name': name, 'label': name, 'type': 'incall', 'incall_range': range_}
            self._confd_client.contexts.create(context)
        else:
            context['incall_ranges'] = [range_]
            self._confd_client.contexts.update(context)

    def _find_context_by(self, **kwargs):
        contexts = self._confd_client.contexts.list(recurse=True, **kwargs)['items']
        for context in contexts:
            return context
