# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from lettuce import world
from xivo_ws import Context, ContextRange, WebServiceRequestError


def update_contextnumbers_user(name, numberbeg, numberend):
    context = get_context_with_name(name)
    contextnumbers = ContextRange(int(numberbeg), int(numberend))
    if not context:
        add_context(name, name, 'internal', contextnumbers_user=contextnumbers)
    else:
        context.users.append(contextnumbers)
        world.ws.contexts.edit(context)


def update_contextnumbers_group(name, numberbeg, numberend):
    context = get_context_with_name(name)
    contextnumbers = ContextRange(int(numberbeg), int(numberend))
    if not context:
        add_context(name, name, 'internal', contextnumbers_group=contextnumbers)
    else:
        context.groups.append(contextnumbers)
        world.ws.contexts.edit(context)


def update_contextnumbers_queue(name, numberbeg, numberend):
    context = get_context_with_name(name)
    contextnumbers = ContextRange(int(numberbeg), int(numberend))
    if not context:
        add_context(name, name, 'internal', contextnumbers_queue=contextnumbers)
    else:
        context.queues.append(contextnumbers)
        world.ws.contexts.edit(context)


def update_contextnumbers_meetme(name, numberbeg, numberend):
    context = get_context_with_name(name)
    contextnumbers = ContextRange(int(numberbeg), int(numberend))
    if not context:
        add_context(name, name, 'internal', contextnumbers_meetme=contextnumbers)
    else:
        context.conf_rooms.append(contextnumbers)
        world.ws.contexts.edit(context)


def update_contextnumbers_incall(name, numberbeg, numberend, didlength):
    context = get_context_with_name(name)
    contextnumbers = ContextRange(int(numberbeg), int(numberend), did_length=didlength)
    if not context:
        add_context(name, name, 'incall', contextnumbers_incall=contextnumbers)
    else:
        context.incalls.append(contextnumbers)
        world.ws.contexts.edit(context)


def add_context(name, display_name, context_type,
                 context_include=[],
                 contextnumbers_user='',
                 contextnumbers_group='',
                 contextnumbers_meetme='',
                 contextnumbers_queue='',
                 contextnumbers_incall=''):

    context = Context()
    context.name = name
    context.display_name = display_name
    context.type = context_type
    context.entity = 'xivo_entity'

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


def get_context_with_name(name):
    try:
        return world.ws.contexts.view(name)
    except WebServiceRequestError:
        return False
