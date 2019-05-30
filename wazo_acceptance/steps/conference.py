# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import (
    assert_that,
    contains_inanyorder,
)

from behave import (
    given,
    then,
    when,
)


@given('there are conference rooms with infos')
def there_are_conference_rooms(context):
    for row in context.table:
        body = dict(zip(row.headings, row.cells))
        conference = context.helpers.conference.create(body)
        extension = context.helpers.extension.create(body)
        context.helpers.conference.add_extension(conference, extension)


@when('the user lists conference rooms')
def user_list_conference_rooms(context):
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


@then(u'the conference rooms list contains')
def the_conference_rooms_list_contains(context):
    name_numbers = []
    for row in context.conference_contacts:
        for extension in row['extensions']:
            name_numbers.append({
                'name': row['name'],
                'exten': extension['exten'],
            })

    expected = list(dict(zip(row.headings, row.cells)) for row in context.table)
    assert_that(name_numbers, contains_inanyorder(*expected))
