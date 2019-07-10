# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import given


@given('there are IVR with infos')
def there_are_ivr_with_infos(context):
    for row in context.table:
        body = row.as_dict()
        context.helpers.ivr.create(body)


@given('the IVR "{name}" choices are')
def the_ivr_choices_are(context, name):
    choices = []
    for row in context.table:
        if row['destination_type'] == 'user':
            firstname, lastname = row['destination_arg'].split(' ', 1)
            confd_user = context.helpers.confd_user.get_by(firstname=firstname, lastname=lastname)
            destination = {
                'type': 'user',
                'user_id': confd_user['id'],
            }
        elif row['destination_type'] == 'none':
            destination = {'type': 'none'}
        else:
            raise AssertionError('unknown destination type {}'.format(row['destination_type']))
        choices.append({'exten': row['exten'], 'destination': destination})

    ivr = context.helpers.ivr.get_by(name=name)
    ivr['choices'] = choices
    context.confd_client.ivr.update(ivr)
