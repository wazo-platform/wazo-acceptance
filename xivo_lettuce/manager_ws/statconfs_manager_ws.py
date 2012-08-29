# -*- coding: utf-8 -*-

from lettuce.registry import world
from xivo_ws import Statconf
from xivo_lettuce.manager_ws import agent_manager_ws, queue_manager_ws


def add_configuration_with_queue(config_name, work_start, work_end, queue_name):
    delete_conf_with_name_if_exists(config_name)
    queue_id = queue_manager_ws.get_queue_id_with_queue_name(queue_name)

    conf = _build_base_configuration(config_name, work_start, work_end)

    conf.queue = [queue_id]
    conf.queue_qos = [10]

    world.ws.statconfs.add(conf)


def add_configuration_with_queue_and_agent(config_name, work_start, work_end, queue_name, agent_number):
    delete_conf_with_name_if_exists(config_name)
    queue_id = queue_manager_ws.get_queue_id_with_queue_name(queue_name)
    agent_id = agent_manager_ws.get_agent_id_with_number(agent_number)

    conf = _build_base_configuration(config_name, work_start, work_end)

    conf.queue = [queue_id]
    conf.agent = [agent_id],
    conf.queue_qos = [10]

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


def delete_conf_with_name_if_exists(conf_name):
    try:
        conf_id = get_conf_id_with_name(conf_name)
    except Exception:
        pass
    else:
        delete_conf_with_conf_id(conf_id)


def get_conf_id_with_name(config_name):
    confs = world.ws.statconfs.search(config_name)
    for conf in confs:
        if conf.name == str(config_name):
            return conf.id
    raise Exception('no statconf with config name %s' % config_name)


def delete_conf_with_conf_id(conf_id):
    world.ws.statconfs.delete(conf_id)
