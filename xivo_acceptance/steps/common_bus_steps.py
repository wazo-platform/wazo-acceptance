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

import pika
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
from xivo_acceptance.helpers import line_helper
from xivo_acceptance.helpers import xivo_helper
from xivo_bus import Marshaler
from xivo_bus.resources.cti.event import UserStatusUpdateEvent


logger = logging.getLogger('acceptance')


def _send_bus_msg(msg, routing_key):
    bus_url = 'amqp://{username}:{password}@{host}:{port}//'.format(**world.config['bus'])
    exchange = Exchange(world.config['bus']['exchange_name'],
                        type=world.config['bus']['exchange_type'])
    with Connection(bus_url) as conn:
        producer = Producer(conn, exchange)
        producer.publish(json.dumps(msg, routing_key=routing_key))


@step(u'When I publish the following message on "([^"]*)":')
def when_i_publish_the_following_message_on_group1(step, routing_key):
    msg = json.dumps(json.loads(step.multiline))  # Clean white spaces
    _send_bus_msg(msg, routing_key)


@step(u'When I publish a "([^"]*)" on the "([^"]*)" routing key with info:')
def when_i_publish_a_event_on_the_routing_key_with_info(step, message, routing_key):
    data = step.hashes[0]
    marshaler = Marshaler()
    msg = marshaler.marshal_message(UserStatusUpdateEvent(data['xivo_id'], data['user_id'], data['status']))
    _send_bus_msg(msg, routing_key)


@step(u'Given I listen on the bus for messages:')
def given_i_listen_on_the_bus_for_messages(step):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=world.config['xivo_host']))
    channel = connection.channel()

    for entry in step.hashes:
        try:
            exchange = world.config['bus']['exchange_name']
            queue_name = entry['queue'].encode('ascii')
            routing_key = entry['routing_key'].encode('ascii')
            result = channel.queue_declare(queue=queue_name)

            channel.queue_purge(queue=queue_name)
            channel.queue_bind(exchange=exchange,
                               queue=queue_name,
                               routing_key=routing_key)
            bus_helper.get_messages_from_bus(queue_name)
        finally:
            connection.close()


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

    for expected_event in step.hashes:
        raw_expected_event = {'name': expected_message,
                              'data': {}}

        raw_expected_event['data']['xivo_id'] = xivo_helper.get_uuid()
        raw_expected_event['data']['status'] = expected_event['status']

        if expected_event.get('user_id', 'no') == 'yes':
            user = user_helper.get_by_firstname_lastname(expected_event['firstname'],
                                                         expected_event['lastname'])
            raw_expected_event['data']['user_id'] = user.id

        if expected_event.get('endpoint_id', 'no') == 'yes':
            line = line_helper.find_with_exten_context(expected_event['number'],
                                                       expected_event['context'])
            raw_expected_event['data']['endpoint_id'] = line.id
            raw_expected_event['data']['status'] = int(expected_event['status'])

        if expected_event.get('agent_id', 'no') == 'yes':
            agent_id = agent_helper.find_agent_id_with_number(expected_event['agent_number'])
            raw_expected_event['data']['agent_id'] = agent_id

        assert_that(events, has_item(has_entries(raw_expected_event)))
