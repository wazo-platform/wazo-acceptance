# Copyright 2019-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import given


@given('there are telephony groups with infos')
def given_there_are_telephony_groups_with_infos(context):
    context.table.require_columns(['name'])
    for row in context.table:
        body = row.as_dict()

        group = context.helpers.confd_group.create(body)

        if body.get('exten') and body.get('context'):
            extension = context.helpers.extension.create(body)
            context.helpers.confd_group.add_extension(group, extension)

        if body.get('schedule'):
            schedule = context.helpers.schedule.get_by(name=body['schedule'])
            context.confd_client.groups(group).add_schedule(schedule['id'])

        if body.get('noanswer_destination'):
            type_, name = body['noanswer_destination'].split(':')
            fallbacks_body = {'noanswer_destination': {'type': type_}}
            if type_ == 'group':
                group_dest = context.helpers.confd_group.get_by(name=name)
                fallbacks_body['noanswer_destination']['group_id'] = group_dest['id']
            else:
                raise NotImplementedError('Destination not implemented: {}'.format(type_))

            context.helpers.confd_group.update_fallbacks(group, fallbacks_body)


@given('the telephony group "{name}" has users')
def given_the_telephony_group_have_user(context, name):
    context.table.require_columns(['firstname', 'lastname'])
    user_members = []
    group = context.helpers.confd_group.get_by(name=name)
    for row in context.table:
        body = row.as_dict()

        user = context.helpers.user.get_by(
            firstname=body['firstname'],
            lastname=body['lastname'],
        )

        user_members.append({'uuid': user['uuid']})

    context.helpers.confd_group.update_user_members(group, user_members)


@given('the telephony group "{name}" has extensions')
def given_the_telephony_group_have_extensions(context, name):
    context.table.require_columns(['context', 'exten'])
    extension_members = []
    group = context.helpers.confd_group.get_by(name=name)
    for row in context.table:
        extension_members.append(row.as_dict())

    context.helpers.confd_group.update_extension_members(group, extension_members)
