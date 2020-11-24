Feature: Stats generation

  Scenario: Placing calls make new stats
    Given there is no queue_log for queue "stat-queue"
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone | agent_number |
      | Stat      | Agent    | 1521  | default | yes        | 021          |
    Given there are queues with infos:
      | name       | exten | context | agents | option_joinempty |
      | stat-queue | 3521  | default | 021    | unavailable      |
    Given there are no hour change in the next 30 seconds
    Given agent "021" is logged

    # Answered call
    When chan_test calls "3521@default" with id "3521-answered"
    When I wait 3 seconds to simulate call center
    When "Stat Agent" answers
    When I wait 1 seconds to simulate call center
    When chan_test hangs up channel with id "3521-answered"

    # Abandoned call
    When chan_test calls "3521@default" with id "3521-abandoned"
    When I wait 1 seconds to simulate call center
    When chan_test hangs up channel with id "3521-abandoned"

    # Blocked call
    When I unlog agent "021" from phone
    When I wait 3 seconds for the call processing
    When chan_test calls "3521@default" with id "3521-blocked"
    When I wait 1 seconds to simulate call center
    When chan_test hangs up channel with id "3521-blocked"

    When I wait 3 seconds for the call processing
    When I generate contact center stats
    Then contact center stats for queue "stat-queue" in the current hour are:
      | answered | received | abandoned | blocked |
      |        1 |        3 |         1 |       1 |
