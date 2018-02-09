# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0+

from lettuce import step, world

from xivo_acceptance.helpers import trunkcustom_helper
from xivo_acceptance.lettuce import common, form


@step(u'Given there is a trunkcustom "([^"]*)"')
def given_there_is_a_trunkcustom(step, interface):
    trunkcustom_helper.add_or_replace_trunkcustom(interface)


@step(u'Given there is no trunkcustom "([^"]*)"')
def given_there_is_no_trunkcustom(step, interface):
    trunkcustom_helper.delete_trunkcustoms_with_interface(interface)


@step(u'When I create a trunkcustom with name "([^"]*)" in the webi')
def when_i_create_a_trunkcustom_with_name_and_trunk_in_the_webi(step, name):
    common.open_url('trunkcustom', 'add')
    input_name = world.browser.find_element_by_id('it-protocol-name', 'trunkcustom form not loaded')
    input_name.send_keys(name)
    input_interface = world.browser.find_element_by_id('it-protocol-interface', 'trunkcustom form not loaded')
    input_interface.send_keys(name)
    form.submit.submit_form()


@step(u'When I remove the trunkcustom "([^"]*)" in the webi')
def when_i_remove_the_trunkcustom_in_the_webi(step, name):
    common.open_url('trunkcustom', 'list')
    common.remove_line(name)
