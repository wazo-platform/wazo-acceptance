# Copyright 2020-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import given


@given('there are call permissions with infos')
def given_there_are_call_permissions_with_infos(context):
    context.table.require_columns(['name'])
    for row in context.table:
        body = row.as_dict()

        body['extensions'] = body['extensions'].split(',')
        call_permission = context.helpers.call_permission.create(body)

        if body.get('users'):
            for name in body.get('users').split(','):
                user = context.helpers.confd_user.get_by(search=name)
                context.confd_client.call_permissions(call_permission).add_user(user)

        if body.get('groups'):
            for name in body.get('groups').split(','):
                group = context.helpers.confd_group.get_by(search=name)
                context.confd_client.groups(group).add_call_permission(call_permission)
