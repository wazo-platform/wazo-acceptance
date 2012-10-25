# -*- coding: utf-8 -*-
from lettuce import step, world
from xivo_lettuce.common import remove_element_if_exist, open_url, \
    go_to_tab, find_line
from xivo_lettuce import form


def phonebook_search(term):
    search = world.browser.find_element_by_id("it-toolbar-search")
    search.clear()
    search.send_keys(term)

    submit_button = world.browser.find_element_by_id("it-subsearch")
    submit_button.click()


def create_entry(entry):
    open_url('phonebook', 'add')

    display_name = "%(first name)s %(last name)s" % entry
    entry.setdefault('display name', display_name)

    form.set_text_field("First Name", entry['first name'])
    form.set_text_field("Last Name", entry['last name'])
    form.set_text_field("Display name", entry['display name'])

    go_to_tab("Office")
    form.set_text_field('Phone', entry.get('phone', ''))

    form.submit_form()


@step(u'Given "([^"]*)" is not in the phonebook')
def given_entry_is_not_in_the_phonebook(step, entry):
    open_url('phonebook')
    phonebook_search(entry)
    remove_element_if_exist("phonebook", entry)
    phonebook_search('')


@step(u'When I add the following entries to the phonebook:')
def when_i_add_the_following_entries_to_the_phonebook(step):
    for entry in step.hashes:
        create_entry(entry)


@step(u'When I search for "([^"]*)"')
def when_i_search_for_term(step, term):
    phonebook_search(term)


@step(u'Then "([^"]*)" appears in the list')
def then_entry_appears_in_the_list(step, entry):
    element = find_line(entry)
    assert element is not None
