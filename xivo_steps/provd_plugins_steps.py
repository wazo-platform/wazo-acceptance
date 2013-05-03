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

from xivo_lettuce.manager import provd_general_manager as provdg
from xivo_lettuce.manager import provd_plugins_manager as provdp


@step(u'Given a update plugins provd with good url')
def given_a_update_plugins_provd(step):
    provdp.update_plugin_list('http://provd.xivo.fr/plugins/1/stable/')


@step(u'Given a update plugins provd with bad url')
def given_a_update_plugins_provd_with_bad_url(step):
    provdp.update_plugin_list('http://provd.xivo.fr/plugins/1/lol/')


@step(u'Then plugins list successfully updated')
def then_plugins_list_successfully_updated(step):
    assert provdp.plugins_successfully_updated()


@step(u'Then plugins list has a error during update')
def then_plugins_list_has_error_during_update(step):
    assert provdp.plugins_error_during_update()
    provdg.update_plugin_server_url('http://provd.xivo.fr/plugins/1/stable/')
