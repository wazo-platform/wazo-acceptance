# -*- coding: UTF-8 -*-

from lettuce.decorators import step
from xivo_lettuce.common import open_url
from xivo_lettuce.manager import profile_manager


@step(u'When I add a CTI profile')
def add_cti_profile(step):
    open_url('profile', 'add')


@step(u'When I set the profile name to "([^"]*)"')
def when_i_set_the_profile_name_to_group1(step, profile_name):
    profile_manager.type_profile_names(profile_name, profile_name)
