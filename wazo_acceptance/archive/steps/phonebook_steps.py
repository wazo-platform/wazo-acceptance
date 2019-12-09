# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step, world

from xivo_acceptance.action.dird import phonebook as phonebook_action_dird


@step(u'Given there are entries in the phonebook "([^"]*)"')
def given_there_are_entries_in_the_phonebook_1(step, phonebook_name):
    entity = world.config['default_entity'].replace('_', '')
    for entry in step.hashes:
        phonebook_action_dird.remove_entry_if_exists(entry, phonebook_name, entity)
        phonebook_action_dird.create_entry(entry, phonebook_name, entity)
