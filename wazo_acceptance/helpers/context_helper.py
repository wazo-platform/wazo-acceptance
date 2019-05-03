# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


def update_contextnumbers_user(behave_context, name, numberbeg, numberend):
    context = _find_context_by(behave_context, name=name)
    range_ = {'start': str(numberbeg), 'end': str(numberend)}
    if not context:
        _add_context(
            behave_context,
            name,
            name,
            'internal',
            user_range=range_,
        )
    else:
        context['user_ranges'] = [range_]
        behave_context.confd_client.contexts.update(context)


def update_contextnumbers_group(behave_context, name, numberbeg, numberend):
    context = _find_context_by(behave_context, name=name)
    range_ = {'start': str(numberbeg), 'end': str(numberend)}
    if not context:
        _add_context(
            behave_context,
            name,
            name,
            'internal',
            group_range=range_,
        )
    else:
        context['group_ranges'] = [range_]
        behave_context.confd_client.contexts.update(context)


def update_contextnumbers_queue(behave_context, name, numberbeg, numberend):
    context = _find_context_by(behave_context, name=name)
    range_ = {'start': str(numberbeg), 'end': str(numberend)}
    if not context:
        _add_context(
            behave_context,
            name,
            name,
            'internal',
            queue_range=range_,
        )
    else:
        context['queue_ranges'] = [range_]
        behave_context.confd_client.contexts.update(context)


def update_contextnumbers_conference(behave_context, name, numberbeg, numberend):
    context = _find_context_by(behave_context, name=name)
    range_ = {'start': str(numberbeg), 'end': str(numberend)}
    if not context:
        _add_context(
            behave_context,
            name,
            name,
            'internal',
            conference_range=range_,
        )
    else:
        context['conference_ranges'] = [range_]
        behave_context.confd_client.contexts.update(context)


def update_contextnumbers_incall(behave_context, name, numberbeg, numberend, didlength):
    context = _find_context_by(behave_context, name=name)
    range_ = {'start': str(numberbeg), 'end': str(numberend), 'did_length': didlength}
    if not context:
        _add_context(
            behave_context,
            name,
            name,
            'incall',
            incall_range=range_,
        )
    else:
        context['incall_ranges'] = [range_]
        behave_context.confd_client.contexts.update(context)


def _add_context(behave_context,
                 name,
                 label,
                 type_,
                 conference_range=None,
                 group_range=None,
                 incall_range=None,
                 queue_range=None,
                 user_range=None):

    context = {
        'name': name,
        'label': label,
        'type': type_,
        'conference_ranges': [conference_range] if conference_range else [],
        'group_ranges': [group_range] if group_range else [],
        'incall_ranges': [incall_range] if incall_range else [],
        'queue_ranges': [queue_range] if queue_range else [],
        'user_ranges': [user_range] if user_range else [],
    }

    behave_context.confd_client.contexts.create(context)


def _find_context_by(behave_context, **kwargs):
    contexts = behave_context.confd_client.contexts.list(recurse=True, **kwargs)['items']
    for context in contexts:
        return context
