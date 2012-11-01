# -*- coding: utf-8 -*-

from lettuce import step

from xivo_lettuce.manager import parking_manager


@step(u'When I change the parking configuration to be:')
def when_i_change_the_parking_configuration_to_be(step):
    parking_configuration = step.hashes[0]
    parking_manager.set_parking_config(parking_configuration)


@step(u'Then I should have to following lines in "([^"]*)":')
def then_i_should_have_to_following_lines_in_group1(step, group1):
    expected_parking_info = step.hashes[0]
    parking_manager.check_parking_info(expected_parking_info)
