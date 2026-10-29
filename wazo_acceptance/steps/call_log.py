# Copyright 2013-2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import then
from hamcrest import all_of, assert_that, greater_than, has_entries, less_than
from wazo_test_helpers import until


def close_to(target, delta):
    minimum = target - delta
    maximum = target + delta
    return all_of(greater_than(minimum), less_than(maximum))


@then('I have the last call log matching:')
def then_i_have_the_last_call_log_matching(context):
    expected = context.table[0].as_dict()
    expected_duration = int(expected.pop('duration', 0))
    if expected.get('answered'):
        expected['answered'] = expected['answered'] == 'True'

    def _assert():
        cdr = context.call_logd_client.cdr.list(direction='desc', limit=1, recurse=True)
        last_call_log = cdr['items'][0]
        assert_that(last_call_log, has_entries(expected))
        if expected_duration:
            assert_that(last_call_log['duration'], close_to(expected_duration, 2))

    until.assert_(_assert, tries=5)


@then('the last call log has participants:')
def then_the_last_call_log_has_participants(context):
    expected = {}
    for row in context.table:
        firstname, lastname = row['user'].split()
        user = context.helpers.confd_user.get_by(firstname=firstname, lastname=lastname)
        role = row['role']
        expected[f'{role}_user_uuid'] = user['uuid']
        contact_number = int(row.get('contact') or 1)
        phone = context.phone_register.get_phone(row['user'], contact_number - 1)
        endpoint_name = phone.sip_contact_uri.split('/')[1]
        line = next(line for line in user['lines'] if line['name'] == endpoint_name)
        expected[f'{role}_line_id'] = line['id']

    def _assert():
        cdr = context.call_logd_client.cdr.list(direction='desc', limit=1, recurse=True)
        assert_that(cdr['items'][0], has_entries(expected))

    until.assert_(_assert, tries=5)
