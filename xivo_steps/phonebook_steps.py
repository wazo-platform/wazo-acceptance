# -*- coding: utf-8 -*-

from lettuce import step, world

from hamcrest import assert_that, equal_to
from xivo_lettuce import assets
from xivo_lettuce.aastra import AastraPhonebookBrowser
from xivo_lettuce.common import find_line
from xivo_lettuce.manager import phonebook_manager


@step(u'Given "([^"]*)" is not in the phonebook')
def given_entry_is_not_in_the_phonebook(step, entry):
    phonebook_manager.remove_entry_if_exists(entry)


@step(u'Given the phonebook is accessible by any hosts')
def given_phone_is_accessible_by_any_hosts(step):
    phonebook_manager.set_accessibility_to_any_host()


@step(u'When I add the following entries to the phonebook:')
def when_i_add_the_following_entries_to_the_phonebook(step):
    for entry in step.hashes:
        phonebook_manager.create_entry(entry)


@step(u'When I search for "([^"]*)"$')
def when_i_search_for_term(step, term):
    phonebook_manager.phonebook_search(term)


@step(u'When I search the phonebook for "([^"]*)" on my Aastra')
def when_i_search_the_phonebook_on_my_aastra(step, term):
    phonebook_browser = AastraPhonebookBrowser()
    world.phone_results = phonebook_browser.search(term)


@step(u'Then I see the following results on the phone')
def then_i_see_the_following_results_on_the_phone(step):
    results = world.phone_results
    expected_results = [info['value'] for info in step.hashes]
    assert_that(results, equal_to(expected_results))


@step(u'Then "([^"]*)" appears in the list')
def then_entry_appears_in_the_list(step, entry):
    element = find_line(entry)
    assert element is not None


@step(u'When I import the CSV file "([^"]*)" into the phonebook')
def when_i_import_the_csv_file_into_the_phonebook(step, csvfile):
    path = assets.full_path(csvfile)
    phonebook_manager.import_csv_file(path)
