# Copyright 2019-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import then
from hamcrest import assert_that, has_entries

from wazo_test_helpers.hamcrest.uuid_ import uuid_


@then('server has uuid')
def then_server_has_uuid(context):
    infos = context.confd_client.infos.get()
    assert_that(infos, has_entries(uuid=uuid_()))
