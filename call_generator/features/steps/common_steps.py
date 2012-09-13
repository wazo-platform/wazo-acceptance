# -*- coding: UTF-8 -*-

from lettuce.decorators import step
from lettuce.registry import world
from datetime import datetime
from utils.func import extract_number_and_context_from_extension
from xivo_lettuce.common import submit_form, open_url


@step(u'Then I see rejected call to extension "([^"]+)" in asterisk log')
def then_i_see_rejected_call_in_asterisk_log(step, extension):
    number, context = extract_number_and_context_from_extension(extension)
    d = datetime.now()
    regex_date = d.strftime("%b %d %H:%M:([0-9]{2})")
    line_search = "\[%s\] NOTICE\[716\] chan_sip.c: Call from (.+) to extension '%s' rejected because extension not found in context '%s'." % (regex_date, number, context)
    command = ['less', '/var/log/asterisk/messages', '|', 'grep', '-E', '"%s"' % line_search]
    result = world.ssh_client_xivo.out_call(command)
    if not result:
        assert(False)


@step(u'Then i see the called extension "([^"]*)" in call logs page')
def then_i_see_the_called_extension_in_call_logs_page(step, exten):
    open_url('cel')
    submit_form()

    expected_exten = world.browser.find_element_by_xpath("//div[@id='sb-part-result']/div/table/tbody/tr[2]/td[3]").text
    assert expected_exten == exten
