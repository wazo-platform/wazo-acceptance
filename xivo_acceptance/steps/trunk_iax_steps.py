# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from lettuce import step, world

from xivo_acceptance.helpers import trunkiax_helper
from xivo_acceptance.lettuce import common, form


@step(u'Given there is a trunkiax "([^"]*)"')
def given_there_is_a_trunkiax(step, name):
    trunkiax_helper.add_or_replace_trunkiax(name)


@step(u'Given there is no trunkiax "([^"]*)"')
def given_there_is_no_trunkiax(step, name):
    trunkiax_helper.delete_trunkiaxs_with_name(name)


@step(u'When I create a trunkiax with name "([^"]*)"')
def when_i_create_a_trunkiax_with_name_and_trunk(step, name):
    common.open_url('trunkiax', 'add')
    input_name = world.browser.find_element_by_id('it-protocol-name', 'trunkiax form not loaded')
    input_name.send_keys(name)
    form.submit.submit_form()


@step(u'When I remove the trunkiax "([^"]*)"')
def when_i_remove_the_trunkiax(step, name):
    common.open_url('trunkiax', 'list')
    common.remove_line(name)
