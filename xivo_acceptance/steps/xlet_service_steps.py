# -*- coding: utf-8 -*-

# Copyright (C) 2016 Avencall
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
from xivo_acceptance.helpers import cti_helper


@step(u'(?:Given|When) I enable DND on XiVO Client')
def when_i_set_enable_on_xivo_client(step):
    cti_helper.set_dnd(True)


@step(u'(?:Given|When) I disable DND on XiVO Client')
def when_i_disable_dnd_on_xivo_client(step):
    cti_helper.set_dnd(False)


@step(u'(?:Given|When) I enable incoming call filtering on XiVO Client')
def when_i_enable_incallfilter_on_xivo_client(step):
    cti_helper.set_incallfilter(True)


@step(u'(?:Given|When) I disable incoming call filtering on XiVO Client')
def when_i_disable_incallfilter_on_xivo_client(step):
    cti_helper.set_incallfilter(False)


@step(u'(?:Given|When) I enable forwarding on no-answer with destination "([^"]*)" on XiVO Client')
def when_i_enable_forwarding_on_noanswer_on_xivo_client(step, destination):
    cti_helper.set_noanswer(True, destination)


@step(u'(?:Given|When) I disable forwarding on no-answer on XiVO Client')
def when_i_disable_forwarding_on_noanswer_on_xivo_client(step):
    cti_helper.set_noanswer(False)


@step(u'(?:Given|When) I enable forwarding on busy with destination "([^"]*)" on XiVO Client')
def when_i_enable_forwarding_on_busy_on_xivo_client(step, destination):
    cti_helper.set_busy(True, destination)


@step(u'(?:Given|When) I disable forwarding on busy on XiVO Client')
def when_i_disable_forwarding_on_busy_on_xivo_client(step):
    cti_helper.set_busy(False)


@step(u'(?:Given|When) I enable unconditional forwarding with destination "([^"]*)" on XiVO Client')
def when_i_enable_unconditional_forwarding_on_xivo_client(step, destination):
    cti_helper.set_unconditional(True, destination)


@step(u'(?:Given|When) I disable unconditional forwarding on XiVO Client')
def when_i_disable_unconditional_forwarding_on_xivo_client(step):
    cti_helper.set_unconditional(False)


@step(u'(?:Given|When) I disable all forwards on XiVO Client')
def when_i_disable_all_forwards_on_xivo_client(step):
    cti_helper.disable_all_forwards()
