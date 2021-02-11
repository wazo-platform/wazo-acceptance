Feature: Call Record

  Scenario: Default call with extension callrecord enabled
    Given the "callrecord" extension is enabled
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone |
      | User      | 800      | 1800  | default | yes        |
      | User      | 801      | 1801  | default | yes        |
    Given "User 800" has no call recording
    Given I listen on the bus for "call_log_created" messages
    When a call is started:
      | caller   | dial | callee   | talk_time | hangup |
      | User 800 | 1801 | User 801 | 3         | callee |
    Then I receive a "call_log_created" event:
      | source_name | destination_name |
      | User 800    | User 801         |
    Then "User 800" has no call recording

  Scenario: Call recorded when call record is enabled
    Given there are telephony users with infos:
      | firstname | lastname | call_record_outgoing_internal_enabled | exten | context | with_phone |
      | User      | 800      | yes                                   | 1800  | default | yes        |
      | User      | 801      | no                                    | 1801  | default | yes        |
    Given "User 800" has no call recording
    Given I listen on the bus for "call_log_created" messages
    When a call is started:
      | caller   | dial | callee   | talk_time | hangup |
      | User 800 | 1801 | User 801 | 3         | callee |
    Then I receive a "call_log_created" event:
      | source_name | destination_name |
      | User 800    | User 801         |
    Then "User 800" has a call recording with "User 801"

  Scenario: Stopping and Starting the recording results in multiple files
    Given there are telephony users with infos:
      | firstname | lastname | call_record_outgoing_internal_enabled | exten | context | with_phone |
      | User      | 800      | yes                                   | 1800  | default | yes        |
      | User      | 801      | no                                    | 1801  | default | yes        |
    Given "User 800" has no call recording
    Given I listen on the bus for "call_log_created" messages
    When "User 800" calls "1801"
    When "User 801" answers
    When I wait 1 seconds for the call processing
    When "User 800" stops call recording
    When "User 800" starts call recording
    When I wait 1 seconds for the call processing
    When "User 801" hangs up
    Then I receive a "call_log_created" event:
      | source_name | destination_name |
      | User 800    | User 801         |
    Then "User 800" has 2 call recordings with "User 801"
