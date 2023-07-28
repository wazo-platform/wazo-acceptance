# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import given


@given('there are telephony groups with infos')
def given_there_are_telephony_groups_with_infos(context):
    context.table.require_columns(['label'])
    for row in context.table:
        body = row.as_dict()

        group = context.helpers.confd_group.create(body)

        if body.get('exten') and body.get('context'):
            context_name = context.helpers.context.get_by(label=body['context'])['name']
            extension_body = {'exten': body['exten'], 'context': context_name}
            extension = context.helpers.extension.create(extension_body)
            context.helpers.confd_group.add_extension(group, extension)

        if body.get('schedule'):
            schedule = context.helpers.schedule.get_by(name=body['schedule'])
            context.confd_client.groups(group).add_schedule(schedule['id'])

        if body.get('noanswer_destination'):
            type_, name = body['noanswer_destination'].split(':')
            fallbacks_body = {'noanswer_destination': {'type': type_}}
            if type_ == 'group':
                group_dest = context.helpers.confd_group.get_by(label=name)
                fallbacks_body['noanswer_destination']['group_id'] = group_dest['id']
            else:
                raise NotImplementedError(f'Destination not implemented: {type_}')

            context.helpers.confd_group.update_fallbacks(group, fallbacks_body)


@given('the telephony group "{label}" has users')
def given_the_telephony_group_have_user(context, label):
    context.table.require_columns(['firstname', 'lastname'])
    user_members = []
    group = context.helpers.confd_group.get_by(label=label)
    for row in context.table:
        body = row.as_dict()

        user = context.helpers.user.get_by(
            firstname=body['firstname'],
            lastname=body['lastname'],
        )

        user_members.append({'uuid': user['uuid']})

    context.helpers.confd_group.update_user_members(group, user_members)


@given('the telephony group "{label}" has extensions')
def given_the_telephony_group_have_extensions(context, label):
    context.table.require_columns(['context', 'exten'])
    extension_members = []
    group = context.helpers.confd_group.get_by(label=label)
    for row in context.table:
        extension_members.append(row.as_dict())

    context.helpers.confd_group.update_extension_members(group, extension_members)
