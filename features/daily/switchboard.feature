Feature: Switchboards

  Scenario: Workflow
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone | with_token |
      | Manager   | Inn      | 1802  | default | yes        | yes        |
      | Reception | Clerk    | 1801  | default | yes        | yes        |
    Given there are switchboards with infos:
      | name | members         |
      | Inn  | Reception Clerk |
    Given there is an incall "1000@from-extern" to the switchboard "Inn"
    Given I listen on the bus for "switchboard_queued_calls_updated" messages
    When incoming call received from "incall" to "1000@from-extern"
    Then I receive a "switchboard_queued_calls_updated" event
    Then switchboard "Inn" has "incall" in queued calls
    When "Reception Clerk" answer queued call "incall" from switchboard "Inn"
    Then "Reception Clerk" is talking to "incall"

    When I wait 1 seconds for the call processing
    When "Reception Clerk" put call "incall" from switchboard "Inn" on hold
    Then switchboard "Inn" has "incall" in held calls
    When "Reception Clerk" answer held call "incall" from switchboard "Inn"
    Then "Reception Clerk" is talking to "incall"

    When I wait 1 seconds for the call processing
    When "Reception Clerk" does a blind transfer to "1802@default" with API
    When I wait 3 seconds for wazo-calld load to drop
    Given I listen on the bus for "call_updated" messages
    When "Manager Inn" answers
    Then I receive a "call_updated" event with data:
      | peer_caller_id_number |
      | incall                |
    # NOTE(fblackburn): Ideally, the phone will support PAI header
    Then "Manager Inn" is talking to "incall" from API

  Scenario: Timeout
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone | with_token |
      | Reception | Clerk    | 1801  | default | yes        | yes        |
    Given there are switchboards with infos:
        | name                 | members         | timeout | noanswer_destination |
        | timeout              | Reception Clerk |      15 | hangup:              |
        | no-timeout           |                 |         | hangup:              |
        | no-fallback          |                 |       1 |                      |
        | transfer-destination |                 |         |                      |

    Given there is an incall "1001@from-extern" to the switchboard "timeout"
    Given there is an incall "1002@from-extern" to the switchboard "no-timeout"
    Given there is an incall "1003@from-extern" to the switchboard "no-fallback"
    Given there is an incall "1004@from-extern" to the switchboard "transfer-destination"

    When incoming call received from "i-will-timeout" to "1001@from-extern"
    When incoming call received from "i-will-not-timeout-1" to "1002@from-extern"
    When incoming call received from "i-will-not-timeout-2" to "1003@from-extern"
    When incoming call received from "i-will-be-transferred-to-switchboard" to "1001@from-extern"
    When incoming call received from "i-will-be-answered" to "1001@from-extern"
    When I wait 2 seconds for the call processing

    # Transfer call to another switchboard
    Then switchboard "timeout" has "i-will-be-transferred-to-switchboard" in queued calls
    When "Reception Clerk" answer queued call "i-will-be-transferred-to-switchboard" from switchboard "timeout"
    Then "Reception Clerk" is talking to "i-will-be-transferred-to-switchboard"
    When I wait 1 seconds for the call processing
    When "Reception Clerk" does a blind transfer to "1004@from-extern" with API

    # Answer next call
    Then switchboard "timeout" has "i-will-be-answered" in queued calls
    When "Reception Clerk" answer queued call "i-will-be-answered" from switchboard "timeout"

    When I wait 10 seconds for the timeout to expire

    Then "Reception Clerk" is talking to "i-will-be-answered" from API
    Then "i-will-timeout" is hungup
    Then switchboard "no-timeout" has "i-will-not-timeout-1" in queued calls
    Then switchboard "no-fallback" has "i-will-not-timeout-2" in queued calls

    # Should be Caller ID "i-will-be-transferred-to-switchboard", 
    # but is "Reception Clerk" due to an Asterisk bug on Local channels
    Then switchboard "transfer-destination" has "Reception Clerk" in queued calls
