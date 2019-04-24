# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_acceptance.lettuce import postgres


def delete_event_by_queue(event, queuename):
    pg_command = 'DELETE FROM queue_log WHERE queuename = \'%s\' and event = \'%s\'' % (queuename, event)
    postgres.exec_sql_request(pg_command)


def delete_event_by_agent_number(event, agent_number):
    agent_number = _build_agent_db_tag_from_number(agent_number)
    pg_command = 'DELETE FROM queue_log WHERE agent = \'%s\' and event = \'%s\'' % (agent_number, event)
    postgres.exec_sql_request(pg_command)


def insert_corrupt_data():
    pg_command = 'INSERT INTO queue_log(time, callid, queuename, agent, event, data1) VALUES (cast (localtimestamp - interval \'1 hour\' as text), \'test_exitwithtimeout\', \'q1\', \'NONE\', \'EXITWITHTIMEOUT\', \'1\')'
    postgres.exec_sql_request(pg_command)


def get_event_count_queue(event, queuename):
    cond = {
        '"queuename"': '\'%s\'' % queuename,
        '"event"': '\'%s\'' % event
    }
    return postgres.exec_count_request('queue_log', **cond)


def get_event_count_agent(event, agent_number):
    cond = {
        '"agent"': '\'%s\'' % _build_agent_db_tag_from_number(agent_number),
        '"event"': '\'%s\'' % event
    }
    return postgres.exec_count_request('queue_log', **cond)


def _build_agent_db_tag_from_number(agent_number):
    return 'Agent/%s' % agent_number
