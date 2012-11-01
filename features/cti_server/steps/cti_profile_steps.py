# -*- coding: UTF-8 -*-


from lettuce import step
from selenium.common.exceptions import NoSuchElementException
from xivo_lettuce import common, form
from xivo_lettuce.manager import profile_manager


@step(u'When I add the CTI profile "([^"]*)" with errors')
def when_i_add_the_cti_profile_1_with_errors(step, profile_name):
    common.open_url('profile', 'add')
    profile_manager.type_profile_names(profile_name, profile_name)
    form.submit_form_with_errors()


@step(u'When I add the CTI profile "([^"]*)"')
def when_i_add_the_cti_profile_1(step, profile_name):
    common.open_url('profile', 'add')
    profile_manager.type_profile_names(profile_name, profile_name)
    form.submit_form()


@step(u'Then I can\'t remove profile "([^"]*)"')
def then_i_see_errors(step, profile_label):
    common.open_url('profile', 'list')
    table_line = common.find_line(profile_label)
    try:
        table_line.find_element_by_xpath(".//a[@title='Delete']")
    except NoSuchElementException:
        pass
    else:
        raise Exception('CTI profile %s should not be removable' % profile_label)
