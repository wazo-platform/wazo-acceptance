# -*- coding: UTF-8 -*-

import time

from lettuce import step, world
from xivo_lettuce import common
from xivo_lettuce import form, func
from xivo_lettuce.form.checkbox import Checkbox
from xivo_lettuce.logs import search_str_in_asterisk_log
from xivo_lettuce.table import extract_webi_table_to_dict


@step(u'Given there is "([^"]*)" activated in extenfeatures page')
def given_there_is_group1_activated_in_extensions_page(step, option_label):
    common.open_url('extenfeatures')
    option = Checkbox.from_label(option_label)
    option.check()
    form.submit.submit_form()


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


@step(u'Then I see the called extension "([^"]*)" by "([^"]*)" in call logs page')
def then_i_see_the_called_extension_in_call_logs_page(step, called, caller):
    common.open_url('cel')
    form.submit.submit_form()

    table = world.browser.find_element_by_xpath("//div[@id='sb-part-result']/div/table")
    lines = extract_webi_table_to_dict(table)

    last_call = lines.pop()
    assert last_call['Called'] == called
