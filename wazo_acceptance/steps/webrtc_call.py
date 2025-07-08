# Copyright 2013-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import time

from behave import then, when
from hamcrest import assert_that, equal_to


@when('a webrtc endpoint calls sip one')
def when_a_webrtc_endpoint_calls_sip_one(context):
    def _call(caller, dial, callee, ring_time=10):
        caller_phone = context.webrtc
        callee_phone = context.phone_register.get_phone(callee)

        caller_phone.call(dial)
        time.sleep(int(ring_time))
        callee_phone.answer()

    for call_info in context.table:
        _call(**call_info.as_dict())


@then('WebRTC channel uses following codecs')
def WebRTC_channel_uses_following_codecs(context):
    context.table.require_columns(['asterisk_codec', 'direct_client_codec', 'sbc_client_codec'])
    sbc = context.config.userdata.get('sbc', 'False')
    for row in context.table:
        body = row.as_dict()

        browser_codec = body['sbc_client_codec'] if sbc == "True" else body['direct_client_codec']
        (incoming, outgoing) = context.webrtc.get_codecs()
        assert_that((incoming, outgoing), equal_to((browser_codec, browser_codec)))

        current_asterisk_codec = context.helpers.asterisk.get_current_call_codec(context.webrtc.sip_username)
        expected_asterisk_codec = body['asterisk_codec']
        assert_that(current_asterisk_codec, equal_to(expected_asterisk_codec))

    context.webrtc.hangup()
