# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from lettuce import step, world
from xivo_lettuce import form
from xivo_lettuce import urls
from xivo_lettuce.common import open_url, edit_line, webi_logout
from xivo_lettuce.manager import admin_user_manager

import time


def is_browser_on_module_page(module):
    url = urls.URLS[module]
    return url in world.browser.current_url


@step(u'When I create an admin user with login "([^"]*)" and password "([^"]*)"')
def when_i_create_an_admin_user_with_login_and_password(step, login, password):
    admin_user_manager.create_admin_user(login, password)


@step(u'When I assign the following rights to the admin user "([^"]*)":')
def when_i_assign_the_following_rights_to_the_admin_user(step, admin):
    admin_user_manager.set_privileges(admin, step.hashes)


@step(u'When I logout from the web interface')
def when_i_logout_from_the_web_interface(step):
    webi_logout()


@step(u'Then I can access the directory configuration')
def then_i_can_access_the_directory_configuration(step):
    open_url("directory_config", "list")
    assert is_browser_on_module_page("directory_config")


@step(u'Then I can access the SIP Protocol configuration')
def then_i_can_access_the_sip_protocol_configuration(step):
    open_url("general_sip")
    assert is_browser_on_module_page("general_sip")


@step(u'Then I cannot access the SCCP Protocol configuration')
def then_i_cannot_access_the_sccp_protocol_configuration(step):
    open_url("sccpgeneralsettings")
    time.sleep(2)
    assert is_browser_on_module_page("sccpgeneralsettings") == False
