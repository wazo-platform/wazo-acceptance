# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step

from xivo_acceptance.helpers import (
    agent_helper,
    queue_helper,
    schedule_helper,
    user_helper,
)


@step(u'^Given there are queues with infos:$')
def given_there_are_queues_with_infos(step):
    for info in step.hashes:
        queue_data = dict(info)

        if queue_data.get('users_number'):
            queue_data['users'] = convert_user_numbers(queue_data.pop('users_number'), queue_data['context'])

        if queue_data.get('agents_number'):
            queue_data['agents'] = convert_agent_numbers(queue_data.pop('agents_number'))

        if queue_data.get('schedule_name'):
            queue_data['schedule_id'] = convert_schedule_name(queue_data.pop('schedule_name'))

        queue_helper.add_or_replace_queue(queue_data)


def convert_user_numbers(user_numbers, context):
    users = []
    user_number_list = user_numbers.split(',')
    for user_number in user_number_list:
        user = user_helper.find_by_exten_context(user_number, context)
        if user:
            users.append(user['id'])
    return users


def convert_agent_numbers(agent_numbers):
    agent_ids = []
    agent_number_list = agent_numbers.split(',')
    for agent_number in agent_number_list:
        agent_id = agent_helper.find_agent_by(number=agent_number.strip())['id']
        agent_ids.append(agent_id)
    return agent_ids


def convert_schedule_name(schedule_name):
    schedule_id = schedule_helper.get_schedule_by(name=schedule_name)
    return schedule_id
