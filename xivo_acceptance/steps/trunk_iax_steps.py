# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step

from xivo_acceptance.helpers import trunkiax_helper


@step(u'Given there is a trunkiax "([^"]*)"')
def given_there_is_a_trunkiax(step, name):
    trunkiax_helper.add_or_replace_trunkiax(name)


@step(u'Given there is no trunkiax "([^"]*)"')
def given_there_is_no_trunkiax(step, name):
    trunkiax_helper.delete_trunkiaxs_with_name(name)


@step(u'When I create a trunkiax with name "([^"]*)"')
def when_i_create_a_trunkiax_with_name_and_trunk(step, name):
    pass


@step(u'When I remove the trunkiax "([^"]*)"')
def when_i_remove_the_trunkiax(step, name):
    pass
