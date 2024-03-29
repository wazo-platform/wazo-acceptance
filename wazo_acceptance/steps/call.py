# Copyright 2020-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import then, when
from hamcrest import assert_that, equal_to, is_
from wazo_test_helpers import until


@then('"{firstname} {lastname}" call is "{status}"')
def then_firstname_lastname_call_is_status(context, firstname, lastname, status):
    user_uuid = context.helpers.confd_user.get_by(firstname=firstname, lastname=lastname)['uuid']
    _assert_call_property(context, user_uuid, call_property=status, property_value=True)


@then('"{firstname} {lastname}" call is not "{status}"')
def then_firstname_lastname_call_is_not_status(context, firstname, lastname, status):
    user_uuid = context.helpers.confd_user.get_by(firstname=firstname, lastname=lastname)['uuid']
    _assert_call_property(context, user_uuid, call_property=status, property_value=False)


@when('"{firstname} {lastname}" relocates its call to its contact "{contact_number}"')
def when_firstname_lastname_relocates_its_call_to_its_contact_number(
    context, firstname, lastname, contact_number
):
    tracking_id = f"{firstname} {lastname}"

    contact = int(contact_number) - 1
    dst_line_sip = context.phone_register.get_phone(tracking_id, contact)
    dst_line_sip_username = dst_line_sip.sip_username

    dst_lines = context.confd_client.lines.list(search=dst_line_sip_username, recurse=True)
    dst_line_id = dst_lines['items'][0]['id']

    token = context.helpers.token.get(tracking_id)['token']
    with context.helpers.utils.set_token(context.calld_client, token):
        current_call_id = context.calld_client.calls.list_calls_from_user()['items'][0]['call_id']
        context.calld_client.relocates.create_from_user(
            initiator=current_call_id,
            destination='line',
            location={'line_id': dst_line_id, 'contact': dst_line_sip_username},
        )


@then('"{firstname} {lastname}" is talking to "{caller_id}" from API')
def then_firstname_lastname_is_talking_to_caller_id_from_api(
    context, firstname, lastname, caller_id
):
    tracking_id = f"{firstname} {lastname}"
    token = context.helpers.token.get(tracking_id)['token']
    with context.helpers.utils.set_token(context.calld_client, token):
        calls = context.calld_client.calls.list_calls_from_user()['items']
    assert_that(caller_id, equal_to(calls[0]['peer_caller_id_number']))


def _assert_call_property(context, user_uuid, call_property, property_value):
    def call_is_status():
        call = context.helpers.call.get_by(user_uuid=user_uuid)
        assert_that(call[call_property], is_(property_value))

    until.assert_(call_is_status, tries=3)
