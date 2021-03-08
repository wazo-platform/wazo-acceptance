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
    # NOTE(fblackburn): Ideally, the phone will support auto answer headers
    When "Reception Clerk" answers
    Then "Reception Clerk" is talking to "incall"

    When "Reception Clerk" put call "incall" from switchboard "Inn" on hold
    Then switchboard "Inn" has "incall" in held calls
    When "Reception Clerk" answer held call "incall" from switchboard "Inn"
    # NOTE(fblackburn): Ideally, the phone will support auto answer headers
    When "Reception Clerk" answers
    Then "Reception Clerk" is talking to "incall"

    When "Reception Clerk" does a blind transfer to "1802@default" with API
    When I wait 3 seconds for wazo-calld load to drop
    Given I listen on the bus for "call_updated" messages
    When "Manager Inn" answers
    Then I receive a "call_updated" event with data:
      | peer_caller_id_number |
      | incall                |
    # NOTE(fblackburn): Ideally, the phone will support PAI header
    Then "Manager Inn" is talking to "incall" from API
