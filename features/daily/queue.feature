Feature: Queues

  Scenario: Add a logged agent to a new queue and answer a call
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | agent_number |
      | John      | Doe      | 1102  | default | 1102         |
    When I log agent "1102" from phone
    When I create the following queues:
      | name   | label   | exten | context | agents |
      | queue2 | Queue 2 | 3102  | default | 1102   |

    Given there is an incall "3102@from-extern" to the queue "queue2"

    When chan_test calls "3102@from-extern" with id "3102-1"
    When I wait "1" seconds for the call processing
    When "John Doe" answers
    When I wait "1" seconds for the call processing
    When "John Doe" hangs up
    When chan_test hangs up channel with id "3102-1"
    When I wait "1" seconds for the call processing
