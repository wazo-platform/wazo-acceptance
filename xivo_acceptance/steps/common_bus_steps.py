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

from hamcrest import assert_that
from hamcrest import has_entries
from hamcrest import has_item
from lettuce import step
from lettuce.registry import world
from xivo_acceptance.helpers import bus_helper
from xivo_acceptance.helpers import user_helper
from xivo_acceptance.helpers import line_helper
from xivo_acceptance.helpers import xivo_helper


logger = logging.getLogger('acceptance')


@step(u'Given I listen on the bus for messages:')
def given_i_listen_on_the_bus_for_messages(step):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=world.config['xivo_host']))
    channel = connection.channel()

    for entry in step.hashes:
        try:
            exchange = entry['exchange'].encode('ascii')
            routing_key = entry['routing_key'].encode('ascii')
            queue_name = 'test_{}'.format(exchange)
            result = channel.queue_declare(queue=queue_name)
            queue_name = result.method.queue

            channel.queue_bind(exchange=exchange,
                               queue=queue_name,
                               routing_key=routing_key)
        finally:
            connection.close()


@step(u'Then I see a message on bus with the following variables:')
def then_i_see_a_message_on_bus_with_the_following_variables(step):
    events = bus_helper.get_messages_from_bus(exchange='xivo-cti')

    for event in events:
        data = event['data']['variables']

        for expected_widget in step.hashes:
            widget_name = expected_widget['widget_name']
            widget_value = expected_widget['value']
            assert(unicode(data[widget_name]) == widget_value)


@step(u'Then I receive a "([^"]*)" on the bus exchange "([^"]*)" with data:')
def then_i_receive_a_message_on_the_bus_with_data_on_exchange(step, expected_message, exchange):
    events = bus_helper.get_messages_from_bus(exchange)

    for expected_event in step.hashes:
        raw_expected_event = {'name': expected_message,
                              'data': {}}

        if expected_event.get('user_id') == 'yes':
            user = user_helper.get_by_firstname_lastname(expected_event['firstname'],
                                                         expected_event['lastname'])
            raw_expected_event['data']['user_id'] = user.id
            raw_expected_event['data']['status'] = expected_event['status']

        if expected_event.get('endpoint_id') == 'yes':
            line = line_helper.find_with_exten_context(expected_event['number'],
                                                       expected_event['context'])
            raw_expected_event['data']['endpoint_id'] = line.id
            raw_expected_event['data']['status'] = int(expected_event['status'])

        raw_expected_event['data']['xivo_id'] = xivo_helper.get_uuid()

        assert_that(events, has_item(has_entries(raw_expected_event)))
