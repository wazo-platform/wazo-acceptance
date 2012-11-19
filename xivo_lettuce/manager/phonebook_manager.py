
from lettuce import step, world

from xivo_lettuce.common import remove_element_if_exist, open_url, \
    go_to_tab, find_line
from xivo_lettuce import form

def phonebook_search(term):
    open_url('phonebook')
    form.input.set_text_field_with_id("it-toolbar-search", term)
    form.submit.submit_form("it-subsearch")


def create_entry(entry):
    open_url('phonebook', 'add')

    display_name = "%(first name)s %(last name)s" % entry
    entry.setdefault('display name', display_name)

    form.input.set_text_field_with_label("First Name", entry['first name'])
    form.input.set_text_field_with_label("Last Name", entry['last name'])
    form.input.set_text_field_with_label("Display name", entry['display name'])

    go_to_tab("Office")
    form.input.set_text_field_with_label('Phone', entry.get('phone', ''))

    form.submit.submit_form()


def remove_entry_if_exists(search):
    phonebook_search(search)
    remove_element_if_exist("phonebook", search)
    phonebook_search('')
