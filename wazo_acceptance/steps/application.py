# Copyright 2019-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import given, then, when
from hamcrest import assert_that, equal_to
from wazo_test_helpers import until


@given('there are applications with infos:')
def given_there_are_application_with_info(context):
    for row in context.table:
        config = row.as_dict()

        body = {'name': config['name'], 'destination': config['destination']}
        if config.get('destination_type'):
            body['destination_options'] = {'type': config['destination_type']}
        context.helpers.application.create(body)


@when('"{user_name}" picks up the call from the application "{app_name}"')
def when_1_picks_up_the_call_from_the_application_2(context, user_name, app_name):
    application = context.helpers.application.get_by(name=app_name, recurse=True)

    incoming_call = until.return_(
        context.helpers.application.get_first_call,
        application['uuid'],
        timeout=3,
        interval=0.25
    )
    node = context.calld_client.applications.create_node(application['uuid'], [incoming_call['id']])

    user = context.helpers.confd_user.get_by(firstname=user_name)
    user_exten = user['lines'][0]['extensions'][0]['exten']
    user_context = user['lines'][0]['extensions'][0]['context']
    context.calld_client.applications.make_call_to_node(
        application['uuid'],
        node['uuid'],
        {'exten': user_exten, 'context': user_context},
    )

    phone = context.phone_register.get_phone(user_name)
    phone.answer()


@then('"{app_name}" contains a node with "{n}" calls')
def then_application_contains_node_with_n_calls(context, app_name, n):
    application = context.helpers.application.get_by(name=app_name, recurse=True)
    calls = context.calld_client.applications.list_calls(application['uuid'])['items']
    assert_that(len(calls), equal_to(2))
