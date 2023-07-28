# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import (
    assert_that,
    contains_inanyorder,
    has_entries,
)

from behave import (
    given,
    then,
    when,
)


@given('there are conference rooms with infos')
def given_there_are_conference_rooms(context):
    for row in context.table:
        body = row.as_dict()
        body['context'] = context.helpers.context.get_by(label=body['context'])['name']
        conference = context.helpers.conference.create(body)
        extension = context.helpers.extension.create(body)
        context.helpers.conference.add_extension(conference, extension)


@when('the user lists conference rooms using wazo-dird')
def when_user_list_conference_rooms(context):
    token = context.helpers.token.create(context.username, context.password)['token']
    backend = 'conference'
    response = context.dird_client.directories.list_sources(
        profile='default',
        backend=backend,
        token=token,
    )
    context.conference_contacts = []
    for source in response['items']:
        contacts = context.dird_client.backends.list_contacts_from_source(
            backend,
            source['uuid'],
            token=token,
        )['items']

        for contact in contacts:
            context.conference_contacts.append(contact)


@then('the conference rooms list contains')
def then_the_conference_rooms_list_contains(context):
    name_numbers = []
    for row in context.conference_contacts:
        for extension in row['extensions']:
            name_numbers.append({
                'name': row['name'],
                'exten': extension['exten'],
            })

    expected = [has_entries(row.as_dict()) for row in context.table]
    assert_that(name_numbers, contains_inanyorder(*expected))
