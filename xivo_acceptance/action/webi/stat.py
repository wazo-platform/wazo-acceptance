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

import copy
from hamcrest import *
from lettuce.registry import world

from xivo_acceptance.helpers import agent_helper, queue_helper, stat_helper


def clean_cache():
    world.ssh_client_xivo.check_call(['xivo-stat', 'clean_db'])


def regenerate_cache():
    world.ssh_client_xivo.check_call(['xivo-stat', 'clean_db'])
    world.ssh_client_xivo.check_call(['xivo-stat', 'fill_db'])


def generate_cache(start_time=None, end_time=None):
    command = ['xivo-stat', 'fill_db']
    if start_time:
        command.append('--start=%s' % start_time)
    if end_time:
        command.append('--end=%s' % end_time)

    ret = world.ssh_client_xivo.check_call(command)
    assert_that(ret, equal_to(0), 'xivo-stall fill_db return value')


def open_queue_stat_page_on_day(queue_name, day, config_name):
    conf_id = stat_helper.find_conf_id_with_name(config_name)
    queue_id = queue_helper.find_queue_id_with_name(queue_name)
    host = world.config.xivo_host

    uri = '''https://%s/statistics/call_center/index.php/data/stats1''' % host
    qry = '''confid=%s&key=queue-%s&axetype=day&dbeg=%s&dend=%s&dday=%s&dweek=2012-08-17&dmonth=2012-08&dyear=2012''' % (conf_id, queue_id, day, day, day)

    url = '%s?%s' % (uri, qry)

    world.browser.get(url)


def open_agent_stat_page_on_day(agent_number, day, config_name):
    conf_id = stat_helper.find_conf_id_with_name(config_name)
    agent_id = agent_helper.find_agent_id_with_number(agent_number)
    host = world.config.xivo_host

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


def check_partial_agent_statistic(stats):
    table = world.browser.find_element_by_id('agent')
    _check_partial_table_statistic(table, stats)


def _check_table_statistic(table, stats):
    values = _get_statistics(table, stats)

    assert_that(values, equal_to(stats), '%s statistics' % table)


def _check_partial_table_statistic(table, stats):
    values = _get_statistics(table, stats)

    assert_that(values, has_items(*stats), 'Statistics contains atleast these items')


def _get_statistics(table, stats):
    list_tr = table.find_elements_by_tag_name('tr')

    list_tr.pop(0)
    headers_line = list_tr.pop(0)
    headers = _extract_th_from_tr_element(headers_line)
    expected_headers = stats[0].keys()
    values = _extract_td_from_tr_elements(list_tr, headers, expected_headers)
    return values


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


def check_agent_login_time(login_time, period_start):
    expected_stats = [
        {'': '%sh-%sh' % (period_start.hour, period_start.hour + 1),
         'Login': login_time}
    ]

    check_partial_agent_statistic(expected_stats)
