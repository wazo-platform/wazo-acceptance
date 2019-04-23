# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step, world
from hamcrest import assert_that, has_items

from xivo_acceptance.action.dird import phonebook as phonebook_action_dird
from xivo_acceptance.lettuce.aastra import AastraPhonebookBrowser


@step(u'Given the phonebook is accessible by any hosts')
def given_phone_is_accessible_by_any_hosts(step):
    pass


@step(u'Given there are entries in the phonebook "([^"]*)"')
def given_there_are_entries_in_the_phonebook_1(step, phonebook_name):
    entity = world.config['default_entity'].replace('_', '')
    for entry in step.hashes:
        phonebook_action_dird.remove_entry_if_exists(entry, phonebook_name, entity)
        phonebook_action_dird.create_entry(entry, phonebook_name, entity)


@step(u'Given there are local dird phonebooks:')
def given_there_are_local_dird_phonebooks(step):
    pass


@step(u'When I search the phonebook for "([^"]*)" on my Aastra "([^"]*)"$')
def when_i_search_the_phonebook_on_my_aastra(step, term, mac_address):
    phonebook_browser = AastraPhonebookBrowser(mac_address)
    phonebook_browser.use_provd_lookup_url()
    world.phone_results = phonebook_browser.search(term)


@step(u'Then I see the following results on the phone')
def then_i_see_the_following_results_on_the_phone(step):
    expected_results = step.hashes
    results = _extract_results(step.keys, world.phone_results)

    assert_that(results, has_items(*expected_results))


def _extract_results(keys, phone_results):
    results = [dict((key, phone_result[key]) for key in keys) for phone_result in phone_results]
    return results
