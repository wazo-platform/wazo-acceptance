# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, is_not, none
from lettuce import step, world


@step(u'Given there is XiVO not configured')
def given_there_is_xivo_not_configured(step):
    cmd = ['rm', '-f', '/var/lib/xivo/configured']
    world.ssh_client_xivo.check_call(cmd)


@step(u'When I start the wizard')
def when_i_start_the_wizard(step):
    world.browser.get(world.config['frontend']['url'])


@step(u'Then I should see the welcome message (.*)')
def then_i_see_the_welcome_message(step, message):
    pass


@step(u'When I select language (.*)')
def when_i_select(step, language):
    pass


@step(u'When I click next')
def when_i_click_next(step):
    pass


@step(u'When I click validate')
def when_i_click_validate(step):
    pass


@step(u'When I accept the terms of the licence')
def when_i_accept_the_terms_of_the_licence(step):
    pass


@step(u'Then I should be on the (.*) page')
def then_i_should_be_on_page(step, page):
    pass


@step(u'Then I see the license')
def then_i_see_the_license(step):
    pass


@step(u'When I fill hostname (.*), domain (.*), password (.*) in the configuration page')
def when_i_fill_the_configuration_page(step, hostname, domain, password):
    pass


@step(u'When I fill entity (.*), start (.*), end (.*)')
def when_i_fill_the_entity_context_page(step, entity, start, end):
    pass


@step(u'Then I should be redirected to the login page')
def then_i_should_be_redirected_to_the_login_page(step):
    pass


@step(u'Then server has uuid')
def then_server_has_uuid(step):
    assert_that(world.confd_client.infos.get()['uuid'], is_not(none()))
