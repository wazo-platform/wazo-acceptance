from lettuce import world

from xivo_lettuce.common import open_url, find_line
from xivo_lettuce import form

MODULE_MAP = {
    'Configuration': 'xivo-configuration',
    'IPBX': 'service-ipbx',
}

CATEGORY_MAP = {
    'Management': 'manage',
    'General settings': 'general_settings',
}

SECTION_MAP = {
    'SIP Protocol': 'sip',
    'Directories': 'directories',
}

def create_admin_user(username, password):
    open_url('admin_user', 'add')
    form.input.set_text_field_with_label("login", username)
    form.input.set_text_field_with_label("password", password)
    form.submit.submit_form()


def set_privileges(username, privileges):
    open_url('admin_user', 'list')

    line = find_line(username)
    acl_button = line.find_element_by_xpath(".//a[@title='Rules']")
    acl_button.click()

    categories = set( (x['module'], x['category']) for x in privileges )
    for module, category in categories:
        open_category(module, category)

    for privilege in privileges:
        set_privilege(privilege)

    form.submit.submit_form()


def open_category(module_label, category_label):
    module = MODULE_MAP[module_label]
    category = CATEGORY_MAP[category_label]

    label_id = 'lb-%s-%s' % (module, category)
    element = world.browser.find_element_by_xpath("//label[@id='%s']/../../../span/a" % label_id)
    element.click()


def set_privilege(privilege):
    module = MODULE_MAP[privilege['module']]
    category = CATEGORY_MAP[privilege['category']]
    section = SECTION_MAP[privilege['section']]


    checkbox_id = '%s-%s-%s' % (module, category, section)
    if privilege['active']:
        form.checkbox.check_checkbox_with_id(checkbox_id)
    else:
        form.checkbox.uncheck_checkbox_with_id(checkbox_id)

