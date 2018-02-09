# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0+

from lettuce import step

from xivo_acceptance.action.webi import callfilter as callfilter_action_webi
from xivo_acceptance.lettuce import common


@step(u'Given there is no callfilter "([^"]*)"$')
def given_there_is_no_callfilter(step, search):
    common.remove_element_if_exist('callfilter', search)


@step(u'Given there are callfilters:')
def given_there_are_callfilters(step):
    for data in step.hashes:
        callfilter_action_webi.add_boss_secretary_filter(**data)


@step(u'^When I create a callfilter "([^"]*)" with a boss "([^"]*)" with a secretary "([^"]*)"$')
def given_there_are_users_with_infos(step, callfilter_name, boss, secretary):
    callfilter_action_webi.add_boss_secretary_filter(name=callfilter_name,
                                                     boss=boss,
                                                     secretary=secretary)
