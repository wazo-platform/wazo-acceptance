# Copyright 2019-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import when, given


@given('there are queues with infos')
def given_there_are_queues(context):
    context.table.require_columns(['name', 'exten', 'context'])
    for row in context.table:
        body = row.as_dict()
        body['options'] = []
        for option in ('option_timeout', 'option_maxlen', 'option_timeout', 'option_joinempty'):
            value = body.pop(option, None)
            if value is not None:
                option_name = option[7:]
                body['options'].append((option_name, value))
        queue = context.helpers.queue.create(body)

        extension_body = {'exten': body['exten'], 'context': body['context']}
        if row.get('timeout') is not None:
            extension_body['timeout'] = int(row['timeout'])
        extension = context.helpers.extension.create(extension_body)
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

        if row.get('schedule'):
            schedule = context.helpers.schedule.get_by(name=row['schedule'])
            context.confd_client.queues(queue).add_schedule(schedule['id'])


@given('queue "{queue_name}" has agent "{agent_number}" with penalty "{penalty}"')
def given_queue_has_agent_with_penalty(context, queue_name, agent_number, penalty):
    queue = context.helpers.queue.get_by(name=queue_name)
    agent = context.helpers.agent.get_by(number=agent_number)
    context.helpers.queue.add_agent_member(queue, agent, penalty=penalty)


@when('I create the following queues')
def when_i_create_the_following_queues(context):
    context.table.require_columns(['name', 'exten', 'context'])
    for row in context.table:
        body = row.as_dict()
        queue = context.helpers.queue.create(body)

        extension_body = {'exten': body['exten'], 'context': body['context']}
        extension = context.helpers.extension.create(extension_body)
        context.helpers.queue.add_extension(queue, extension)

        if row.get('agents'):
            for agent_number in row['agents'].split(','):
                agent = context.helpers.agent.get_by(number=agent_number)
                context.helpers.queue.add_agent_member(queue, agent)
