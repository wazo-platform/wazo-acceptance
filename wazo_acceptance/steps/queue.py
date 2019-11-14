# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import when


@when('I create the following queues')
def when_i_create_the_following_queues(context):
    context.table.require_columns(['name', 'exten', 'context'])
    for row in context.table:
        body = {'name': row['name'], 'label': row.get('label')}
        queue = context.helpers.queue.create(body)

        body = {'exten': row['exten'], 'context': row['context']}
        extension = context.helpers.extension.create(body)
        context.helpers.queue.add_extension(queue, extension['id'])

        for agent_number in row.get('agents', '').split(','):
            agent = context.helpers.agent.get_by(number=agent_number)
            context.helpers.queue.add_agent_member(queue, agent['id'])

        queue = context.helpers.queue.create(body)

        body = {'exten': row['exten'], 'context': row['context']}
        extension = context.helpers.extension.create(body)
        context.helpers.queue.add_extension(queue, extension['id'])

        for agent_number in row.get('agents', '').split(','):
            agent = context.helpers.agent.get_by(number=agent_number)
            context.helpers.queue.add_agent_member(queue, agent['id'])
