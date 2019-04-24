# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step

from xivo_acceptance.helpers import directory_helper


@step(u'Given the internal directory exists')
def given_the_internal_directory_exists(step):
    directory_helper.configure_internal_directory()
