'''
Created on 2011-11-11

@author: jylebleu
'''
from lettuce.decorators import step
from lettuce.registry import world
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException

USER_ADD_URL = 'service/ipbx/index.php/pbx_settings/users/?act=add'


@step(u'When I create a user (.*) (.*)')
def when_i_create_a_user(step, firstName, lastName):
    world.browser.get('%s%s' % (world.url, USER_ADD_URL))
    input_firtName = world.browser.find_element_by_id('it-userfeatures-firstname')
    input_lastName = world.browser.find_element_by_id('it-userfeatures-lastname')
    input_firtName.send_keys(firstName)
    input_lastName.send_keys(lastName)
    world.browser.find_element_by_id('it-submit').click()
    world.user = '%s %s' % (firstName, lastName)
    
    
    
@step(u'Then the list of users has the users:')
def then_i_see_the_list_of_users_has_the_users(step):
    assert world.browser.find_element_by_xpath("//table[@id='table-main-listing']//tr[contains(.,'%s')]" % world.user) is not None
    
@step(u'When user is removed')
def remove_user(step):
    delete_button = world.browser.find_element_by_xpath("//table[@id='table-main-listing']//tr[contains(.,'%s')]//a[@title='Delete']" % world.user)
    delete_button.click()
    alert = world.browser.switch_to_alert();
    alert.accept()
    
@step(u'Then user is not displayed in the list')
def then_user_is_not_displayed_in_the_list(step):
    user_line = None
    try:
        user_line = world.browser.find_element_by_xpath("//table[@id='table-main-listing']//tr[contains(.,'%s')]" % world.user)
    except NoSuchElementException:
        pass
    
    assert user_line is None
    
    

