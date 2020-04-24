# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import json

from hamcrest import (
    assert_that,
    has_entries,
    has_item,
)
from mock import ANY
from lettuce import step
from xivo_acceptance.helpers import (
    agent_helper,
    bus_helper,
    line_read_helper,
    user_helper,
    xivo_helper,
)

logger = logging.getLogger('acceptance')


@step(u'Given I listen on the bus for messages:')
def given_i_listen_on_the_bus_for_messages(step):
    for entry in step.hashes:
        queue_name = entry['queue'].encode('ascii')
        routing_key = entry['routing_key'].encode('ascii')
        bus_helper.add_binding(queue_name, routing_key)


@step(u'Then I receive a "([^"]*)" on the queue "([^"]*)" with data:')
def then_i_receive_a_message_on_the_queue_with_data(step, expected_message, queue):
    events = bus_helper.get_messages_from_bus(queue)
    local_xivo_uuid = xivo_helper.get_uuid()

    for expected_event in step.hashes:
        raw_expected_event = {'name': expected_message,
                              'data': {}}

        if 'status' in expected_event:
            raw_expected_event['data']['status'] = expected_event['status']
        if 'to' in expected_event:
            raw_expected_event['data']['to'] = json.loads(expected_event['to'])
        if 'alias' in expected_event:
            raw_expected_event['data']['alias'] = expected_event['alias']
        if 'msg' in expected_event:
            raw_expected_event['data']['msg'] = expected_event['msg']

        if expected_event.get('origin_uuid', 'no') == 'yes':
            raw_expected_event['origin_uuid'] = local_xivo_uuid

        if expected_event.get('user_id', 'no') == 'yes':
            user = user_helper.get_by_firstname_lastname(expected_event['firstname'],
                                                         expected_event['lastname'])
            raw_expected_event['data']['user_id'] = user['id']

        if expected_event.get('user_uuid', 'no') == 'yes':
            user = user_helper.get_by_firstname_lastname(expected_event['firstname'],
                                                         expected_event['lastname'])
            raw_expected_event['data']['user_uuid'] = user['uuid']

        if expected_event.get('user_uuid', 'no') == 'ANY':
            raw_expected_event['data']['user_uuid'] = ANY

        if expected_event.get('id', 'no') == 'ANY':
            raw_expected_event['data']['id'] = ANY

        if expected_event.get('uuid', 'no') == 'ANY':
            raw_expected_event['data']['uuid'] = ANY

        if expected_event.get('endpoint_id', 'no') == 'yes':
            line = line_read_helper.get_with_exten_context(expected_event['number'],
                                                           expected_event['context'])
            raw_expected_event['data']['endpoint_id'] = line['id']
            raw_expected_event['data']['status'] = int(expected_event['status'])

        if expected_event.get('agent_id', 'no') == 'yes':
            agent_id = agent_helper.find_agent_by(number=expected_event['agent_number'])['id']
            raw_expected_event['data']['agent_id'] = agent_id

        if expected_event.get('from', 'no') == 'yes':
            user = user_helper.get_by_firstname_lastname(expected_event['firstname'],
                                                         expected_event['lastname'])
            from_ = [local_xivo_uuid, user['uuid']]
            raw_expected_event['data']['from'] = from_

        if expected_event.get('call_id') == 'ANY':
            raw_expected_event['data']['call_id'] = ANY

        assert_that(events, has_item(has_entries(raw_expected_event)))
