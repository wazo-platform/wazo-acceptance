# -*- coding: utf-8 -*-

from lettuce.registry import world
from xivo_ws import Statconf


def create_configuration(config_name, work_start, work_end, queue_name):
    conf = world.ws.statconfs.search(config_name)
    if conf:
        world.ws.statconfs.delete(conf[0].id)
    qid = world.ws.queues.search(queue_name)[0].id

    conf = Statconf(
        name=config_name,
        hour_start=work_start,
        hour_end=work_end,
        queue=[qid],
        dbegcache='2012-01',
        queue_qos=[10],
        monday=True,
        tuesday=True,
        wednesday=True,
        thursday=True,
        friday=True,
        saturday=True,
        sunday=True
        )
    world.ws.statconfs.add(conf)


def regenerate_cache():
    world.ssh_client.check_call(['xivo-stat', 'clean_db'])
    world.ssh_client.check_call(['xivo-stat', 'fill_db'])


def open_queue_stat_page_on_day(queue_name, day, config_name):
    conf_id = world.ws.statconfs.search(config_name)[0].id
    qid = world.ws.queues.search(queue_name)[0].id
    host = world.remote_host

    url = '''https://%s/statistics/call_center/index.php/data/stats1?confid=%s&key=queue-%s&axetype=day&dbeg=%s&dend=%s&dday=%s&dweek=2012-08-17&dmonth=2012-08&dyear=2012''' % (host, conf_id, qid, day, day, day)

    world.browser.get(url)


def check_queue_statistic(stats):
    table = world.browser.find_element_by_id('queue').text
    lines = [l.strip() for l in table.split('\n')]
    headers = lines[1].split(' ')
    values = lines[2:]

    expected_headers = stats[0].keys()[1:]
    expected_values = [stat.values() for stat in stats]

    for row in expected_values:
        matching_result_row = [line for line in values if line.split(' ')[0] == row[0]][0].split(' ')
        for expected_index, column in enumerate(expected_headers):
            index = headers.index(column) + 1
            result = matching_result_row[index]
            expected = row[expected_index + 1]
            assert result == expected, 'Result does not match expectations'
