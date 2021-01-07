Feature: Call Record

  Scenario: Default call with extension callrecord enabled
    Given call record directories are empty
    Given the "callrecord" extension is enabled
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone |
      | User      | 800      | 1800  | default | yes        |
      | User      | 801      | 1801  | default | yes        |
    When a call is started:
      | caller   | dial | callee   | talk_time | hangup |
      | User 800 | 1801 | User 801 | 3         | callee |
    Then call record directories are empty

  Scenario: Call recorded when call record is enabled
    Given call record directories are empty
    Given there are telephony users with infos:
      | firstname | lastname | call_record_enabled | exten | context | with_phone |
      | User      | 800      | yes                 | 1800  | default | yes        |
      | User      | 801      | no                  | 1801  | default | yes        |
    When a call is started:
      | caller   | dial | callee   | talk_time | hangup |
      | User 800 | 1801 | User 801 | 3         | callee |
    Then call record directories are not empty
