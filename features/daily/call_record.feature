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
    Then I receive a "call_log_created" event with data:
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
    Then I receive a "call_log_created" event with data:
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
    Then I receive a "call_log_created" event with data:
      | source_name | destination_name |
      | User 800    | User 801         |
    Then "User 800" has 2 call recordings with "User 801"

  Scenario: Group calls should be recorded if the answerer is configured to be recorded
    Given there are telephony users with infos:
      | firstname | lastname | call_record_incoming_internal_enabled | exten | context | with_phone |
      | User      | 800      | yes                                   | 1800  | default | yes        |
      | User      | 801      | no                                    | 1801  | default | yes        |
      | User      | 802      | yes                                   | 1802  | default | yes        |
    Given there are telephony groups with infos:
      | label      | exten | context |
      | incoming   |  2514 | default |
    Given the telephony group "incoming" has users:
      | firstname | lastname |
      | User      | 800      |
    Given the telephony group "incoming" has extensions:
      | context | exten |
      | default | 1802  |
    Given "User 800" has no call recording
    Given I listen on the bus for "call_log_created" messages
    When "User 801" calls "2514"
    When "User 800" answers
    When I wait 1 seconds for the call processing
    When "User 801" hangs up
    Then I receive a "call_log_created" event:
      | source_name | destination_name |
      | User 801    | User 800         |
    Then "User 801" has a call recording with "User 800"
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
      | User      | 800      | no                                    | 1800  | default | yes        |
      | User      | 801      | yes                                   | 1801  | default | yes        |
    Given there are telephony groups with infos:
      | label      | exten | context |
      | incoming   |  2514 | default |
    Given the telephony group "incoming" has users:
      | firstname | lastname |
      | User      | 800      |
    Given "User 800" has no call recording
    Given I listen on the bus for "call_log_created" messages
    When "User 801" calls "2514"
    When "User 800" answers
    When I wait 1 seconds for the call processing
    When "User 801" hangs up
    Then I receive a "call_log_created" event:
      | source_name | destination_name |
      | User 801    | User 800         |
    Then "User 801" has a call recording with "User 800"

  Scenario: Queue calls should be recorded if the answerer is configured to be recorded
    Given there are telephony users with infos:
      | firstname | lastname | call_record_incoming_internal_enabled | exten | context | with_phone | agent_number |
      | User      | 800      | yes                                   | 1800  | default | yes        |              |
      | User      | 801      | no                                    | 1801  | default | yes        |              |
      | User      | 802      | yes                                   | 1802  | default | yes        | 1234         |
    Given agent "1234" is logged
    Given there are queues with infos:
      | name       | exten | context |
      | incoming   |  3123 | default |
    Given the queue "incoming" has users:
      | firstname | lastname |
      | User      | 800      |
    Given the queue "incoming" has agents:
      | agent_number |
      | 1234         |
    Given "User 800" has no call recording
    Given I listen on the bus for "call_log_created" messages
    When "User 801" calls "3123"
    When "User 800" answers
    When I wait 1 seconds for the call processing
    When "User 801" hangs up
    Then I receive a "call_log_created" event:
      | source_name | destination_name |
      | User 801    | User 800         |
    Then "User 801" has a call recording with "User 800"
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
      | User      | 800      | no                                    | 1800  | default | yes        |
      | User      | 801      | yes                                   | 1801  | default | yes        |
    Given there are queues with infos:
      | name       | exten | context |
      | incoming   |  3123 | default |
    Given the queue "incoming" has users:
      | firstname | lastname |
      | User      | 800      |
    Given "User 800" has no call recording
    Given I listen on the bus for "call_log_created" messages
    When "User 801" calls "3123"
    When "User 800" answers
    When I wait 1 seconds for the call processing
    When "User 801" hangs up
    Then I receive a "call_log_created" event:
      | source_name | destination_name |
      | User 801    | User 800         |
    Then "User 801" has a call recording with "User 800"

  Scenario: User to user recording status
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone |
      | User      | 800      | 1800  | default | yes        |
      | User      | 801      | 1801  | default | yes        |
    When "User 800" calls "1801"
    When "User 801" answers
    When "User 800" starts call recording
    Then "User 800" call is recording status is "active"
    Then "User 801" call is recording status is "inactive"
    When "User 801" starts call recording
    Then "User 800" call is recording status is "active"
    Then "User 801" call is recording status is "active"
    When "User 800" stops call recording
    Then "User 800" call is recording status is "inactive"
    Then "User 801" call is recording status is "active"

  Scenario: User to group recording status
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone |
      | User      | 800      | 1800  | default | yes        |
      | User      | 801      | 1801  | default | yes        |
    Given there are telephony groups with infos:
      | name       | exten | context |
      | incoming   |  2514 | default |
    Given the telephony group "incoming" has users:
      | firstname | lastname |
      | User      | 801      |
    When "User 800" calls "2514"
    When "User 801" answers
    When "User 800" starts call recording
    Then "User 800" call is recording status is "active"
    Then "User 801" call is recording status is "inactive"
    When "User 801" starts call recording
    Then "User 800" call is recording status is "active"
    Then "User 801" call is recording status is "active"
    When "User 800" stops call recording
    Then "User 800" call is recording status is "inactive"
    Then "User 801" call is recording status is "active"

  Scenario: User to queue recording status
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone |
      | User      | 800      | 1800  | default | yes        |
      | User      | 801      | 1801  | default | yes        |
    Given there are queues with infos:
      | name       | exten | context |
      | incoming   |  3123 | default |
    Given the queue "incoming" has users:
      | firstname | lastname |
      | User      | 801      |
    When "User 800" calls "3123"
    When "User 801" answers
    When "User 800" starts call recording
    Then "User 800" call is recording status is "active"
    Then "User 801" call is recording status is "inactive"
    When "User 801" starts call recording
    Then "User 800" call is recording status is "active"
    Then "User 801" call is recording status is "active"
    When "User 800" stops call recording
    Then "User 800" call is recording status is "inactive"
    Then "User 801" call is recording status is "active"

  Scenario: Incoming call to user
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone | call_record_incoming_external_enabled |
      | User      | 800      | 1800  | default | yes        | yes                                   |
    Given there is an incall "1800@from-extern" to the user "User 800"
    Given "User 800" has no call recording
    When incoming call received from "5551231234" to "1800@from-extern"
    Given I listen on the bus for "call_log_created" messages
    When "User 800" answers
    Then "User 800" call is recording status is "active"
    When "User 800" stops call recording
    Then "User 800" call is recording status is "inactive"
    When "User 800" starts call recording
    Then "User 800" call is recording status is "active"
    When "User 800" hangs up
    Then I receive a "call_log_created" event:
      | destination_name |
      | User 800         |
    Then "User 800" has 2 call recordings from incoming call "5551231234"

  Scenario: Incoming call to group
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone | call_record_incoming_external_enabled |
      | User      | 800      | 1800  | default | yes        | yes                                   |
    Given there are telephony groups with infos:
      | name       | exten | context |
      | incoming   |  2514 | default |
    Given the telephony group "incoming" has users:
      | firstname | lastname |
      | User      | 800      |
    Given there is an incall "2514@from-extern" to the group "incoming"
    Given "User 800" has no call recording
    When incoming call received from "5551231234" to "2514@from-extern"
    Given I listen on the bus for "call_log_created" messages
    When "User 800" answers
    Then "User 800" call is recording status is "active"
    When "User 800" stops call recording
    Then "User 800" call is recording status is "inactive"
    When "User 800" starts call recording
    Then "User 800" call is recording status is "active"
    When "User 800" hangs up
    Then I receive a "call_log_created" event:
      | destination_name |
      | User 800         |
    Then "User 800" has 2 call recordings from incoming call "5551231234"

  Scenario: Incoming call to queue
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone | call_record_incoming_external_enabled |
      | User      | 800      | 1800  | default | yes        | yes                                   |
    Given there are queues with infos:
      | name       | exten | context |
      | incoming   |  3123 | default |
    Given the queue "incoming" has users:
      | firstname | lastname |
      | User      | 800      |
    Given there is an incall "3123@from-extern" to the queue "incoming"
    Given "User 800" has no call recording
    When incoming call received from "5551231234" to "3123@from-extern"
    Given I listen on the bus for "call_log_created" messages
    When "User 800" answers
    Then "User 800" call is recording status is "active"
    When "User 800" stops call recording
    Then "User 800" call is recording status is "inactive"
    When "User 800" starts call recording
    Then "User 800" call is recording status is "active"
    When "User 800" hangs up
    Then I receive a "call_log_created" event:
      | destination_name |
      | User 800         |
    Then "User 800" has 2 call recordings from incoming call "5551231234"
