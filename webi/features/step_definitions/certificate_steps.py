# -*- coding: utf-8 -*-
import datetime

from lettuce import step, world
from xivo_lettuce import form, logs
from xivo_lettuce.common import open_url, remove_all_elements, go_to_tab
from xivo_lettuce.manager import asterisk_manager
from xivo_lettuce.checkbox import Checkbox
from selenium.webdriver.support.select import Select


def create_or_replace_certificate(info):
    remove_all_elements('certificat', info['name'])

    open_url('certificat', 'add')

    input_name = world.browser.find_element_by_id('it-name')
    input_name.send_keys(info['name'])

    input_email = world.browser.find_element_by_id('it-subject-emailAddress')
    input_email.clear()
    input_email.send_keys(info['email'])

    input_date = world.browser.find_element_by_id('it-validity-end')
    input_date.clear()

    date = datetime.datetime.now()
    if info['valid date in the future'] == "yes":
        date += datetime.timedelta(days=31)
    else:
        date -= datetime.timedelta(days=1)

    input_date.send_keys(date.strftime("%m/%d/%Y"))

    if 'autosigned' in info:
        autosign_check = world.browser.find_element_by_id('it-autosigned')
        checked = info['autosigned'] == "yes"
        Checkbox(autosign_check).set_checked(checked)

    if 'certificate authority' in info:
        authority_check = world.browser.find_element_by_id('it-is_ca')
        checked = info['certificate authority'] == "yes"
        Checkbox(authority_check).set_checked(checked)



def insert_hostname_into_form():
    command = ['hostname', '-f']
    hostname = world.ssh_client_xivo.out_call(command).strip()

    input_cn = world.browser.find_element_by_id("it-subject-CN")
    input_cn.send_keys(hostname)

def update_sip_configuration(info):
    open_url('general_sip')
    go_to_tab('Security')

    checked = info['allow tls connections'] == "yes"
    Checkbox.from_label("Allow TLS connections").set_checked(checked)

    form.set_text_field("Listening address", info['listening address'])

    form.set_select_field("Server certificate", info['server certificate'])
    form.set_select_field("CA certificate", info['ca certificate'])
    form.submit_form()


@step(u'When I create a certificate with the following invalid info:')
def when_i_create_a_certificate_with_the_following_invalid_info(step):
    for info in step.hashes:
        create_or_replace_certificate(info)
        form.submit_form_with_errors()

@step(u'When I create a certificate with following valid info:')
def when_i_create_a_certificate_with_following_valid_info(step):
    for info in step.hashes:
        create_or_replace_certificate(info)
        form.submit_form()


@step(u'I create a certificate with following valid info and the server\'s hostname as common name:$')
def i_create_a_certificate_with_following_valid_info_and_the_server_s_hostname_as_common_name(step):
    for info in step.hashes:
        create_or_replace_certificate(info)
        insert_hostname_into_form()
        form.submit_form()

@step(u'When I enable the following options for the SIP Protocol:')
def when_i_enable_the_following_options_for_the_sip_protocol(step):
    for info in step.hashes:
        update_sip_configuration(info)


@step(u'Then SIP tls connections use the "([^"]*)" certificate for encryption')
def then_sip_tls_connections_use_the_group1_certificate_for_encryption(step, certificate):
    configfile = "sip.conf"
    certificate_path = "/var/lib/pf-xivo/certificates/%s.pem" % certificate
    variable = "tlscertfile"
    current_path = asterisk_manager.get_asterisk_conf(configfile, variable)
    assert(current_path == certificate_path)


@step(u'Then there are no warnings when reloading sip configuration')
def then_there_are_no_warnings_when_reloading_sip_configuration(step):

    now = datetime.datetime.now()

    asterisk_manager.send_to_asterisk_cli("sip reload")
    command = ['tac', '/var/log/asterisk/messages', '|', 'grep', 'WARNING', '--max-count', '5']
    output = world.ssh_client_xivo.out_call(command).strip()

    lines = logs.read_last_log_lines(output, now)
    assert len(lines) > 1


