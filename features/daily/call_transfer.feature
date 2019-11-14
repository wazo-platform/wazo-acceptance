Feature: Call transfer

  Scenario: Multiple blind transfers do not mix up channel
    Given there are telephony users with infos:
      | firstname | lastname | exten | context |
      | User      | A        | 1801  | default |
      | User      | B        | 1802  | default |
      | User      | C        | 1803  | default |
      | User      | D        | 1804  | default |
    Given there are queues
      | name    | display_name | exten | context | users         |
      | queue_a | Queue A      | 3801  | default | 1801@default  |
    Given there is an incall "3801@from-extern" to the queue "queue_a"

    When chan_test calls "3801@from-extern"
    When I wait "2" seconds for the call processing
    Then "User A" is ringing

    When "User A" answers
    When "User A" does a blind transfer to "1802@default" with API
    Then "User B" is ringing

    When "User B" answers
    Then "User A" is hungup

    When "User C" calls "1801"
    Then "User A" is ringing

    When "User A" answers
    When "User A" does a blind transfer to "1804@default" with API
    Then "User D" is ringing

    When "User D" answers
    Then "User A" is hungup

    Then "User B" is talking
    Then "User C" is talking
    Then "User D" is talking

    When "User D" hangs up
    Then "User C" is hungup
    Then "User B" is talking
