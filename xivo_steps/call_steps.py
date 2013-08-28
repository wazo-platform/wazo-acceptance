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

import time

from lettuce import step
from xivo_lettuce import common
from xivo_lettuce import form, func
from xivo_lettuce.form.checkbox import Checkbox
from xivo_lettuce.logs import search_str_in_asterisk_log
from xivo_lettuce.manager import call_manager


@step(u'Given there is "([^"]*)" activated in extenfeatures page')
def given_there_is_group1_activated_in_extensions_page(step, option_label):
    common.open_url('extenfeatures')
    option = Checkbox.from_label(option_label)
    option.check()
    form.submit.submit_form()


@step(u'Given the agent "([^"]*)" will answer a call and hangup after (\d+) seconds')
def given_the_agent_will_answer_a_call_and_hangup_after_10_seconds(step, agent_number, seconds):
    call_duration_ms = int(seconds) * 1000
    call_manager.execute_answer_then_hangup(call_duration_ms)


@step(u'When I call extension "([^"]*)" from trunk "([^"]*)"')
def when_i_call_extension_from_trunk(step, extension, trunk_name):
    call_manager.execute_n_calls_then_wait(1,
                                           extension,
                                           username=trunk_name,
                                           password=trunk_name)


@step(u'Then I see no recording file of this call in monitoring audio files page')
def then_i_not_see_recording_file_of_this_call_in_monitoring_audio_files_page(step):
    now = int(time.time())
    search = 'user-1100-1101-%d.wav'
    nbtries = 0
    maxtries = 5
    while nbtries < maxtries:
        file_name = search % (now - nbtries)
        assert not common.element_is_in_list('sounds', file_name, {'dir': 'monitor'})
        nbtries += 1


@step(u'Then I see rejected call to extension "([^"]+)" in asterisk log')
def then_i_see_rejected_call_in_asterisk_log(step, extension):
    number, context = func.extract_number_and_context_from_extension(extension)
    expression = "to extension '%s' rejected because extension not found in context '%s'" % (number, context)
    assert search_str_in_asterisk_log(expression)
