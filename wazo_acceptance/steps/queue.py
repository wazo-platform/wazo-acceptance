# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import when


@when('I create the following queues')
def when_i_create_the_following_queues(context):
    context.table.require_columns(['name', 'exten', 'context'])
    for row in context.table:
        body = {
            'name': row['name'].lower(),
            'label': row['display_name'],
            'options': []
        }
        if 'maxlen' in row:
            body['options'].append(['maxlen', row['maxlen']])
        if 'joinempty' in row:
            body['options'].append(['joinempty', row['joinempty']])
        if 'leavewhenempty' in row:
            body['options'].append(['leavewhenempty', row['leavewhenempty']])
        if 'ringing_time' in row:
            body['timeout'] = row['ringing_time']
        if 'wrapuptime' in row:
            body['options'].append(['wrapuptime', row['wrapuptime']])
        if 'reachability_timeout' in row:
            body['options'].append(['timeout', row['reachability_timeout']])
        if 'ring_strategy' in row:
            body['options'].append(['strategy', row['ring_strategy']])

        queue = context.helpers.queue.create(body)

        body = {'exten': row['exten'], 'context': row['context']}
        extension = context.helpers.extension.create(body)
        context.helpers.queue.add_extension(queue, extension['id'])

        for agent_number in row.get('agents', '').split(','):
            agent = context.helpers.agent.get_by(number=agent_number)
            context.helpers.queue.add_agent_member(queue, agent['id'])
