# -*- coding: utf-8 -*-

from lettuce import step

from xivo_lettuce import form
from xivo_lettuce.common import open_url
from xivo_lettuce.manager import incall_manager as incall_man
from xivo_lettuce.manager_ws import incall_manager_ws


@step(u'When I create an incall with DID "([^"]*)" in context "([^"]*)"')
def when_i_create_incall_with_did(step, incall_did, context):
    open_url('incall', 'add')
    incall_man.type_incall_did(incall_did)
    incall_man.type_incall_context(context)
    form.submit_form()


@step(u'Given there is an incall "([^"]*)" in context "([^"]*)" to the "([^"]*)" "([^"]*)"$')
def given_there_is_an_incall_group1_in_context_group2_to(step, did, context, dst_type, dst_name):
    incall_manager_ws.delete_incalls_with_did(did)
    incall_manager_ws.add_incall(did, context, dst_type, dst_name)


@step(u'Given there is an incall "([^"]*)" in context "([^"]*)" to the "(.+)" "([^"]*)" with caller id name "([^"]*)" number "([^"]*)"')
def given_there_is_an_incall_group1_in_context_group2_to_the_queue_group3(step, did, context, destination_type, destination_name, caller_id_name, caller_id_number):
    incall_manager_ws.delete_incalls_with_did(did)
    open_url('incall', 'add')
    incall_man.type_incall_did(did)
    incall_man.type_incall_context(context)
    incall_man.type_incall_destination(destination_type, destination_name)
    incall_man.type_incall_caller_id('"%s" <%s>' % (caller_id_name, caller_id_number))
    form.submit_form()


@step(u'When incall "([^"]*)" is removed')
def when_incall_is_removed(step, incall_did):
    incall_man.remove_incall_with_did(incall_did)
