# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from lettuce import world

from xivo_lettuce import common, form

MODULE_MAP = {
    'Configuration': 'xivo-configuration',
    'IPBX': 'service-ipbx',
}

CATEGORY_MAP = {
    'Management': 'manage',
    'General settings': 'general_settings',
    'IPBX settings': 'pbx_settings',
    'IPBX configuration': 'system_management',
}

SECTION_MAP = {
    'SIP Protocol': 'sip',
    'Directories': 'directories',
    'Users': 'users',
    'Contexts': 'context',
    'Entities': 'entity',
}


def create_admin_user(username, password, entity='xivo_entity'):
    common.open_url('admin_user', 'add')
    form.input.set_text_field_with_label("login", username)
    form.input.set_text_field_with_label("password", password)
    form.select.set_select_field_with_label("Entity", entity)
    form.submit.submit_form()


def set_privileges(username, privileges):
    common.open_url('admin_user', 'list')

    line = common.get_line(username)
    acl_button = line.find_element_by_xpath(".//a[@title='Rules']")
    acl_button.click()

    categories = set((x['module'], x['category']) for x in privileges)
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
