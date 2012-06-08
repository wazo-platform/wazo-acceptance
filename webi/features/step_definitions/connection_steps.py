# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world

from xivo_lettuce import common


@step(u'When I login as (.*) with password (.*) in (.*)')
def when_i_login_the_webi(step, login, password, language):
    common.webi_login(login, password, language)


@step(u'Given I am logged in')
def i_am_logged_in(step):
    if not common.logged():
        common.go_to_home_page()
        common.webi_login_as_default()
