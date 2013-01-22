# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
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

from lettuce import world
from xivo_ws import Statconf
from xivo_lettuce.manager_ws import agent_manager_ws, queue_manager_ws


def add_configuration_with_agent(config_name, work_start, work_end, agent_number):
    delete_confs_with_name(config_name)
    agent_id = agent_manager_ws.find_agent_id_with_number(agent_number)

    conf = _build_base_configuration(config_name, work_start, work_end)
    conf.agent = [agent_id]

    world.ws.statconfs.add(conf)


def add_configuration_with_queue(config_name, work_start, work_end, queue_name):
    delete_confs_with_name(config_name)
    queue_id = queue_manager_ws.find_queue_id_with_name(queue_name)

    conf = _build_base_configuration(config_name, work_start, work_end)
    conf.queue = [queue_id]
    conf.queue_qos = {queue_id: 10}

    world.ws.statconfs.add(conf)


def add_configuration_with_queue_and_agent(config_name, work_start, work_end, queue_name, agent_number):
    delete_confs_with_name(config_name)
    queue_id = queue_manager_ws.find_queue_id_with_name(queue_name)
    agent_id = agent_manager_ws.find_agent_id_with_number(agent_number)

    conf = _build_base_configuration(config_name, work_start, work_end)
    conf.queue = [queue_id]
    conf.queue_qos = {queue_id: 10}
    conf.agent = [agent_id]

    world.ws.statconfs.add(conf)


def add_configuration_with_infos(config_name, work_start, work_end, data):
    delete_confs_with_name(config_name)

    list_queue_id = []
    dict_queue_id_qos = {}
    for q in data['queues']:
        queue_id = queue_manager_ws.find_queue_id_with_name(q['name'])
        list_queue_id.append(queue_id)
        dict_queue_id_qos[queue_id] = q['qos']

    list_agent_id = []
    for agent_number in data['agents']:
        agent_id = agent_manager_ws.find_agent_id_with_number(agent_number)
        list_agent_id.append(agent_id)

    conf = _build_base_configuration(config_name, work_start, work_end)
    conf.queue = list_queue_id
    conf.queue_qos = dict_queue_id_qos
    conf.agent = list_agent_id

    world.ws.statconfs.add(conf)


def _build_base_configuration(config_name, work_start, work_end):
    conf = Statconf(
        name=config_name,
        hour_start=work_start,
        hour_end=work_end,
        dbegcache='2012-01',
        monday=True,
        tuesday=True,
        wednesday=True,
        thursday=True,
        friday=True,
        saturday=True,
        sunday=True
        )
    return conf


def delete_confs_with_name(name):
    for conf in _search_confs_with_name(name):
        world.ws.statconfs.delete(conf.id)


def find_conf_id_with_name(name):
    conf = _find_conf_with_name(name)
    return conf.id


def _find_conf_with_name(name):
    confs = _search_confs_with_name(name)
    if len(confs) != 1:
        raise Exception('expecting 1 conf with name %r: found %s' %
                        (name, len(confs)))
    return confs[0]


def _search_confs_with_name(name):
    name = unicode(name)
    confs = world.ws.statconfs.search(name)
    return [conf for conf in confs if conf.name == name]
