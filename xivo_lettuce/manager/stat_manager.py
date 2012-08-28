# -*- coding: utf-8 -*-

from lettuce.registry import world
from xivo_ws import Statconf


def create_configuration(config_name, work_start, work_end, queue_name, agent_number=None):
    conf = world.ws.statconfs.search(config_name)
    if conf:
        world.ws.statconfs.delete(conf[0].id)
    qid = world.ws.queues.search(queue_name)[0].id
    agent_id = world.ws.agent.search(agent_number)[0].id

    conf = Statconf(
        name=config_name,
        hour_start=work_start,
        hour_end=work_end,
        queue=[qid],
        agent=[agent_id],
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
    world.ssh_client_xivo.check_call(['xivo-stat', 'clean_db'])
    world.ssh_client_xivo.check_call(['xivo-stat', 'fill_db'])


def open_queue_stat_page_on_day(queue_name, day, config_name):
    conf_id = world.ws.statconfs.search(config_name)[0].id
    qid = world.ws.queues.search(queue_name)[0].id
    host = world.xivo_host

    url = '''https://%s/statistics/call_center/index.php/data/stats1?confid=%s&key=queue-%s&axetype=day&dbeg=%s&dend=%s&dday=%s&dweek=2012-08-17&dmonth=2012-08&dyear=2012''' % (host, conf_id, qid, day, day, day)

    world.browser.get(url)


def open_agent_stat_page_on_day(agent_number, day, config_name):
    conf_id = world.ws.statconfs.search(config_name)[0].id
    agent_id = world.ws.agents.search(agent_number)[0].id
    host = world.xivo_host

    url = '''https://%s/statistics/call_center/index.php/data/stats2?confid=%s&key=agent-%s&axetype=day&dbeg=%s&dend=%s&dday=%s&dweek=2012-08-17&dmonth=2012-08&dyear=2012''' % (host, conf_id, agent_id, day, day, day)

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


def check_agent_statistic(stats):
    table = world.browser.find_element_by_id('agent').text
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
