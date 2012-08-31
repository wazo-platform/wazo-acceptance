# -*- coding: utf-8 -*-

from lettuce.registry import world
from xivo_lettuce.manager_ws import agent_manager_ws, queue_manager_ws, \
    statconfs_manager_ws
import copy


def regenerate_cache():
    world.ssh_client_xivo.check_call(['xivo-stat', 'clean_db'])
    world.ssh_client_xivo.check_call(['xivo-stat', 'fill_db'])


def open_queue_stat_page_on_day(queue_name, day, config_name):
    conf_id = statconfs_manager_ws.get_conf_id_with_name(config_name)
    queue_id = queue_manager_ws.get_queue_id_with_queue_name(queue_name)
    host = world.xivo_host

    uri = '''https://%s/statistics/call_center/index.php/data/stats1''' % host
    qry = '''confid=%s&key=queue-%s&axetype=day&dbeg=%s&dend=%s&dday=%s&dweek=2012-08-17&dmonth=2012-08&dyear=2012''' % (conf_id, queue_id, day, day, day)

    url = '%s?%s' % (uri, qry)

    world.browser.get(url)


def open_agent_stat_page_on_day(agent_number, day, config_name):
    conf_id = statconfs_manager_ws.get_conf_id_with_name(config_name)
    agent_id = agent_manager_ws.get_agent_id_with_number(agent_number)
    host = world.xivo_host

    uri = '''https://%s/statistics/call_center/index.php/data/stats2''' % host
    qry = '''confid=%s&key=agent-%s&axetype=day&dbeg=%s&dend=%s&dday=%s&dweek=2012-08-17&dmonth=2012-08&dyear=2012''' % (conf_id, agent_id, day, day, day)

    url = '%s?%s' % (uri, qry)

    world.browser.get(url)


def check_queue_statistic(stats):
    table = world.browser.find_element_by_id('queue')
    _check_table_statistic(table, stats)


def check_agent_statistic(stats):
    table = world.browser.find_element_by_id('agent')
    _check_table_statistic(table, stats)


def _check_table_statistic(table, stats):
    list_tr = table.find_elements_by_tag_name('tr')

    list_tr.pop(0)
    headers_line = list_tr.pop(0)
    headers = _extract_th_from_tr_element(headers_line)
    expected_headers = stats[0].keys()
    values = _extract_td_from_tr_elements(list_tr, headers, expected_headers)

    assert(stats == values)


def _extract_td_from_tr_elements(list_tr, headers, expected_headers):
    lines = list()
    for tr_element in list_tr:
        td_elements = tr_element.find_elements_by_tag_name('td')
        td_elements_text = [td_element.text.strip() for td_element in td_elements]
        line_dict = dict(zip(headers, td_elements_text))
        _filter_key_dict(line_dict, expected_headers)
        lines.append(line_dict)
    return lines


def _filter_key_dict(line_dict, filter_keys):
    ref_line_dict = copy.deepcopy(line_dict.keys())
    for key in ref_line_dict:
        if key not in filter_keys:
            del(line_dict[key])


def _extract_th_from_tr_element(tr_element):
    header_th = tr_element.find_elements_by_tag_name('th')
    return [header.text.strip() for header in header_th]
