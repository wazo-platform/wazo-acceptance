# -*- coding: utf-8 -*-

from lettuce.registry import world


def delete_event_by_queue(event, queuename):
    print 'deleting %s on %s' % (event, queuename)
    pg_command = '"DELETE FROM queue_log WHERE queuename = \'%s\' and event = \'%s\'"' % (queuename, event)
    command = ['psql', '-h', 'localhost', '-U', 'asterisk', '-c', pg_command]
    print world.ssh_client.check_call(command)


def get_event_count_queue(event, queuename):
    pg_command = '"SELECT COUNT(*) FROM queue_log WHERE queuename = \'%s\' and event = \'%s\'"' % (queuename, event)
    command = ['psql', '-h', 'localhost', '-U', 'asterisk', '-c', pg_command]
    res = world.ssh_client.out_call(command)
    return int(res.split('\n')[2].strip())
