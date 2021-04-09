Feature: Call transfer

  Scenario: Multiple blind transfers do not mix up channels
    Given there are telephony users with infos:
      | firstname | lastname | exten | context |
      | User      | A        | 1801  | default |
      | User      | B        | 1802  | default |
      | User      | C        | 1803  | default |
      | User      | D        | 1804  | default |
    Given there are queues with infos:
      | name    | exten | context | users        |
      | queue_a | 3801  | default | 1801@default |
    Given there is an incall "3801@from-extern" to the queue "queue_a"

    When chan_test calls "3801@from-extern"
    When I wait 2 seconds for the call processing
    Then "User A" is ringing

    When "User A" answers
    When I wait 1 seconds for the call processing
    When "User A" does a blind transfer to "1802@default" with API
    When I wait 3 seconds for wazo-calld load to drop
    Then "User B" is ringing

    When "User B" answers
    Then "User A" is hungup

    When "User C" calls "1801"
    Then "User A" is ringing

    When "User A" answers
    When I wait 1 seconds for the call processing
    When "User A" does a blind transfer to "1804@default" with API
    When I wait 3 seconds for wazo-calld load to drop
    Then "User D" is ringing

    When "User D" answers
    Then "User A" is hungup

    Then "User B" is talking
    Then "User C" is talking
    Then "User D" is talking

    When "User D" hangs up
    Then "User C" is hungup
    Then "User B" is talking

  Scenario: Complete attended transfer, cancel transfer and parking recovery
    Given there are telephony users with infos:
      | firstname | lastname | exten | context |
      | User      | A        | 1801  | default |
      | User      | B        | 1802  | default |
    Given there are queues with infos:
      | name    | exten | context | users        |
      | queue_a | 3801  | default | 1801@default |
    Given there is an incall "3801@from-extern" to the queue "queue_a"
    Given there are parking lots with infos:
      | name     | slots_start | slots_end | exten | context |
      | parking1 | 1851        | 1851      | 1850  | default |

    When incoming call received from "incall" to "3801@from-extern"
    When I wait 2 seconds for the call processing
    Then "User A" is ringing

    When "User A" answers
    When I wait 1 seconds for the call processing
    When "User A" does an attended transfer to "1802@default" with API
    Then "User A" is talking
    Then "incall" is holding
    Then "User B" is ringing

    When "User A" cancel the transfer with API
    Then "User A" is talking
    Then "incall" is talking
    Then "User B" is hungup

    When "User A" does an attended transfer to "1802@default" with API
    Then "User A" is talking
    Then "incall" is holding
    Then "User B" is ringing

    When "User B" answers
    Then "User A" is talking
    # Then "incall" is holding  # issue WAZO-1470
    Then "User B" is talking

    When "User B" hangs up
    Then "User A" is talking
    Then "incall" is talking
    Then "User B" is hungup

    When I wait 0.5 seconds for the transfer lock release
    When "User A" does an attended transfer to "1850@default" with API
    When "User A" complete the transfer with API
    Then "User A" is hungup
    Then "incall" is talking
    Then "User B" is hungup

    When "User A" calls "1851"
    When I wait 1 seconds for the call processing
    Then "User A" is talking
    Then "incall" is talking

    When "User A" does an attended transfer to "1802@default" with API
    When "User B" answers
    Then "User A" is talking
    Then "incall" is talking
    Then "User B" is talking

    When "User A" complete the transfer with API
    Then "User A" is hungup
    Then "incall" is talking
    Then "User B" is talking
