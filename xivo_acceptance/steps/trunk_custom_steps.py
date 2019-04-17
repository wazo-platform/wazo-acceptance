# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step

from xivo_acceptance.helpers import trunkcustom_helper


@step(u'Given there is a trunkcustom "([^"]*)"')
def given_there_is_a_trunkcustom(step, interface):
    trunkcustom_helper.add_or_replace_trunkcustom(interface)


@step(u'Given there is no trunkcustom "([^"]*)"')
def given_there_is_no_trunkcustom(step, interface):
    trunkcustom_helper.delete_trunkcustoms_with_interface(interface)


@step(u'When I create a trunkcustom with name "([^"]*)" in the webi')
def when_i_create_a_trunkcustom_with_name_and_trunk_in_the_webi(step, name):
    pass


@step(u'When I remove the trunkcustom "([^"]*)" in the webi')
def when_i_remove_the_trunkcustom_in_the_webi(step, name):
    pass
