# Copyright 2013-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class Context:

    def __init__(self, confd_client):
        self._confd_client = confd_client

    def update_contextnumbers_user(self, name, range_start, range_end):
        context = self._find_by(name=name)
        ranges = [{'start': str(range_start), 'end': str(range_end)}]
        if not context:
            context = {'name': name, 'label': name, 'type': 'internal', 'user_ranges': ranges}
            self._confd_client.contexts.create(context)
        else:
            context['user_ranges'] = ranges
            self._confd_client.contexts.update(context)

    def update_contextnumbers_group(self, name, range_start, range_end):
        context = self._find_by(name=name)
        ranges = [{'start': str(range_start), 'end': str(range_end)}]
        if not context:
            context = {'name': name, 'label': name, 'type': 'internal', 'group_ranges': ranges}
            self._confd_client.contexts.create(context)
        else:
            context['group_ranges'] = ranges
            self._confd_client.contexts.update(context)

    def update_contextnumbers_queue(self, name, range_start, range_end):
        context = self._find_by(name=name)
        ranges = [{'start': str(range_start), 'end': str(range_end)}]
        if not context:
            context = {'name': name, 'label': name, 'type': 'internal', 'queue_ranges': ranges}
            self._confd_client.contexts.create(context)
        else:
            context['queue_ranges'] = ranges
            self._confd_client.contexts.update(context)

    def update_contextnumbers_conference(self, name, range_start, range_end):
        context = self._find_by(name=name)
        ranges = [{'start': str(range_start), 'end': str(range_end)}]
        if not context:
            context = {'name': name, 'label': name, 'type': 'internal', 'conference_room_ranges': ranges}
            self._confd_client.contexts.create(context)
        else:
            context['conference_room_ranges'] = ranges
            self._confd_client.contexts.update(context)

    def update_contextnumbers_incall(self, name, range_start, range_end, did_length):
        context = self._find_by(name=name)
        ranges = [{'start': str(range_start), 'end': str(range_end), 'did_length': did_length}]
        if not context:
            context = {'name': name, 'label': name, 'type': 'incall', 'incall_ranges': ranges}
            self._confd_client.contexts.create(context)
        else:
            context['incall_ranges'] = ranges
            self._confd_client.contexts.update(context)

    def create_outcall_context(self, external_name, internal_name):
        context = self._find_by(name=external_name)
        internal_context = self._find_by(name=internal_name)
        if not context:
            context_data = {'name': 'to-extern', 'label': 'to-extern', 'type': 'outcall'}
            context = self._confd_client.contexts.create(context_data)

        self._confd_client.contexts(internal_context).update_contexts([{'id': context['id']}])

    def _find_by(self, **kwargs):
        contexts = self._confd_client.contexts.list(recurse=True, **kwargs)['items']
        for context in contexts:
            return context
