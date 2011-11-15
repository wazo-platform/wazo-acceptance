from lettuce.decorators import step
from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException


USER_ADD_URL = 'service/ipbx/index.php/pbx_settings/users/?act=add'

@step(u'When I create a user (.*) (.*)')
def when_i_create_a_user(step, firstName, lastName):
    world.browser.get('%s%s' % (world.url, USER_ADD_URL))
    world.waitFor('it-userfeatures-firstname', 'User form not loaded')
    input_firtName = world.browser.find_element_by_id('it-userfeatures-firstname')
    input_lastName = world.browser.find_element_by_id('it-userfeatures-lastname')
    input_firtName.send_keys(firstName)
    input_lastName.send_keys(lastName)
    world.browser.find_element_by_id('it-submit').click()
    world.user = '%s %s' % (firstName, lastName)

@step(u'Then the list of users has the users:')
def then_i_see_the_list_of_users_has_the_users(step):
    world.waitFor('table-main-listing', 'User list not loaded')
    assert world.browser.find_element_by_xpath("//table[@id='table-main-listing']//tr[contains(.,'%s')]" % world.user) is not None

@step(u'When user is removed')
def remove_user(step):
    world.waitFor('table-main-listing', 'Delete button not loaded')
    delete_button = world.browser.find_element_by_xpath("//table[@id='table-main-listing']//tr[contains(.,'%s')]//a[@title='Delete']" % world.user)
    delete_button.click()
    alert = world.browser.switch_to_alert();
    alert.accept()

def _user_not_in_list():
    world.waitFor('table-main-listing', 'User list not loaded')
    try:
        user = world.browser.find_element_by_xpath("//table[@id='table-main-listing']//tr[contains(.,'%s')]" % world.user)
        return user is None
    except NoSuchElementException:
        return True

@step(u'Then user is not displayed in the list')
def then_user_is_not_displayed_in_the_list(step):
    assert _user_not_in_list()
