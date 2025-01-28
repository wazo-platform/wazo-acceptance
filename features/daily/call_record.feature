Feature: Call Record

  Scenario: Default call with extension callrecord enabled
    Given the "callrecord" extension is enabled
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone |
      | User      | Chen     | 1800  | default | yes        |
      | User      | 801      | 1801  | default | yes        |
    Given "User Chen" has no call recording
    Given I listen on the bus for "call_log_created" messages
    When a call is started:
      | caller    | dial | callee   | talk_time | hangup |
      | User Chen | 1801 | User 801 | 3         | callee |
    Then I receive a "call_log_created" event with data:
      | source_name | destination_name |
      | User Chen   | User 801         |
    Then "User Chen" has no call recording

  Scenario: Call recorded when call record is enabled
    Given there are telephony users with infos:
      | firstname | lastname | call_record_outgoing_internal_enabled | exten | context | with_phone |
      | User      | Clark    | yes                                   | 1800  | default | yes        |
      | User      | 801      | no                                    | 1801  | default | yes        |
    Given "User Clark" has no call recording
    Given I listen on the bus for "call_log_created" messages
    When a call is started:
      | caller     | dial | callee   | talk_time | hangup |
      | User Clark | 1801 | User 801 | 3         | callee |
    Then I receive a "call_log_created" event with data:
      | source_name | destination_name |
      | User Clark  | User 801         |
    Then "User Clark" has a call recording with "User 801"

  Scenario: Stopping and Starting the recording results in multiple files
    Given there are telephony users with infos:
      | firstname | lastname   | call_record_outgoing_internal_enabled | exten | context | with_phone | online_call_record_enabled |
      | User      | Desjardins | yes                                   | 1800  | default | yes        | yes                        |
      | User      | 801        | no                                    | 1801  | default | yes        | no                         |
    Given "User Desjardins" has no call recording
    Given I listen on the bus for "call_log_created" messages
    When "User Desjardins" calls "1801"
    When "User 801" answers
    When I wait 1 seconds for the call processing
    When "User Desjardins" stops call recording
    When "User Desjardins" starts call recording
    When I wait 1 seconds for the call processing
    When "User 801" hangs up
    Then I receive a "call_log_created" event with data:
      | source_name     | destination_name |
      | User Desjardins | User 801         |
    Then "User Desjardins" has 2 call recordings with "User 801"

  Scenario: Group calls should be recorded if the answerer is configured to be recorded
    Given there are telephony users with infos:
      | firstname | lastname | call_record_incoming_internal_enabled | exten | context | with_phone |
      | User      | Hall     | yes                                   | 1800  | default | yes        |
      | User      | 801      | no                                    | 1801  | default | yes        |
      | User      | 802      | yes                                   | 1802  | default | yes        |
    Given there are telephony groups with infos:
      | label      | exten | context |
      | incoming   |  2514 | default |
    Given the telephony group "incoming" has users:
      | firstname | lastname |
      | User      | Hall     |
    Given the telephony group "incoming" has extensions:
      | context | exten |
      | default | 1802  |
    Given "User Hall" has no call recording
    Given I listen on the bus for "call_log_created" messages
    When "User 801" calls "2514"
    When "User Hall" answers
    When I wait 1 seconds for the call processing
    When "User 801" hangs up
    Then I receive a "call_log_created" event:
      | source_name | destination_name |
      | User 801    | User Hall        |
    Then "User 801" has a call recording with "User Hall"
    Given "User 802" has no call recording
    When "User 801" calls "2514"
    When "User 802" answers
    When I wait 1 seconds for the call processing
    When "User 801" hangs up
    Then I receive a "call_log_created" event:
      | source_name | destination_name |
      | User 801    | User 802         |
    Then "User 801" has a call recording with "User 802"

  Scenario: Group calls should be recorded if the caller is configured to be recorded
    Given there are telephony users with infos:
      | firstname | lastname | call_record_outgoing_internal_enabled | exten | context | with_phone |
      | User      | Pan      | no                                    | 1800  | default | yes        |
      | User      | 801      | yes                                   | 1801  | default | yes        |
    Given there are telephony groups with infos:
      | label      | exten | context |
      | incoming   |  2514 | default |
    Given the telephony group "incoming" has users:
      | firstname | lastname |
      | User      | Pan      |
    Given "User Pan" has no call recording
    Given I listen on the bus for "call_log_created" messages
    When "User 801" calls "2514"
    When "User Pan" answers
    When I wait 1 seconds for the call processing
    When "User 801" hangs up
    Then I receive a "call_log_created" event:
      | source_name | destination_name |
      | User 801    | User Pan         |
    Then "User 801" has a call recording with "User Pan"

  Scenario: Queue calls should be recorded if the answerer is configured to be recorded
    Given there are telephony users with infos:
      | firstname | lastname | call_record_incoming_internal_enabled | exten | context | with_phone | agent_number |
      | User      | Lee      | yes                                   | 1800  | default | yes        |              |
      | User      | 801      | no                                    | 1801  | default | yes        |              |
      | User      | 802      | yes                                   | 1802  | default | yes        | 1234         |
    Given agent "1234" is logged
    Given there are queues with infos:
      | name       | exten | context |
      | incoming   |  3123 | default |
    Given the queue "incoming" has users:
      | firstname | lastname |
      | User      | Lee      |
    Given the queue "incoming" has agents:
      | agent_number |
      | 1234         |
    Given "User Lee" has no call recording
    Given I listen on the bus for "call_log_created" messages
    When "User 801" calls "3123"
    When "User Lee" answers
    When I wait 1 seconds for the call processing
    When "User 801" hangs up
    Then I receive a "call_log_created" event:
      | source_name | destination_name |
      | User 801    | User Lee         |
    Then "User 801" has a call recording with "User Lee"
    Given "User 802" has no call recording
    When "User 801" calls "3123"
    When "User 802" answers
    When I wait 1 seconds for the call processing
    When "User 801" hangs up
    Then I receive a "call_log_created" event:
      | source_name | destination_name |
      | User 801    | User 802         |
    Then "User 801" has a call recording with "User 802"

  Scenario: Queue calls should be recorded if the caller is configured to be recorded
    Given there are telephony users with infos:
      | firstname | lastname | call_record_outgoing_internal_enabled | exten | context | with_phone |
      | User      | Poe      | no                                    | 1800  | default | yes        |
      | User      | 801      | yes                                   | 1801  | default | yes        |
    Given there are queues with infos:
      | name       | exten | context |
      | incoming   |  3123 | default |
    Given the queue "incoming" has users:
      | firstname | lastname |
      | User      | Poe      |
    Given "User Poe" has no call recording
    Given I listen on the bus for "call_log_created" messages
    When "User 801" calls "3123"
    When "User Poe" answers
    When I wait 1 seconds for the call processing
    When "User 801" hangs up
    Then I receive a "call_log_created" event:
      | source_name | destination_name |
      | User 801    | User Poe         |
    Then "User 801" has a call recording with "User Poe"

  Scenario: User to user recording status
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone | online_call_record_enabled |
      | User      | Brown    | 1800  | default | yes        | yes                        |
      | User      | 801      | 1801  | default | yes        | yes                        |
    When "User Brown" calls "1801"
    When "User 801" answers
    When "User Brown" starts call recording
    Then "User Brown" call is recording status is "active"
    Then "User 801" call is recording status is "inactive"
    When "User 801" starts call recording
    Then "User Brown" call is recording status is "active"
    Then "User 801" call is recording status is "active"
    When "User Brown" stops call recording
    Then "User Brown" call is recording status is "inactive"
    Then "User 801" call is recording status is "active"

  Scenario: User to group recording status
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone | online_call_record_enabled |
      | User      | Smith    | 1800  | default | yes        | yes                        |
      | User      | 801      | 1801  | default | yes        | yes                        |
    Given there are telephony groups with infos:
      | label      | exten | context | dtmf_record_toggle |
      | incoming   |  2514 | default | yes                |
    Given the telephony group "incoming" has users:
      | firstname | lastname |
      | User      | 801      |
    When "User Smith" calls "2514"
    When "User 801" answers
    When "User Smith" starts call recording
    Then "User Smith" call is recording status is "active"
    Then "User 801" call is recording status is "inactive"
    When "User 801" starts call recording
    Then "User Smith" call is recording status is "active"
    Then "User 801" call is recording status is "active"
    When "User Smith" stops call recording
    Then "User Smith" call is recording status is "inactive"
    Then "User 801" call is recording status is "active"

  Scenario: User to queue recording status
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone | online_call_record_enabled |
      | User      | Ray      | 1800  | default | yes        | yes                        |
      | User      | 801      | 1801  | default | yes        | yes                        |
    Given there are queues with infos:
      | name       | exten | context | dtmf_record_toggle |
      | incoming   |  3123 | default | yes                |
    Given the queue "incoming" has users:
      | firstname | lastname |
      | User      | 801      |
    When "User Ray" calls "3123"
    When "User 801" answers
    When "User Ray" starts call recording
    Then "User Ray" call is recording status is "active"
    Then "User 801" call is recording status is "inactive"
    When "User 801" starts call recording
    Then "User Ray" call is recording status is "active"
    Then "User 801" call is recording status is "active"
    When "User Ray" stops call recording
    Then "User Ray" call is recording status is "inactive"
    Then "User 801" call is recording status is "active"

  Scenario: Incoming call to user
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone | call_record_incoming_external_enabled | online_call_record_enabled |
      | User      | Boucher  | 1800  | default | yes        | yes                                   | yes                        |
    Given there is an incall "1800@from-extern" to the user "User Boucher"
    Given "User Boucher" has no call recording
    When incoming call received from "5551231234" to "1800@from-extern"
    Given I listen on the bus for "call_log_created" messages
    When "User Boucher" answers
    Then "User Boucher" call is recording status is "active"
    When "User Boucher" stops call recording
    Then "User Boucher" call is recording status is "inactive"
    When "User Boucher" starts call recording
    Then "User Boucher" call is recording status is "active"
    When "User Boucher" hangs up
    Then I receive a "call_log_created" event:
      | destination_name |
      | User Boucher     |
    Then "User Boucher" has 2 call recordings from incoming call "5551231234"

  Scenario: Incoming call to group
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone | call_record_incoming_external_enabled |
      | User      | Baker    | 1800  | default | yes        | yes                                   |
    Given there are telephony groups with infos:
      | label      | exten | context | dtmf_record_toggle |
      | incoming   |  2514 | default | yes                |
    Given the telephony group "incoming" has users:
      | firstname | lastname |
      | User      | Baker    |
    Given there is an incall "2514@from-extern" to the group "incoming"
    Given "User Baker" has no call recording
    When incoming call received from "5551231234" to "2514@from-extern"
    Given I listen on the bus for "call_log_created" messages
    When "User Baker" answers
    Then "User Baker" call is recording status is "active"
    When "User Baker" stops call recording
    Then "User Baker" call is recording status is "inactive"
    When "User Baker" starts call recording
    Then "User Baker" call is recording status is "active"
    When "User Baker" hangs up
    Then I receive a "call_log_created" event:
      | destination_name |
      | User Baker       |
    Then "User Baker" has 2 call recordings from incoming call "5551231234"

  Scenario: Incoming call to queue
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone | call_record_incoming_external_enabled |
      | User      | Anderson | 1800  | default | yes        | yes                                   |
    Given there are queues with infos:
      | name       | exten | context | dtmf_record_toggle |
      | incoming   |  3123 | default | yes                |
    Given the queue "incoming" has users:
      | firstname | lastname |
      | User      | Anderson |
    Given there is an incall "3123@from-extern" to the queue "incoming"
    Given "User Anderson" has no call recording
    When incoming call received from "5551231234" to "3123@from-extern"
    Given I listen on the bus for "call_log_created" messages
    When "User Anderson" answers
    Then "User Anderson" call is recording status is "active"
    When "User Anderson" stops call recording
    Then "User Anderson" call is recording status is "inactive"
    When "User Anderson" starts call recording
    Then "User Anderson" call is recording status is "active"
    When "User Anderson" hangs up
    Then I receive a "call_log_created" event:
      | destination_name |
      | User Anderson    |
    Then "User Anderson" has 2 call recordings from incoming call "5551231234"
