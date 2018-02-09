# -*- coding: utf-8 -*-
# Copyright (C) 2013-2016 Avencall
# SPDX-License-Identifier: GPL-3.0+


from lettuce.decorators import step

from xivo_acceptance.helpers import entity_helper


@step(u'^Given there are entities with infos:$')
def given_there_are_elements_with_infos(step):
    for data in step.hashes:
        entity_helper.add_entity(data['name'], data['display_name'])
