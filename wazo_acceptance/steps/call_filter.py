# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
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
            if ',' in body['recipients']:
                raise NotImplementedError('Many recipients not implemented')
            user = context.helpers.confd_user.get_by(search=body['recipients'])
            users = [user]
            context.confd_client.call_filters(call_filter).update_user_recipients(users)

        if body.get('surrogates'):
            if ',' in body['surrogates']:
                raise NotImplementedError('Many surrogates not implemented')
            user = context.helpers.confd_user.get_by(search=body['surrogates'])
            users = [user]
            context.confd_client.call_filters(call_filter).update_user_surrogates(users)
