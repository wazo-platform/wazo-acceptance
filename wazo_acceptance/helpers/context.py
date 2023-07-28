# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class Context:

    def __init__(self, confd_client):
        self._confd_client = confd_client

    def update_contextnumbers_user(self, label, range_start, range_end):
        context = self._find_by(label=label)
        ranges = [{'start': str(range_start), 'end': str(range_end)}]
        if not context:
            context = {'label': label, 'type': 'internal', 'user_ranges': ranges}
            self._confd_client.contexts.create(context)
        else:
            context['user_ranges'] = ranges
            self._confd_client.contexts.update(context)

    def update_contextnumbers_group(self, label, range_start, range_end):
        context = self._find_by(label=label)
        ranges = [{'start': str(range_start), 'end': str(range_end)}]
        if not context:
            context = {'label': label, 'type': 'internal', 'group_ranges': ranges}
            self._confd_client.contexts.create(context)
        else:
            context['group_ranges'] = ranges
            self._confd_client.contexts.update(context)

    def update_contextnumbers_queue(self, label, range_start, range_end):
        context = self._find_by(label=label)
        ranges = [{'start': str(range_start), 'end': str(range_end)}]
        if not context:
            context = {'label': label, 'type': 'internal', 'queue_ranges': ranges}
            self._confd_client.contexts.create(context)
        else:
            context['queue_ranges'] = ranges
            self._confd_client.contexts.update(context)

    def update_contextnumbers_conference(self, label, range_start, range_end):
        context = self._find_by(label=label)
        ranges = [{'start': str(range_start), 'end': str(range_end)}]
        if not context:
            context = {'label': label, 'type': 'internal', 'conference_room_ranges': ranges}
            self._confd_client.contexts.create(context)
        else:
            context['conference_room_ranges'] = ranges
            self._confd_client.contexts.update(context)

    def update_contextnumbers_incall(self, label, range_start, range_end, did_length):
        context = self._find_by(label=label)
        ranges = [{'start': str(range_start), 'end': str(range_end), 'did_length': did_length}]
        if not context:
            context = {'label': label, 'type': 'incall', 'incall_ranges': ranges}
            self._confd_client.contexts.create(context)
        else:
            context['incall_ranges'] = ranges
            self._confd_client.contexts.update(context)

    def create_outcall_context(self, external_label, internal_label):
        context = self._find_by(label=external_label)
        internal_context = self._find_by(label=internal_label)
        if not context:
            context_data = {'label': 'to-extern', 'type': 'outcall'}
            context = self._confd_client.contexts.create(context_data)

        self._confd_client.contexts(internal_context).update_contexts([{'id': context['id']}])

    def _find_by(self, **kwargs):
        contexts = self._confd_client.contexts.list(recurse=True, **kwargs)['items']
        for context in contexts:
            del context['uuid']
            return context

    def get_by(self, **kwargs):
        context = self._find_by(**kwargs)
        if not context:
            raise Exception(f'Context not found: {kwargs}')
        return context
