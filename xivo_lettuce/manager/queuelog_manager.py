# -*- coding: utf-8 -*-

from lettuce.registry import world
from xivo_dao import queue_log_dao
from xivo_dao.alchemy import dbconnection


class asterisk_connection(object):
    '''
    Context manager to be able to use xivo-dao

    Usage:
        with asterisk_connection():
            dao.function(...)
    '''

    def __enter__(self):
        db_connection_pool = dbconnection.DBConnectionPool(dbconnection.DBConnection)
        dbconnection.register_db_connection_pool(db_connection_pool)

        uri = 'postgresql://asterisk:proformatique@%s/asterisk' % world.xivo_host
        dbconnection.add_connection_as(uri, 'asterisk')

    def __exit__(self, t, v, tr):
        dbconnection.unregister_db_connection_pool()


def delete_event_by_queue(event, queuename):
    pg_command = '"DELETE FROM queue_log WHERE queuename = \'%s\' and event = \'%s\'"' % (queuename, event)
    _exec_pgsql_request(pg_command)


def delete_event_by_agent_number(event, agent_number):
    agent_number = _build_agent_db_tag_from_number(agent_number)
    pg_command = '"DELETE FROM queue_log WHERE agent = \'%s\' and event = \'%s\'"' % (agent_number, event)
    _exec_pgsql_request(pg_command)


def delete_event_by_queue_between(event, queuename, start, end):
    with asterisk_connection():
        queue_log_dao.delete_event_by_queue_between(event, queuename, start, end)


def delete_event_between(start, end):
    with asterisk_connection():
        queue_log_dao.delete_event_between(start, end)


def get_event_count_queue(event, queuename):
    pg_command = '"SELECT COUNT(*) FROM queue_log WHERE queuename = \'%s\' and event = \'%s\'"' % (queuename, event)
    res = _exec_pgsql_request_with_return(pg_command)
    return int(res.split('\n')[-4].strip())


def get_event_count_agent(event, agent_number):
    agent_number = _build_agent_db_tag_from_number(agent_number)
    pg_command = '"SELECT COUNT(*) FROM queue_log WHERE agent = \'%s\' and event = \'%s\'"' % (agent_number, event)
    res = _exec_pgsql_request_with_return(pg_command)
    return int(res.split('\n')[-4].strip())


def _build_agent_db_tag_from_number(agent_number):
    return 'Agent/%s' % agent_number


def _exec_pgsql_request(pg_command):
    command = ['psql', '-h', 'localhost', '-U', 'asterisk', '-c', pg_command]
    world.ssh_client_xivo.check_call(command)


def _exec_pgsql_request_with_return(pg_command):
    command = ['psql', '-h', 'localhost', '-U', 'asterisk', '-c', pg_command]
    return world.ssh_client_xivo.out_call(command)


def insert_entries(entries):
    with asterisk_connection():
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
