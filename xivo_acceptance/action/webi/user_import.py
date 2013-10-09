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

from lettuce.registry import world


USER_URL = '/service/ipbx/index.php/pbx_settings/users/%s'


def open_import_user_form():
    URL = USER_URL % '?act=import'
    world.browser.get('%s%s' % (world.xivo_url, URL))
    world.browser.find_element_by_id('it-import', 'User import form not loaded')
