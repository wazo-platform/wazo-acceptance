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

        uri = 'postgresql://asterisk:proformatique@%s/asterisk' % world.remote_host
        dbconnection.add_connection_as(uri, 'asterisk')

    def __exit__(self, t, v, tr):
        dbconnection.unregister_db_connection_pool()


def create_pgpass_on_remote_host():
    cmd = ['echo', '*:*:asterisk:asterisk:proformatique', '>', '.pgpass']
    world.ssh_client.check_call(cmd)
    cmd = ['chmod', '600', '.pgpass']
    world.ssh_client.check_call(cmd)


def delete_event_by_queue(event, queuename):
    create_pgpass_on_remote_host()
    pg_command = '"DELETE FROM queue_log WHERE queuename = \'%s\' and event = \'%s\'"' % (queuename, event)
    command = ['psql', '-h', 'localhost', '-U', 'asterisk', '-c', pg_command]
    world.ssh_client.check_call(command)


def delete_event_by_queue_between(event, queuename, start, end):
    with asterisk_connection():
        queue_log_dao.delete_event_by_queue_between(event, queuename, start, end)


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


def get_event_count_queue(event, queuename):
    create_pgpass_on_remote_host()
    pg_command = '"SELECT COUNT(*) FROM queue_log WHERE queuename = \'%s\' and event = \'%s\'"' % (queuename, event)
    command = ['psql', '-h', 'localhost', '-U', 'asterisk', '-c', pg_command]
    res = world.ssh_client.out_call(command)
    return int(res.split('\n')[-4].strip())
