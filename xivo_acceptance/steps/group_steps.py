# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step

from xivo_acceptance.helpers import user_helper, group_helper
from xivo_acceptance.lettuce import func


@step(u'Given there are groups:')
def given_there_are_groups(step):
    pass


@step(u'Given there is a group "([^"]*)" with extension "([^"]*)" and users:$')
def given_there_is_a_group_with_extension_and_users(step, name, extension):
    number, context = func.extract_number_and_context_from_extension(extension)

    users = []
    for info in step.hashes:
        user = user_helper.get_by_firstname_lastname(info['firstname'], info.get('lastname'))
        users.append(user)

    group_helper.add_or_replace_group(name, number, context, users)
