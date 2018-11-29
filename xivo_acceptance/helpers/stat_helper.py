# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+


def add_configuration_with_agent(config_name, work_start, work_end, agent_number):
    raise NotImplementedError


def add_configuration_with_queue(config_name, work_start, work_end, queue_name):
    raise NotImplementedError


def add_configuration_with_queue_and_agent(config_name, work_start, work_end, queue_name, agent_number):
    raise NotImplementedError


def add_configuration_with_queue_and_agents(config_name, work_start, work_end, queues, agents):
    raise NotImplementedError


def find_conf_id_with_name(name):
    raise NotImplementedError
