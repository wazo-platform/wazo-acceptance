Feature: Queues

    @skip_old_webi_step
    Scenario: Add a logged agent to a new queue and answer a call
        Given there are users with infos:
          | firstname | lastname | number | context | agent_number | protocol |
          | John      | Doe      |   1102 | default | 1102         | sip      |
        When I log agent "1102"
        When I create the following queues:
          | name   | display name | number | context | agents       |
          | queue2 | Queue 2      | 3102   | default | 1102         |

        Given there is an incall "3102" in context "from-extern" to the "Queue" "queue2"
        Given there is no "CONNECT" entry in queue "queue2"
        Given there is no "COMPLETEAGENT" entry in queue "queue2"
        Given there is no "ENTERQUEUE" entry in queue "queue2"

        When chan_test calls "3102@from-extern" with id "3102-1"
        When I wait 1 seconds for the calls processing
        When "John Doe" answers
        When I wait 1 seconds for the calls processing
        When "John Doe" hangs up
        When chan_test hangs up "3102-1"
        When I wait 1 seconds for the calls processing

        Then I should see 1 "ENTERQUEUE" event in queue "queue2" in the queue log
        Then I should see 1 "CONNECT" event in queue "queue2" in the queue log
        Then I should see 1 "COMPLETEAGENT" event in queue "queue2" in the queue log
