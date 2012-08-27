# -*- coding: utf-8 -*-

from lettuce import step

from xivo_lettuce.common import open_url, submit_form
from xivo_lettuce.manager import incall_manager as incall_man


@step(u'Given there is no incall with DID "([^"]*)"')
def given_there_is_no_incall_with_did(step, did):
    incall_man.remove_incall_with_did(did)


@step(u'When I create an incall with DID "([^"]*)" in context "([^"]*)"')
def when_i_create_incall_with_did(step, incall_did, context):
    open_url('incall', 'add')
    incall_man.type_incall_did(incall_did)
    incall_man.type_incall_context(context)
    submit_form()


@step(u'When incall "([^"]*)" is removed')
def when_incall_is_removed(step, incall_did):
    incall_man.remove_incall_with_did(incall_did)
