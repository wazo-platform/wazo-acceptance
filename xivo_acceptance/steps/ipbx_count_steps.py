# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step


@step(u'Given I have (\d+) enabled trunk')
def given_i_have_trunk(step, count):
    pass


@step(u'Given i remember the number of available trunk as "([^"]*)"')
def given_i_remember_the_number__of_available_trunk_as(step, name_var):
    pass


@step(u'When I open the ibpx count page')
def when_i_open_the_ipbx_count_page(step):
    pass


@step(u'Then I should have (\d+) more then remembered value "([^"]*)"')
def then_i_should_have_n_more_then_remembered_calue(step, count, name_var):
    pass
