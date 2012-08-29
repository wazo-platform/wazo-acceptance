# -*- coding: utf-8 -*-

from lettuce.registry import world
from xivo_ws import Statconf


def add_configuration(config_name, work_start, work_end, queue_name, agent_number=None):
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


def get_conf_id_with_name(config_name):
    return world.ws.statconfs.search(config_name)[0].id
