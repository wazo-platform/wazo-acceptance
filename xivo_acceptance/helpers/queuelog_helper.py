# -*- coding: utf-8 -*-
# Copyright (C) 2013-2016 Avencall
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_acceptance.lettuce import postgres
from xivo_dao import queue_log_dao
from xivo_dao.helpers.db_utils import session_scope


def delete_event_by_queue(event, queuename):
    pg_command = 'DELETE FROM queue_log WHERE queuename = \'%s\' and event = \'%s\'' % (queuename, event)
    postgres.exec_sql_request(pg_command)


def delete_event_by_agent_number(event, agent_number):
    agent_number = _build_agent_db_tag_from_number(agent_number)
    pg_command = 'DELETE FROM queue_log WHERE agent = \'%s\' and event = \'%s\'' % (agent_number, event)
    postgres.exec_sql_request(pg_command)


def delete_event_between(start, end):
    with session_scope():
        queue_log_dao.delete_event_between(start, end)


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


def get_agent_last_login_duration(agent_number):
    query = "SELECT cast(data2 as int) FROM queue_log WHERE event = 'AGENTCALLBACKLOGOFF' AND agent = :agent ORDER BY time DESC LIMIT 1"
    agent = _build_agent_db_tag_from_number(agent_number)
    return postgres.exec_sql_request(query, agent=agent).fetchone()[0]


def _build_agent_db_tag_from_number(agent_number):
    return 'Agent/%s' % agent_number


def insert_entries(entries):
    with session_scope():
        for entry in entries:
            queue_log_dao.insert_entry(
                entry['time'],
                entry['callid'],
                entry['queuename'],
                entry['agent'],
                entry['event'],
                entry['data1'],
                entry['data2'],
                entry['data3'],
                entry['data4'],
                entry['data5']
            )
