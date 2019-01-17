# -*- coding: utf-8 -*-
# Copyright (C) 2014-2016 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

import time

from kombu import Connection, Queue, Exchange, Consumer

from lettuce import world

_queues = {}

COLLECTD_EXCHANGE = Exchange('collectd', type='topic', durable=False, arguments={'auto_delete': True})


def add_binding(queue_name, routing_key, exchange=None):
    exchange = exchange or Exchange(world.config['bus']['exchange_name'],
                                    type=world.config['bus']['exchange_type'])
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
