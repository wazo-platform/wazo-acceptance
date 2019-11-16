# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import when, given


@given('there are queues with infos')
def given_there_are_queues(context):
    context.table.require_columns(['name', 'exten', 'context'])
    for row in context.table:
        body = {'name': row['name'], 'label': row.get('label')}
        queue = context.helpers.queue.create(body)

        body = {'exten': row['exten'], 'context': row['context']}
        extension = context.helpers.extension.create(body)
        context.helpers.queue.add_extension(queue, extension)

        if row.get('agents'):
            for agent_number in row['agents'].split(','):
                agent = context.helpers.agent.get_by(number=agent_number)
                context.helpers.queue.add_agent_member(queue, agent)

        if row.get('users'):
            for user_extension in row['users'].split(','):
                exten, exten_context = user_extension.split('@')
                user = context.helpers.confd_user.get_by(exten=exten, context=exten_context)
                context.helpers.queue.add_user_member(queue, user)


@when('I create the following queues')
def when_i_create_the_following_queues(context):
    context.table.require_columns(['name', 'exten', 'context'])
    for row in context.table:
        body = {'name': row['name'], 'label': row.get('label')}
        queue = context.helpers.queue.create(body)

        body = {'exten': row['exten'], 'context': row['context']}
        extension = context.helpers.extension.create(body)
        context.helpers.queue.add_extension(queue, extension)

        if row.get('agents'):
            for agent_number in row['agents'].split(','):
                agent = context.helpers.agent.get_by(number=agent_number)
                context.helpers.queue.add_agent_member(queue, agent)
