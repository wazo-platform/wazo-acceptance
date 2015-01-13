# -*- coding: utf-8 -*-

# Copyright (C) 2014 Avencall
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

from lettuce import world


def get_messages_from_bus(queue_name):
    parameters = pika.ConnectionParameters(host=world.config['xivo_host'])
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    events = []

    def callback(channel, method, props, body):
        unmarshaled_body = json.loads(body)
        events.append(unmarshaled_body)

    channel.basic_consume(callback, queue=queue_name, no_ack=True)
    connection.process_data_events()
    connection.close()

    return events
