# -*- coding: utf-8 -*-

# Copyright (C) 2014-2016 Avencall
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

import time

from kombu import Connection, Queue, Exchange, Consumer

from lettuce import world

_queues = {}


def add_binding(queue_name, routing_key, exchange_name=None):
    exchange_name = exchange_name or world.config['bus']['exchange_name']
    exchange = Exchange(exchange_name, type=world.config['bus']['exchange_type'])
    with Connection(world.config['bus_url']) as conn:
        queue = Queue(queue_name, exchange=exchange, routing_key=routing_key,
                      channel=conn.channel())
        queue.declare()
        queue.purge()
        _queues[queue_name] = queue


def get_messages_from_bus(queue_name):
    events = []

    def on_event(body, message):
        events.append(body)
        message.ack()

    with Connection(world.config['bus_url']) as conn:
        with Consumer(conn, [_queues[queue_name]], callbacks=[on_event]):
            try:
                end = time.time() + 3
                while time.time() < end:
                    conn.drain_events(timeout=1)
            except Exception:  # timeout
                pass

    return events
