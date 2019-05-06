# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import world

from . import incall_helper


def add_or_replace_application(application):
    _delete_similar_applications(application)
    app_body = {
        'name': application['name'],
        'destination_options': {
            'type': 'holding',
        },
    }
    app = world.confd_client.applications.create(app_body)
    incall_helper.add_incall(
        application['incall'],
        'from-extern',
        'application',
        {
            'application_uuid': app['uuid'],
            'application': 'custom',
        },
    )
    return app


def _delete_similar_applications(application):
    name = application.get('name')
    if name:
        for app in _find_by_name(name):
            world.confd_client.applications.delete(app['uuid'])

    incall = application.get('incall')
    if incall:
        incall_helper.delete_incalls_with_did(incall)


def _find_by_name(application_name):
    response = world.confd_client.applications.list(name=application_name, recurse=True)
    for app in response['items']:
        yield app
