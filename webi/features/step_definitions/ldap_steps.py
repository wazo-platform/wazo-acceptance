# -*- coding: utf-8 -*-
from lettuce import step
from xivo_lettuce.common import *
from xivo_lettuce.manager import ldap_manager as ldap_man

@step(u'When I create an LDAP server with name "([^"]*)" and host "([^"]*)"')
def when_i_create_an_ldap_server_with_name_1_and_host_2(step, name, host):
    open_url('ldap', 'add')
    ldap_man.type_ldap_name_and_host(name,host)
    submit_form()

