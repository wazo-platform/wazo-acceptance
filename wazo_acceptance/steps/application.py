# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import time
from behave import (
    given,
    then,
    when,
)
from hamcrest import (
    assert_that,
    equal_to,
)


@given('there are applications with infos')
def there_are_application_with_info(context):
    for row in context.table:
        config = row.as_dict()

        body = {'name': config['name'], 'destination': config['destination']}
        if config.get('destination_type'):
            body['destination_options'] = {'type': config['destination_type']}
        context.helpers.application.create(body)


@when('"{user_name}" picks up the call from the application "{app_name}"')
def step_impl(context, user_name, app_name):
    application = context.helpers.application.get_by(name=app_name, recurse=True)

    for _ in range(10):
        calls = context.calld_client.applications.list_calls(application['uuid'])['items']
        if not calls:
            time.sleep(0.25)
            continue

        incoming_call = calls[0]
        break
    else:
        assert False, 'call failed to enter stasis app'

    node = context.calld_client.applications.create_node(application['uuid'], [incoming_call['id']])

    user = context.helpers.confd_user.get_by(firstname=user_name)
    user_exten = user['lines'][0]['extensions'][0]['exten']
    user_context = user['lines'][0]['extensions'][0]['context']
    context.calld_client.applications.join_node(
        application['uuid'],
        node['uuid'],
        user_exten,
        user_context,
    )

    phone = context.phone_register.get_phone(user_name)
    phone.answer()


@then('"{app_name}" contains a node with "{n}" calls')
def application_contains_node_with_n_calls(context, app_name, n):
    application = context.helpers.application.get_by(name=app_name, recurse=True)
    calls = context.calld_client.applications.list_calls(application['uuid'])['items']
    assert_that(len(calls), equal_to(2))
