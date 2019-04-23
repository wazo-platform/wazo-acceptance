# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step

from xivo_acceptance.helpers import incall_helper


@step(u'Given there are incalls with infos in the webi:')
def given_there_are_incalls_with_infos(step):
    pass


@step(u'Given there is an incall "([^"]*)" in context "([^"]*)" to the "([^"]*)" "([^"]*)"$')
def given_there_is_an_incall_group1_in_context_group2_to(step, did, context, dst_type, dst_name):
    incall_helper.add_or_replace_incall(did, context, dst_type, dst_name)
