# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from lettuce import world

from xivo_acceptance.helpers import (
    entity_helper,
    outcall_helper,
    tenant_helper,
)


def update_contextnumbers_user(name, numberbeg, numberend, entity_name=None):
    context = find_context_by(name=name)
    range_ = {'start': str(numberbeg), 'end': str(numberend)}
    if not context:
        add_context(
            name,
            name,
            'internal',
            user_range=range_,
            entity_name=entity_name
        )
    else:
        context['user_ranges'] = [range_]
        world.confd_client.contexts.update(context)


def update_contextnumbers_group(name, numberbeg, numberend, entity_name=None):
    context = find_context_by(name=name)
    range_ = {'start': str(numberbeg), 'end': str(numberend)}
    if not context:
        add_context(
            name,
            name,
            'internal',
            group_range=range_,
            entity_name=entity_name
        )
    else:
        context['group_ranges'] = [range_]
        world.confd_client.contexts.update(context)


def update_contextnumbers_queue(name, numberbeg, numberend, entity_name=None):
    context = find_context_by(name=name)
    range_ = {'start': str(numberbeg), 'end': str(numberend)}
    if not context:
        add_context(
            name,
            name,
            'internal',
            queue_range=range_,
            entity_name=entity_name
        )
    else:
        context['queue_ranges'] = [range_]
        world.confd_client.contexts.update(context)


def update_contextnumbers_meetme(name, numberbeg, numberend, entity_name=None):
    context = find_context_by(name=name)
    range_ = {'start': str(numberbeg), 'end': str(numberend)}
    if not context:
        add_context(
            name,
            name,
            'internal',
            conference_range=range_,
            entity_name=entity_name
        )
    else:
        context['conference_ranges'] = [range_]
        world.confd_client.contexts.update(context)


def update_contextnumbers_incall(name, numberbeg, numberend, didlength, entity_name=None):
    context = find_context_by(name=name)
    range_ = {'start': str(numberbeg), 'end': str(numberend), 'did_length': didlength}
    if not context:
        add_context(
            name,
            name,
            'incall',
            incall_range=range_,
            entity_name=entity_name
        )
    else:
        context['incall_ranges'] = [range_]
        world.confd_client.contexts.update(context)


def add_context(name,
                label,
                type_,
                conference_range=None,
                group_range=None,
                incall_range=None,
                queue_range=None,
                user_range=None,
                entity_name=None):
    entity_name = entity_name or world.config['default_entity']
    entity_helper.add_entity(entity_name, entity_name)

    tenant_uuid = tenant_helper.get_tenant_uuid(entity_name)
    world.confd_client.set_tenant(tenant_uuid)

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

    world.confd_client.contexts.create(context)


def delete_context(context):
    outcall_helper.delete_outcalls_with_context(context['name'])
    world.confd_client.contexts.delete(context)


def add_or_replace_context(name, display_name, context_type):
    context = find_context_by(name=name)
    if context:
        delete_context(context)
    add_context(name, display_name, context_type)


def find_context_by(**kwargs):
    contexts = world.confd_client.contexts.list(recurse=True, **kwargs)['items']
    for context in contexts:
        return context
