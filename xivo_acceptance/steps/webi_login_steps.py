# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import *
from lettuce import step, world
from xivo_acceptance.lettuce import common


@step(u'When I login as (.*) with password (.*) in (.*)')
def when_i_login_the_webi(step, login, password, language):
    common.webi_login(login, password, language)


@step(u'Then I should be logged in "(.*)"')
def then_i_should_be_logged(step, username_expected):
    element = world.browser.find_element_by_xpath('//h1[@id="loginbox"]/span[contains(.,"Login")]/b')
    username = element.text
    assert_that(username, equal_to(username_expected))
