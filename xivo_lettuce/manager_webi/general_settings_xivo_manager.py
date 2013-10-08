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

from xivo_lettuce.common import open_url
from xivo_lettuce.form.checkbox import Checkbox
from xivo_lettuce import form


def enable_live_reload():
    _toggle_live_reload('enable')


def disable_live_reload():
    _toggle_live_reload('disable')


def _toggle_live_reload(state):
    open_url('general_settings')
    option = Checkbox.from_label('Live reload configuration')
    if state == 'enable':
        option.check()
    else:
        option.uncheck()
    form.submit.submit_form()
