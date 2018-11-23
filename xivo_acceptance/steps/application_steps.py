# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import time

from lettuce import step, world

from hamcrest import (
    assert_that,
    equal_to,
)

from xivo_acceptance.helpers import (
    application_helper,
    user_helper,
)


@step(u'Given the are applications with infos:')
def given_the_are_applications_with_infos(step):
    if not hasattr(step.scenario, 'applications'):
        step.scenario.applications = {}

    for application in step.hashes:
        app = application_helper.add_or_replace_application(application)
        step.scenario.applications[app['uuid']] = app


@step(u'When "([^"]*)" picks up the call from the application "([^"]*)"')
def when_user_picks_up_the_call_from_the_application_app(step, user_name, app_name):
    app = _get_application(step, app_name)

    for _ in xrange(10):
        calls = world.ctid_ng_client.applications.list_calls(app['uuid'])['items']
        if not calls:
            time.sleep(0.25)
            continue

        incoming_call = calls[0]
        break
    else:
        assert False, 'call failed to enter stasis app'

    node = world.ctid_ng_client.applications.create_node(app['uuid'], [incoming_call['id']])

    user = user_helper.get_user_by_name(user_name)
    user_exten = user['lines'][0]['extensions'][0]['exten']
    user_context = user['lines'][0]['extensions'][0]['context']
    world.ctid_ng_client.applications.join_node(app['uuid'], node['uuid'], user_exten, user_context)

    phone = step.scenario.phone_register.get_user_phone(user_name)
    phone.answer()


@step(u'Then "([^"]*)" contains a node with "([^"]*)" calls')
def then_application_contains_a_node_with_n_calls(step, app_name, n):
    app = _get_application(step, app_name)
    calls = world.ctid_ng_client.applications.list_calls(app['uuid'])['items']
    assert_that(len(calls), equal_to(2))


def _get_application(step, app_name):
    assert hasattr(step.scenario, 'applications')

    for application in step.scenario.applications.itervalues():
        if application['name'] != app_name:
            continue
        return application

    raise Exception('No application found in step.scenario')
