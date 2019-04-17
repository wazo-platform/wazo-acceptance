# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, empty, is_not
from lettuce.decorators import step
from lettuce.registry import world

from xivo_acceptance.helpers import outcall_helper, trunksip_helper


@step(u'Given there is no outcall "([^"]*)"')
def given_there_is_no_outcall(step, name):
    outcall_helper.delete_outcalls_with_name(name)


@step(u'Given there is an outcall "([^"]*)" with trunk "([^"]*)" and no extension matched')
def given_there_is_an_outcall_with_trunk_and_no_extensions_matched(step, outcall_name, trunk_name):
    trunksip_helper.add_or_replace_trunksip(world.dummy_ip_address, trunk_name)
    trunk_id = trunksip_helper.find_trunksip_id_with_name(trunk_name)

    outcall = {'name': outcall_name,
               'trunks': [{'id': trunk_id}]}
    outcall_helper.add_or_replace_outcall(outcall)


@step(u'Given there is an outcall "([^"]*)" with trunk "([^"]*)" with extension patterns')
def given_there_is_an_outcall_with_trunk_with_extension_patterns(step, outcall_name, trunk_name):
    trunksip_helper.add_or_replace_trunksip(world.dummy_ip_address, trunk_name)
    trunk_id = trunksip_helper.find_trunksip_id_with_name(trunk_name)

    extensions = []
    for outcall_extension in step.hashes:
        extension = {}
        extension['context'] = 'to-extern'
        extension['exten'] = outcall_extension['extension_pattern']
        extension['stripnum'] = outcall_extension.get('stripnum', 0)
        extension['caller_id'] = outcall_extension.get('caller_id', '')
        extensions.append(extension)

    outcall = {'name': outcall_name,
               'trunks': [{'id': trunk_id}],
               'extensions': extensions}
    outcall_helper.add_or_replace_outcall(outcall)


@step(u'Given there is an outcall "([^"]*)" with trunk "([^"]*)"$')
def given_there_is_an_outcall_with_trunk(step, outcall_name, trunk_name):
    trunksip_helper.add_or_replace_trunksip(world.dummy_ip_address, trunk_name)
    trunk_id = trunksip_helper.find_trunksip_id_with_name(trunk_name)

    outcall = {'name': outcall_name,
               'trunks': [{'id': trunk_id}]}
    outcall_helper.add_or_replace_outcall(outcall)


@step(u'Then there are an outcall "([^"]*)" with preprocess subroutine "([^"]*)"')
def then_there_are_an_outcall(step, name, preprocess_subroutine):
    outcalls = world.confd_client.outcalls.list(name=name, preprocess_subroutine=preprocess_subroutine)
    assert_that(outcalls['items'], is_not(empty()))


@step(u'When I create an outcall with name "([^"]*)" and trunk "([^"]*)" in the webi')
def when_i_create_an_outcall_with_name_and_trunk_in_the_webi(step, name, trunk):
    pass


@step(u'When i edit the outcall "([^"]*)" and set preprocess subroutine to "([^"]*)" in the webi')
def when_i_edit_the_outcall_and_set_preprocess_subroutine_in_the_webi(step, name, preprocess_subroutine):
    pass


@step(u'When I remove the outcall "([^"]*)" in the webi')
def when_i_remove_the_outcall_in_the_webi(step, name):
    pass


@step(u'When I remove extension patterns from outcall "([^"]*)" in the webi:')
def when_i_remove_extension_patterns_from_outcall_1_in_the_webi(step, outcall_name):
    pass


@step(u'When I add the following extension patterns to the outcall "([^"]*)" in the webi:')
def when_i_add_the_following_extension_patterns_to_the_outcall_1_in_the_webi(step, outcall_name):
    pass


@step(u'Then the outcall "([^"]*)" has the extension patterns in the webi:')
def then_the_outcall_1_has_the_extension_patterns_in_the_webi(step, outcall_name):
    pass


@step(u'Then the outcall "([^"]*)" does not have extension patterns in the webi:')
def then_the_outcall_1_does_not_have_extension_patterns_in_the_webi(step, outcall_name):
    pass


@step(u'Then there is no outcall "([^"]*)" in the webi')
def then_there_is_no_outcall_in_the_webi(step, name):
    pass
