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
        application = context.helpers.application.create(body)

        body = {'destination': {
            'type': 'application',
            'application': 'custom',
            'application_uuid': application['uuid'],
        }}
        incall = context.helpers.incall.create(body)

        body = {'exten': config['incall'], 'context': 'from-extern'}
        extension = context.helpers.extension.create(body)

        context.helpers.incall.add_extension(incall, extension)


@when('"{user_name}" picks up the call from the application "{app_name}"')
def step_impl(context, user_name, app_name):
    application = context.helpers.application.find_by(name=app_name, recurse=True)
    assert application is not None

    for _ in range(10):
        calls = context.helpers.application.list_calls(application['uuid'])
        if not calls:
            time.sleep(0.25)
            continue

        incoming_call = calls[0]
        break
    else:
        assert False, 'call failed to enter stasis app'

    node = context.helpers.application.create_node(application['uuid'], [incoming_call['id']])

    user = context.helpers.confd_user.get_by(firstname=user_name)
    user_exten = user['lines'][0]['extensions'][0]['exten']
    user_context = user['lines'][0]['extensions'][0]['context']
    context.helpers.application.join_node(
        application['uuid'],
        node['uuid'],
        user_exten,
        user_context,
    )

    phone = context.phone_register.get_phone(user_name)
    phone.answer()


@then(u'"{app_name}" contains a node with "{n}" calls')
def application_contains_node_with_n_calls(context, app_name, n):
    application = context.helpers.application.find_by(name=app_name, recurse=True)

    calls = context.helpers.application.list_calls(application['uuid'])
    assert_that(len(calls), equal_to(2))
