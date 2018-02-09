# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0+

from lettuce import step

from xivo_acceptance.action.webi import parking as parking_action_webi


@step(u'When I change the parking configuration to be:')
def when_i_change_the_parking_configuration_to_be(step):
    parking_configuration = step.hashes[0]
    parking_action_webi.set_parking_config(parking_configuration)


@step(u'Then asterisk should have the following parking configuration:')
def then_asterisk_should_have_the_following_parking_configuration(step):
    expected_parking_info = step.hashes[0]
    parking_action_webi.check_parking_info(expected_parking_info)
