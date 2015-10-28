# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
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


def delete_event_by_queue_between(event, queuename, start, end):
    with session_scope():
        queue_log_dao.delete_event_by_queue_between(event, queuename, start, end)


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


def get_last_callid(event, agent_number):
    with session_scope():
        callid = queue_log_dao.get_last_callid_with_event_for_agent(
            event,
            _build_agent_db_tag_from_number(agent_number)
        )
    return callid


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
