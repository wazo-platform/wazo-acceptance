Feature: Call Record

  Scenario: Default call with extension callrecord enabled
    Given the "callrecord" extension is enabled
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone |
      | User      | 800      | 1800  | default | yes        |
      | User      | 801      | 1801  | default | yes        |
    Given "User 800" has no call recording
    When a call is started:
      | caller   | dial | callee   | talk_time | hangup |
      | User 800 | 1801 | User 801 | 3         | callee |
    Then "User 800" has no call recording

  Scenario: Call recorded when call record is enabled
    Given there are telephony users with infos:
      | firstname | lastname | call_record_outgoing_internal_enabled | exten | context | with_phone |
      | User      | 800      | yes                                   | 1800  | default | yes        |
      | User      | 801      | no                                    | 1801  | default | yes        |
    Given "User 800" has no call recording
    When a call is started:
      | caller   | dial | callee   | talk_time | hangup |
      | User 800 | 1801 | User 801 | 3         | callee |
    Then "User 800" has a call recording with "User 801"
