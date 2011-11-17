# -*- coding: UTF-8 -*-

from lettuce.decorators import step
from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException


USER_URL = 'service/ipbx/index.php/pbx_settings/users/%s'


def _open_add_user_form():
    URL = USER_URL % '?act=add'
    world.browser.get('%s%s' % (world.url, URL))
    world.waitFor('it-userfeatures-firstname', 'User add form not loaded')
    
def _open_edit_user_form(id):
    URL = USER_URL % '?act=edit&id=%d'
    world.browser.get('%s%s' % (world.url, URL % id))
    world.waitFor('it-userfeatures-firstname', 'User edit form not loaded')

def _open_list_user_url():
    URL = USER_URL % '?act=list'
    world.browser.get('%s%s' % (world.url, URL))
    world.waitFor('table-main-listing', 'User list not loaded')

def _type_user_names(firstName, lastName):
    world.user = '%s %s' % (firstName, lastName)
    input_firtName = world.browser.find_element_by_id('it-userfeatures-firstname')
    input_lastName = world.browser.find_element_by_id('it-userfeatures-lastname')
    input_firtName.clear()
    input_firtName.send_keys(firstName)
    input_lastName.clear()
    input_lastName.send_keys(lastName)

def _type_user_in_group(groupName):
    group = world.browser.find_element_by_xpath("//li[@id='dwsm-tab-7']//a[@href='#groups']")
    group.click()
    world.waitFor('sb-part-groups', 'Group tab not loaded')
    select_group = world.browser.find_element_by_xpath('//select[@id="it-grouplist"]//option[@value="%s"]' % groupName)
    select_group.click()
    add_button = world.browser.find_element_by_id('bt-ingroup')
    add_button.click()

def _submit_user_form():
    return world.browser.find_element_by_id('it-submit').click()

@step(u'When I create a user (.*) ([a-zA-Z-]+)$')
def when_i_create_a_user(step, firstName, lastName):
    _open_add_user_form()
    _type_user_names(firstName, lastName)
    _submit_user_form()

def _user_is_saved(firstname, lastname):
    _open_list_user_url()
    try:
        user = world.browser.find_element_by_xpath("//table[@id='table-main-listing']//tr[contains(.,'%s')]" % (firstname, lastname))
        return user is not None
    except NoSuchElementException:
        return False

@step(u'Then user (.*) (.*) is not displayed in the list')
def then_user_is_not_displayed_in_the_list(step, firstname, lastname):
    assert _user_is_saved(firstname, lastname)

@step(u'When I add user (.*) (.*) in group (.*)')
def when_i_create_a_user_in_group(step, firstname, lastname, group):
    import context_steps as ctx
    ctx.when_i_edit_a_context(step, 'default')
    ctx.when_i_add_group_interval(step, 5000, 6000)
    import group_steps as grp
    grp.when_i_create_group(step, world.group)
    _open_add_user_form()
    _type_user_names(firstname, lastname)
    _type_user_in_group(group)
    _submit_user_form()
    _user_is_saved(firstname, lastname)

def _insert_user(firstname, lastname):
    from webservices.user import WsUser
    import json
    with open('xivojson/user.json') as f:
        datajson = f.read()  % {'firstname': firstname,
                'lastname': lastname}
        data = json.loads(datajson)
    wsu = WsUser()
    wsu.add(data)

def _delete_user(firstname, lastname):
    from webservices.user import WsUser
    wsu = WsUser()
    for id in _find_user_id(firstname, lastname):
        wsu.delete(id)

@step(u'When I edit (.*) (.*)')
def when_i_edit_user(step, firstname, lastname):
    id = _find_user_id(firstname, lastname)
    if len(id) > 0:
        _open_edit_user_form(id[0])
        _submit_user_form()

@step(u'When I rename (.*) (.*) to (.*) (.*)')
def when_i_rename_user(step, orig_firstname, orig_lastname, dest_firstname, dest_lastname):
    id = _find_user_id(orig_firstname, orig_lastname)
    _delete_user(dest_firstname, dest_lastname)
    if len(id) > 0:
        _open_edit_user_form(id[0])
        _type_user_names(dest_firstname, dest_lastname)
        _submit_user_form()
        _user_is_saved(dest_firstname, dest_lastname)

def _insert_group_with_user(group_name, user_list=[]):
    from webservices import group
    import json
    with open('xivojson/group.json') as f:
        data = f.read()
        users = ""
        if len(user_list) > 0:
            users = r', "user": [%s]' % ', '.join(['"%s"' % str(id) for id in user_list])
        data = data % {'user_list': users,
                'groupname': group_name}
        data = json.loads(data)
    wsg = group.WsGroup()
    wsg.clear()
    wsg.add(data)

def _is_in_group(group_name, user_id):
    from webservices import group
    wsg = group.WsGroup()
    group_list = wsg.list()
    group_id = [group['id'] for group in group_list if group['name'] == group_name]
    if len(group_id) > 0:
        group_view = wsg.view(group_id[0])
        for user in group_view['user']:
            if user['userid'] == user_id:
                return True
    return False

@step(u'Then (.*) (.*) is in group (.*)')
def then_user_is_in_group(step, firstname, lastname, group_name):
    user_id_list = _find_user_id(firstname, lastname)
    if len(user_id_list) > 0:
        assert _is_in_group(group_name, user_id_list[0])

def _find_user_id(firstname, lastname):
    from webservices import user
    wsu = user.WsUser()
    user_list = wsu.list()
    return [userinfo['id'] for userinfo in user_list
        if userinfo['firstname'] == firstname and userinfo['lastname'] == lastname]

@step(u'Given a user (.*) (.*) in group (.*)')
def given_a_user_in_group(step, firstname, lastname, group):
    world.user = '%s %s' % (firstname, lastname)
    world.group = group
    _delete_user(firstname, lastname)
    _insert_user(firstname, lastname)
    _insert_group_with_user(group, _find_user_id(firstname, lastname))
