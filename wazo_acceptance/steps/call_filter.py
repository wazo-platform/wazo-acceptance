# Copyright 2020-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import given


@given('there are call filters with infos')
def given_there_are_call_filters_with_infos(context):
    context.table.require_columns(['name', 'strategy'])
    for row in context.table:
        body = row.as_dict()
        body.setdefault('source', 'all')

        call_filter = context.helpers.call_filter.create(body)

        if body.get('recipients'):
            users = []
            timeout = body.pop('recipients_timeout', None)
            for recipient in body['recipients'].split(','):
                user = context.helpers.confd_user.get_by(search=recipient)
                user['timeout'] = timeout
                users.append(user)
            context.confd_client.call_filters(call_filter).update_user_recipients(users)

        if body.get('surrogates'):
            users = []
            for surrogate in body['surrogates'].split(','):
                user = context.helpers.confd_user.get_by(search=surrogate)
                users.append(user)
            context.confd_client.call_filters(call_filter).update_user_surrogates(users)
