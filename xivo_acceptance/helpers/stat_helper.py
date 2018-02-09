# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0+

from lettuce import world

from xivo_acceptance.helpers import agent_helper, queue_helper
from xivo_ws import Statconf


def add_configuration_with_agent(config_name, work_start, work_end, agent_number):
    delete_confs_with_name(config_name)
    agent_id = agent_helper.find_agent_id_with_number(agent_number)

    conf = _build_base_configuration(config_name, work_start, work_end)
    conf.agent = [agent_id]

    world.ws.statconfs.add(conf)


def add_configuration_with_queue(config_name, work_start, work_end, queue_name):
    delete_confs_with_name(config_name)
    queue_id = queue_helper.find_queue_id_with_name(queue_name)

    conf = _build_base_configuration(config_name, work_start, work_end)
    conf.queue = [queue_id]
    conf.queue_qos = {queue_id: 10}

    world.ws.statconfs.add(conf)


def add_configuration_with_queue_and_agent(config_name, work_start, work_end, queue_name, agent_number):
    delete_confs_with_name(config_name)
    queue_id = queue_helper.find_queue_id_with_name(queue_name)
    agent_id = agent_helper.find_agent_id_with_number(agent_number)

    conf = _build_base_configuration(config_name, work_start, work_end)
    conf.queue = [queue_id]
    conf.queue_qos = {queue_id: 10}
    conf.agent = [agent_id]

    world.ws.statconfs.add(conf)


def add_configuration_with_queue_and_agents(config_name, work_start, work_end, queues, agents):
    delete_confs_with_name(config_name)

    queue_names = queues.split(',')
    queue_ids = []
    queue_qos = {}
    for queue_name in queue_names:
        queue_id = queue_helper.find_queue_id_with_name(queue_name.strip())
        queue_ids.append(queue_id)
        queue_qos[queue_id] = 10

    agent_numbers = agents.split(',')
    agent_ids = []
    for agent_number in agent_numbers:
        agent_ids.append(agent_helper.find_agent_id_with_number(agent_number.strip()))

    conf = _build_base_configuration(config_name, work_start, work_end)
    conf.queue = queue_ids
    conf.queue_qos = queue_qos
    conf.agent = agent_ids

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
