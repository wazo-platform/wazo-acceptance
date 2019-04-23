# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step

from xivo_acceptance.helpers import directory_helper


@step(u'Given the directory definition "([^"]*)" does not exist')
def given_the_directory_definition_does_not_exist(step, definition):
    pass


@step(u'Given the internal directory exists')
def given_the_internal_directory_exists(step):
    directory_helper.configure_internal_directory()


@step(u'Given the directory definition "([^"]*)" is included in the default directory')
def given_the_directory_definition_group1_is_included_in_the_default_directory(step, definition):
    pass


@step(u'Given I add the following CTI directory definition:')
def given_i_add_the_following_cti_directory_definition(step):
    pass


@step(u'Given I map the following fields and save the directory definition:')
def given_i_map_the_following_fields_and_save_the_directory_definition(step):
    pass
