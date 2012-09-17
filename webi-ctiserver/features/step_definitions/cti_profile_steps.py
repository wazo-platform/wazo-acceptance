# -*- coding: UTF-8 -*-


from lettuce import step
from selenium.common.exceptions import NoSuchElementException
from xivo_lettuce.common import open_url, find_line
from xivo_lettuce.manager import profile_manager
from webi.features.step_definitions import user_steps
from xivo_lettuce.manager.profile_manager import delete_profile


@step(u'When I add a CTI profile')
def add_cti_profile(step):
    open_url('profile', 'add')


@step(u'When I set the profile name to "([^"]*)"')
def when_i_set_the_profile_name_to_group1(step, profile_name):
    profile_manager.type_profile_names(profile_name, profile_name)


@step(u'Then I can\'t remove profile "([^"]*)"')
def then_i_see_errors(step, profile_label):
    open_url('profile', 'list')
    table_line = find_line(profile_label)
    try:
        delete_button = table_line.find_element_by_xpath(".//a[@title='Delete']")
    except NoSuchElementException:
        assert True
    else:
        assert False
