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


@then('WebRTC channel uses "{asterisk_codec}" on the asterisk side and "{browser_codec}" on the browser')
def WebRTC_call_channel_codecs(context, asterisk_codec, browser_codec):
    (incoming, outgoing) = context.webrtc.get_codecs()
    assert_that((incoming, outgoing), equal_to((browser_codec, browser_codec)))
    assert_that(context.helpers.asterisk.get_current_call_codec(context.webrtc.sip_username), equal_to(asterisk_codec))
    context.webrtc.hangup()
