# -*- coding: utf-8 -*-
from lettuce import step, world

from xivo_lettuce import assets
from xivo_lettuce.common import find_line
from xivo_lettuce.manager import phonebook_manager


@step(u'Given "([^"]*)" is not in the phonebook')
def given_entry_is_not_in_the_phonebook(step, entry):
    phonebook_manager.remove_entry_if_exists(entry)


@step(u'When I add the following entries to the phonebook:')
def when_i_add_the_following_entries_to_the_phonebook(step):
    for entry in step.hashes:
        phonebook_manager.create_entry(entry)


@step(u'When I search for "([^"]*)"')
def when_i_search_for_term(step, term):
    phonebook_manager.phonebook_search(term)


@step(u'Then "([^"]*)" appears in the list')
def then_entry_appears_in_the_list(step, entry):
    element = find_line(entry)
    assert element is not None


@step(u'When I import the CSV file "([^"]*)" into the phonebook')
def when_i_import_the_csv_file_into_the_phonebook(step, csvfile):
    path = assets.full_path(csvfile)
    phonebook_manager.import_csv_file(path)
