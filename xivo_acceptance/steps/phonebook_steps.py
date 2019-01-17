# -*- coding: utf-8 -*-
# Copyright 2013-2017 The Wazo Authors  (see the AUTHORS file)
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step, world
from hamcrest import assert_that, has_items

from xivo_acceptance.action.webi import phonebook as phonebook_action_webi
from xivo_acceptance.action.dird import phonebook as phonebook_action_dird
from xivo_acceptance.lettuce import common
from xivo_acceptance.lettuce.aastra import AastraPhonebookBrowser


@step(u'Given "([^"]*)" "([^"]*)" is not in the phonebook "([^"]*)"')
def given_entry_is_not_in_the_phonebook(step, firstname, lastname, phonebook_name):
    entity = world.config['default_entity'].replace('_', '')
    entry = {'first name': firstname,
             'last name': lastname}
    phonebook_action_dird.remove_entry_if_exists(entry, phonebook_name, entity)


@step(u'Given the phonebook is accessible by any hosts')
def given_phone_is_accessible_by_any_hosts(step):
    phonebook_action_webi.set_accessibility_to_any_host()


@step(u'Given there are entries in the phonebook "([^"]*)"')
def given_there_are_entries_in_the_phonebook_1(step, phonebook_name):
    entity = world.config['default_entity'].replace('_', '')
    for entry in step.hashes:
        phonebook_action_dird.remove_entry_if_exists(entry, phonebook_name, entity)
        phonebook_action_dird.create_entry(entry, phonebook_name, entity)


@step(u'Given there are local dird phonebooks:')
def given_there_are_local_dird_phonebooks(step):
    default_entity = world.config['default_entity'].replace('_', '')
    for entry in step.hashes:
        phonebook_action_webi.remove_directory_if_exists(entry['name'])
        phonebook_action_webi.create_local_dird_directory(entry['name'],
                                                          entry['phonebook name'],
                                                          entry.get('entity', default_entity))


@step(u'When I add the following entries to the phonebook "([^"]*)"')
def when_i_add_the_following_entries_to_the_phonebook(step, phonebook_name):
    entity = world.config['default_entity'].replace('_', '')
    for entry in step.hashes:
        phonebook_action_webi.create_entry(entry, phonebook_name, entity)


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


@step(u'Then "([^"]*)" appears in the list')
def then_entry_appears_in_the_list(step, entry):
    assert common.find_line(entry) is not None


def _extract_results(keys, phone_results):
    results = [dict((key, phone_result[key]) for key in keys) for phone_result in phone_results]
    return results
