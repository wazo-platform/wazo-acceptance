# -*- coding: utf-8 -*-

from lettuce import step

from xivo_lettuce import form
from xivo_lettuce.common import open_url
from xivo_lettuce.manager import incall_manager as incall_man
from xivo_lettuce.manager_ws import incall_manager_ws


@step(u'Given there is an incall "([^"]*)" in context "([^"]*)" to the "([^"]*)" "([^"]*)"$')
def given_there_is_an_incall_group1_in_context_group2_to(step, did, context, dst_type, dst_name):
    incall_manager_ws.delete_incalls_with_did(did)
    incall_manager_ws.add_incall(did, context, dst_type, dst_name)


@step(u'Given there is an incall "([^"]*)" in context "([^"]*)" to the "([^"]*)" "([^"]*)" with caller id name "([^"]*)" number "([^"]*)"')
def given_there_is_an_incall_group1_in_context_group2_to_the_queue_group3(step, did, context, dst_type, dst_name, cid_name, cid_num):
    caller_id = '"%s" <%s>' % (cid_name, cid_num)
    incall_manager_ws.delete_incalls_with_did(did)
    incall_manager_ws.add_incall(did, context, dst_type, dst_name, caller_id)


@step(u'When I create an incall with DID "([^"]*)" in context "([^"]*)"')
def when_i_create_incall_with_did(step, incall_did, context):
    open_url('incall', 'add')
    incall_man.type_incall_did(incall_did)
    incall_man.type_incall_context(context)
    form.submit_form()


@step(u'When incall "([^"]*)" is removed')
def when_incall_is_removed(step, incall_did):
    incall_man.remove_incall_with_did(incall_did)
