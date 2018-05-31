# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from lettuce import world

from xivo_acceptance.helpers import outcall_helper, entity_helper
from xivo_ws import Context, ContextRange, WebServiceRequestError


def update_contextnumbers_user(name, numberbeg, numberend, entity_name=None):
    context = get_context_with_name(name)
    contextnumbers = ContextRange(int(numberbeg), int(numberend))
    if not context:
        add_context(name,
                    name,
                    'internal',
                    contextnumbers_user=contextnumbers,
                    entity_name=entity_name)
    else:
        context.users.append(contextnumbers)
        world.ws.contexts.edit(context)


def update_contextnumbers_group(name, numberbeg, numberend, entity_name=None):
    context = get_context_with_name(name)
    contextnumbers = ContextRange(int(numberbeg), int(numberend))
    if not context:
        add_context(name,
                    name,
                    'internal',
                    contextnumbers_group=contextnumbers,
                    entity_name=entity_name)
    else:
        context.groups.append(contextnumbers)
        world.ws.contexts.edit(context)


def update_contextnumbers_queue(name, numberbeg, numberend, entity_name=None):
    context = get_context_with_name(name)
    contextnumbers = ContextRange(int(numberbeg), int(numberend))
    if not context:
        add_context(name,
                    name,
                    'internal',
                    contextnumbers_queue=contextnumbers,
                    entity_name=entity_name)
    else:
        context.queues.append(contextnumbers)
        world.ws.contexts.edit(context)


def update_contextnumbers_meetme(name, numberbeg, numberend, entity_name=None):
    context = get_context_with_name(name)
    contextnumbers = ContextRange(int(numberbeg), int(numberend))
    if not context:
        add_context(name,
                    name,
                    'internal',
                    contextnumbers_meetme=contextnumbers,
                    entity_name=entity_name)
    else:
        context.conf_rooms.append(contextnumbers)
        world.ws.contexts.edit(context)


def update_contextnumbers_incall(name, numberbeg, numberend, didlength, entity_name=None):
    context = get_context_with_name(name)
    contextnumbers = ContextRange(int(numberbeg), int(numberend), did_length=didlength)
    if not context:
        add_context(name,
                    name,
                    'incall',
                    contextnumbers_incall=contextnumbers,
                    entity_name=entity_name)
    else:
        context.incalls.append(contextnumbers)
        world.ws.contexts.edit(context)


def add_context(name,
                display_name,
                context_type,
                context_include=[],
                contextnumbers_user='',
                contextnumbers_group='',
                contextnumbers_meetme='',
                contextnumbers_queue='',
                contextnumbers_incall='',
                entity_name=None):
    entity_name = entity_name or world.config['default_entity']
    entity_helper.add_entity(entity_name, entity_name)

    context = Context()
    context.name = name
    context.display_name = display_name
    context.type = context_type
    context.entity = entity_name

    if context_include:
        context.context_include = [context_include]
    if contextnumbers_user:
        context.users = [contextnumbers_user]
    if contextnumbers_group:
        context.groups = [contextnumbers_group]
    if contextnumbers_queue:
        context.queues = [contextnumbers_queue]
    if contextnumbers_meetme:
        context.conf_rooms = [contextnumbers_meetme]
    if contextnumbers_incall:
        context.incalls = [contextnumbers_incall]

    world.ws.contexts.add(context)


def delete_context(context):
    outcall_helper.delete_outcalls_with_context(context.name)
    world.ws.contexts.delete(context.id)


def add_or_replace_context(name, display_name, context_type):
    context = get_context_with_name(name)
    if context:
        delete_context(context)
    add_context(name, display_name, context_type)


def get_context_with_name(name):
    try:
        return world.ws.contexts.view(name)
    except WebServiceRequestError:
        return False
