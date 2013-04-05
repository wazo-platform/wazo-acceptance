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


from lettuce import step
from xivo_lettuce.manager import callfilter_manager
from xivo_lettuce.form import submit
from xivo_lettuce.common import open_url


@step(u'^When I create a callfilter "([^"]*)" with a boss "([^"]*)" with a secretary "([^"]*)"$')
def given_there_are_users_with_infos(step, callfilter_name, boss, secretary):
    open_url('callfilter', 'add')
    callfilter_manager.type_callfilter_name(callfilter_name)
    callfilter_manager.type_callfilter_boss(boss)
    callfilter_manager.add_secretary(secretary)
    submit.submit_form()
