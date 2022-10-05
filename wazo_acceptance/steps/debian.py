# Copyright 2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import given
from hamcrest import assert_that, equal_to


@given('the "{package_name}" Debian package is installed')
def given_package_is_installed(context, package_name):
    assert_that(
        context.remote_sysutils.send_command(['apt-get', 'update'], check=True),
        equal_to(True),
    )
    assert_that(
        context.remote_sysutils.send_command(['apt-get', '-y', 'install', package_name], check=True),
        equal_to(True),
    )
