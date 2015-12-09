# -*- coding: utf-8 -*-

# Copyright (C) 2013-2015 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import logging
import json

from kombu import Connection, Exchange, Producer

from hamcrest import all_of
from hamcrest import assert_that
from hamcrest import has_entry
from hamcrest import has_entries
from hamcrest import has_item
from hamcrest import matches_regexp
from lettuce import step
from lettuce.registry import world
from xivo_acceptance.helpers import agent_helper
from xivo_acceptance.helpers import bus_helper
from xivo_acceptance.helpers import user_helper
from xivo_acceptance.helpers import line_read_helper
from xivo_acceptance.helpers import xivo_helper
from xivo_bus import Marshaler
from xivo_bus.resources.cti.event import UserStatusUpdateEvent
from xivo_bus.resources.chat.event import ChatMessageEvent


logger = logging.getLogger('acceptance')


def _send_bus_msg(msg, routing_key):
    exchange = Exchange(world.config['bus']['exchange_name'],
                        type=world.config['bus']['exchange_type'])
    with Connection(world.config['bus_url']) as conn:
        producer = Producer(conn, exchange)
        producer.publish(msg, routing_key=routing_key)


@step(u'When I publish the following message on "([^"]*)":')
def when_i_publish_the_following_message_on_group1(step, routing_key):
    msg = json.dumps(json.loads(step.multiline))  # Clean white spaces
    _send_bus_msg(msg, routing_key)


@step(u'When I publish a chat message:')
def when_i_publish_a_chat_message(step):
    data = step.hashes[0]
    local_xivo_uuid = xivo_helper.get_uuid()
    user_id = user_helper.get_by_firstname_lastname(data['firstname'], data['lastname'])['id']
    to = local_xivo_uuid, user_id
    event = ChatMessageEvent(json.loads(data['from']), to, data['alias'], data['msg'])
    msg = Marshaler(local_xivo_uuid).marshal_message(event)
    _send_bus_msg(msg, event.routing_key)


@step(u'When I publish a "([^"]*)" on the "([^"]*)" routing key with info:')
def when_i_publish_a_event_on_the_routing_key_with_info(step, message, routing_key):
    data = step.hashes[0]
    marshaler = Marshaler(xivo_helper.get_uuid())
    msg = marshaler.marshal_message(UserStatusUpdateEvent(data['xivo_id'], data['user_id'], data['status']))
    _send_bus_msg(msg, routing_key)


@step(u'Given I listen on the bus for messages:')
def given_i_listen_on_the_bus_for_messages(step):
    for entry in step.hashes:
        queue_name = entry['queue'].encode('ascii')
        routing_key = entry['routing_key'].encode('ascii')
        bus_helper.add_binding(queue_name, routing_key)


@step(u'Then I see a message in queue "([^"]*)" with the following variables:')
def then_i_see_a_message_on_bus_with_the_following_variables(step, queue):
    events = bus_helper.get_messages_from_bus(queue)

    for event in events:
        data = event['data']['variables']

        for expected_widget in step.hashes:
            widget_name = expected_widget['widget_name']
            widget_value = expected_widget['value']
            assert(unicode(data[widget_name]) == widget_value)


@step(u'Then I see an AMI message "([^"]*)" on the queue "([^"]*)":')
def then_i_see_an_ami_message_on_the_queue(step, event_name, queue):
    events = bus_helper.get_messages_from_bus(queue)

    matcher_dict = dict((event_line['header'], matches_regexp(event_line['value']))
                        for event_line in step.hashes)

    assert_that(events, has_item(all_of(has_entry('name', event_name),
                                        has_entry('data', has_entries(matcher_dict)))))


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

        if expected_event.get('endpoint_id', 'no') == 'yes':
            line = line_read_helper.get_with_exten_context(expected_event['number'],
                                                           expected_event['context'])
            raw_expected_event['data']['endpoint_id'] = line['id']
            raw_expected_event['data']['status'] = int(expected_event['status'])

        if expected_event.get('agent_id', 'no') == 'yes':
            agent_id = agent_helper.find_agent_id_with_number(expected_event['agent_number'])
            raw_expected_event['data']['agent_id'] = agent_id

        if expected_event.get('from', 'no') == 'yes':
            user = user_helper.get_by_firstname_lastname(expected_event['firstname'],
                                                         expected_event['lastname'])
            from_ = [local_xivo_uuid, user['id']]
            raw_expected_event['data']['from'] = from_

        assert_that(events, has_item(has_entries(raw_expected_event)))
