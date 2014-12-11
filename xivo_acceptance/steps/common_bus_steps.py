# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
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

import json
import pika

from hamcrest import all_of
from hamcrest import assert_that
from hamcrest import equal_to
from hamcrest import has_key
from itertools import count
from lettuce import step
from lettuce.registry import world
from xivo_acceptance.helpers import user_helper
from xivo_acceptance.helpers import xivo_helper

MAGIC_COLUMNS = ['user_id', 'xivo_uuid', 'firstname', 'lastname']


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
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=world.config['xivo_host']))
    channel = connection.channel()
    queue_name = 'test_xivo-cti'

    def callback(ch, method, props, body):
        unmarshaled_body = json.loads(body)
        data = unmarshaled_body['data']['variables']

        for expected_widget in step.hashes:
            widget_name = expected_widget['widget_name']
            widget_value = expected_widget['value']
            assert(unicode(data[widget_name]) == widget_value)

    channel.basic_consume(callback, queue=queue_name, no_ack=True)
    connection.process_data_events()
    connection.close()


@step(u'Then I receive a "([^"]*)" on the bus with data on exchange "([^"]*)":')
def then_i_receive_a_message_on_the_bus_with_data_on_exchange(step, expected_message, exchange):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=world.config['xivo_host']))
    channel = connection.channel()
    queue_name = 'test_{}'.format(exchange)
    counter = count(0)

    def callback(ch, method, props, body):
        unmarshaled_body = json.loads(body)
        assert_that(unmarshaled_body, all_of(has_key('name'),
                                             has_key('data')),
                    'Unexpected body formar {}'.format(unmarshaled_body))
        message = unmarshaled_body['name']
        data = unmarshaled_body['data']

        assert_that(message, equal_to(expected_message),
                    'The received message did not match name {}'.format(expected_message))

        for expected in step.hashes:
            if data_in_expected(expected, data):
                next(counter)
                break


    channel.basic_consume(callback, queue=queue_name, no_ack=True)
    connection.process_data_events()
    connection.close()
    matches = next(counter)
    assert_that(matches, equal_to(len(step.hashes)),
                'Only matches {} in {}'.format(matches, len(step.hashes)))


def _magic_user_match(expected, actual):
    assert_that(expected, all_of(has_key('firstname'),
                                 has_key('lastname')),
                'Precondition for the magic user match not met')

    if expected.get('user_id') == 'yes':
        user = user_helper.get_by_firstname_lastname(expected['firstname'],
                                                     expected['lastname'])
        if not user:
            return False

    if 'firstname' in actual:
        if expected['firstname'] != actual['firstname']:
            return False
    if 'lastname' in actual:
        if expected['lastname'] != actual['lastname']:
            return False

    return True


def _magic_xivo_match(expected, actual):
    if expected.get('xivo_uuid') != 'yes':
        return True

    uuid = xivo_helper.get_uuid()
    for value in actual.itervalues():
        if value == uuid:
            return True
    return False


def data_in_expected(expected, data):
    for key, value in expected.iteritems():
        if key in MAGIC_COLUMNS:
            continue
        if value != data[key]:
            return False

    return _magic_user_match(expected, data) and _magic_xivo_match(expected, data)
