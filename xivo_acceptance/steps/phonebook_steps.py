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

from lettuce import step, world
from hamcrest import *

from xivo_acceptance.action.webi import phonebook as phonebook_action_webi
from xivo_acceptance.lettuce import assets, common
from xivo_acceptance.lettuce.aastra import AastraPhonebookBrowser


@step(u'Given "([^"]*)" is not in the phonebook')
def given_entry_is_not_in_the_phonebook(step, search):
    phonebook_action_webi.remove_entry_matching(search)


@step(u'Given the phonebook is accessible by any hosts')
def given_phone_is_accessible_by_any_hosts(step):
    phonebook_action_webi.set_accessibility_to_any_host()


@step(u'Given there are entries in the phonebook:')
def given_there_are_entries_in_the_phonebook(step):
    for entry in step.hashes:
        phonebook_action_webi.remove_entry_if_exists(entry)
        phonebook_action_webi.create_entry(entry)


@step(u'When I add the following entries to the phonebook:')
def when_i_add_the_following_entries_to_the_phonebook(step):
    for entry in step.hashes:
        phonebook_action_webi.create_entry(entry)


@step(u'When I search for "([^"]*)"$')
def when_i_search_for_term(step, term):
    phonebook_action_webi.phonebook_search(term)


@step(u'When I search the phonebook for "([^"]*)" on my Aastra "([^"]*)"$')
def when_i_search_the_phonebook_on_my_aastra(step, term, mac_address):
    phonebook_browser = AastraPhonebookBrowser(mac_address)
    phonebook_browser.use_provd_lookup_url()
    world.phone_results = phonebook_browser.search(term)


@step(u'When I search the phonebook for "([^"]*)" on my Aastra "([^"]*)" using the compatibility URL$')
def when_i_search_the_phonebook_on_my_aastra_using_compat_url(step, term, mac_address):
    phonebook_browser = AastraPhonebookBrowser(mac_address)
    phonebook_browser.use_compat_lookup_url()
    world.phone_results = phonebook_browser.search(term)


@step(u'Then I see the following results on the phone')
def then_i_see_the_following_results_on_the_phone(step):
    expected_results = step.hashes
    results = _extract_results(step.keys, world.phone_results)

    assert_that(results, has_items(*expected_results))


@step(u'Then I do not see the following results on the phone')
def then_i_do_not_see_the_following_results_on_the_phone(step):
    expected_results = step.hashes
    results = _extract_results(step.keys, world.phone_results)

    assert_that(results, is_not(has_items(*expected_results)))


@step(u'Then "([^"]*)" appears in the list')
def then_entry_appears_in_the_list(step, entry):
    assert common.find_line(entry) is not None


@step(u'When I import the CSV file "([^"]*)" into the phonebook')
def when_i_import_the_csv_file_into_the_phonebook(step, csvfile):
    path = assets.full_path(csvfile)
    phonebook_action_webi.import_csv_file(path)


def _extract_results(keys, phone_results):
    results = [dict((key, phone_result[key]) for key in keys) for phone_result in phone_results]
    return results
