Feature: Stats generation

  Scenario: Placing calls make new queue stats
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
    When I wait 2 seconds to simulate call center
    When chan_test hangs up channel with id "3521-answered"

    # Abandoned call
    When chan_test calls "3521@default" with id "3521-abandoned"
    When I wait 2 seconds to simulate call center
    When chan_test hangs up channel with id "3521-abandoned"

    # Blocked call
    When I unlog agent "021" from API
    When chan_test calls "3521@default" with id "3521-blocked"
    When I wait 2 seconds to simulate call center
    When chan_test hangs up channel with id "3521-blocked"

    When I wait 3 seconds for the call processing
    When I generate contact center stats
    Then contact center stats for queue "stat-queue" in the current hour are:
      | answered | received | abandoned | blocked |
      |        1 |        3 |         1 |       1 |

  Scenario: Agent pause and login time
    Given there is no queue_log for agent "1003"
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | agent_number |
      | Stat      | Agent    | 1003  | default | 1003         |
    Given there are queues with infos:
      | name       | exten | context | agents |
      | stat-queue | 3521  | default | 1003   |
    Given there are no hour change in the next 30 seconds
    
    # First cycle
    When I log agent "1003" from API
    When I pause agent "1003"
    When I wait 2 seconds during my pause
    When I unpause agent "1003"
    When I wait 3 seconds while being logged on
    When I unlog agent "1003" from API

    # Second cycle
    When I log agent "1003" from API
    When I pause agent "1003"
    When I wait 2 seconds during my pause
    When I unpause agent "1003"
    When I wait 1 seconds while being logged on
    When I unlog agent "1003" from API

    When I wait 1 seconds for the call processing
    When I generate contact center stats
    Then contact center stats for agent "1003" in the current hour are:
      | login_time | pause_time |
      |          8 |          4 |


  Scenario: Agent wrapup and conversation time
      Given there is no queue_log for agent "1003"
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | agent_number |
      | Stat      | Agent    | 1003  | default | 1003         |
    Given there are queues with infos:
      | name         | exten | context | agents | option_wrapuptime |
      | stat-queue_1 | 3521  | default | 1003   | 2                 |
      | stat-queue_2 | 3522  | default | 1003   | 0                 |
    Given there are no hour change in the next 30 seconds
    Given agent "1003" is logged

    # First call 2 seconds in conversation 2 seconds wrapup
    When chan_test calls "3521@default" with id "3521-answered"
    When I wait 1 seconds to simulate call center
    When "Stat Agent" answers
    When I wait 2 seconds to simulate call center
    When chan_test hangs up channel with id "3521-answered"
    When I wait 2 seconds until the wrapup completes

    # Second call 3 seconds in conversation
    When chan_test calls "3522@default" with id "3522-answered"
    When I wait 1 seconds to simulate call center
    When "Stat Agent" answers
    When I wait 3 seconds to simulate call center
    When chan_test hangs up channel with id "3522-answered"

    When I generate contact center stats
    Then contact center stats for agent "1003" in the current hour are:
      | wrapup_time | conversation_time |
      |           2 |                 5 |

  Scenario: Placing calls make new qos stats
    Given there is no queue_log for queue "stat-queue"
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone | agent_number |
      | Stat      | Agent    | 1523  | default | yes        | 023          |
    Given there are queues with infos:
      | name       | exten | context | agents |
      | stat-queue | 3523  | default | 023    |
    Given there are no hour change in the next 30 seconds
    Given agent "023" is logged

    When chan_test places calls in order:
      | exten | context | call_id                |
      |  3523 | default | 3523-answered-qos5     |
      |  3523 | default | 3523-answered-qos15-1  |
      |  3523 | default | 3523-answered-qos15-2  |
      |  3523 | default | 3523-answered-qos20    |
      |  3523 | default | 3523-abandoned-qos10-1 |
      |  3523 | default | 3523-abandoned-qos10-2 |
      |  3523 | default | 3523-abandoned-qos20   |
    When I wait 1 seconds for the call processing

    # QoS 5 seconds
    When "Stat Agent" answers
    When "Stat Agent" hangs up
    When I wait 5 seconds to simulate call center

    # QoS 10 seconds
    When chan_test hangs up channel with id "3523-abandoned-qos10-1"
    When chan_test hangs up channel with id "3523-abandoned-qos10-2"
    When I wait 5 seconds to simulate call center

    # QoS 15 seconds
    When "Stat Agent" answers
    When "Stat Agent" hangs up
    When "Stat Agent" answers
    When "Stat Agent" hangs up
    When I wait 5 seconds to simulate call center

    # QoS 20 seconds
    When "Stat Agent" answers
    When chan_test hangs up channel with id "3523-abandoned-qos20"
    When "Stat Agent" hangs up

    When I wait 5 seconds for the call processing
    When I generate contact center stats
    Then contact center qos stats for queue "stat-queue" in the current hour are:
      | qos_threshold | answered | abandoned |
      |             5 |        1 |         0 |
      |            10 |        0 |         2 |
      |            15 |        2 |         0 |
      |     remainder |        1 |         1 |
