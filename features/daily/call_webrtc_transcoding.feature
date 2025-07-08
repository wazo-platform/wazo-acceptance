@transcoding
Feature: Call Transcoding

  Scenario: Call between linphone and WebRTC
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | webrtc |
      | Alice     | 1100     | 1100  | default | no     |
      | Wayne     | 1120     | 1120  | default | yes    |
    When a webrtc endpoint calls sip one:
      | caller      | dial | callee      |
      | Wayne 1120  | 1100 | Alice 1100  |
    Then WebRTC channel uses following codecs:
      | asterisk_codec | direct_client_codec | sbc_client_codec |
      | ulaw           | PCMU                | Opus             |
