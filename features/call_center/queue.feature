Feature: Queues

    Scenario: Add queue named with non-ASCII characters
        When I create the following queues:
            | name     | display name | number | context |
            | epicerie | Épicerie     | 3000   | default |
        Then queue "Épicerie" is displayed in the list

    Scenario: Cannot add queue named general
        When I create the following invalid queues:
            | name    | display name | number | context |
            | general | general      | 3001   | default |
        Then I see errors

    Scenario: Queue strategy ring linear
        When I create the following queues:
            | name  | display name | number | context | ring strategy |
            | green | Green        | 3500   | default | Linear        |
        Then I see no errors
        When I edit the queue "green"
        Then I see no errors
        When I edit the queue "green" and set ring strategy at "Ring All"
        Then I see no errors
        When I edit the queue "green" and set ring strategy at "Linear" with errors
        Then I see errors

    Scenario: Add an unlogged agent to a new queue
        Given I have the following agents with a user:
            | firstname | lastname | number | context |
            | Bob       | Smith    | 1101   | default |
        When I create the following queues:
            | name   | display name | number | context | agents       |
            | queue1 | Queue 1      | 3101   | default | 1101@default |
        Then the agent "1101" is not a member of the queue "queue1" in asterisk

    Scenario: Add a logged agent to a new queue
        Given I have the following agents with a user:
            | firstname | lastname | number | context |
            | John      | Doe      | 1102   | default |
        When I log agent "1102"
        When I create the following queues:
            | name   | display name | number | context | agents       |
            | queue2 | Queue 2      | 3102   | default | 1102@default |
        Then the agent "1102" is a member of the queue "queue2" in asterisk

    Scenario: Add a logged agent to a new queue and answer a call
        Given I have the following agents with a user:
            | firstname | lastname | number | context |
            | John      | Doe      | 1102   | default |
        When I log agent "1102"
        When I create the following queues:
            | name   | display name | number | context | agents       |
            | queue2 | Queue 2      | 3102   | default | 1102@default |

        Given there is an incall "3102" in context "from-extern" to the "Queue" "queue2" with caller id name "Lord Greg" number "1234"
        Given there are no calls running
        Given there is no "CONNECT" entry in queue "queue2"
        Given there is no "COMPLETEAGENT" entry in queue "queue2"
        Given there is no "ENTERQUEUE" entry in queue "queue2"

        Given I wait call then I answer then I hang up after "3s"
        When there is 1 calls to extension "3102@from-extern" on trunk "to_incall" and wait
        When I wait 10 seconds for the calls processing

        Then I should see 1 "ENTERQUEUE" event in queue "queue2" in the queue log
        Then I should see 1 "CONNECT" event in queue "queue2" in the queue log
        Then I should see 1 "COMPLETEAGENT" event in queue "queue2" in the queue log

    Scenario: Delete a queue with logged agents
        Given I have the following agents with a user:
            | firstname | lastname | number | context |
            | Wayne     | Brady    | 1103   | default |
        Given there are queues with infos:
            | name   | display name | number | context | agents_number |
            | queue3 | Queue 3      | 3103   | default | 1103          |
        When I log agent "1103"
        Then the agent "1103" is a member of the queue "queue3" in asterisk
        When I delete the queue with number "3103"
        Then the queue "queue3" does not exist in asterisk

    Scenario: Add an unlogged agent to an existing queue
        Given I have the following agents with a user:
            | firstname | lastname | number | context |
            | Brad      | Pitt     | 1104   | default |
        Given there are queues with infos:
            | name   | display name | number | context |
            | queue4 | Queue 4      | 3104   | default |
        When I add the agent with extension "1104@default" to the queue "queue4"
        Then the agent "1104" is not a member of the queue "queue4" in asterisk

    Scenario: Remove an unlogged agent from an existing queue
        Given I have the following agents with a user:
            | firstname | lastname   | number | context |
            | Alice     | Wonderland | 1105   | default |
        Given there are queues with infos:
            | name   | display name | number | context | agents_number |
            | queue5 | Queue 5      | 3105   | default | 1105          |
        When I remove the agent with extension "1105@default" from the queue "queue5"
        Then the agent "1105" is not a member of the queue "queue5" in asterisk

    Scenario: Add a logged agent to an existing queue
        Given I have the following agents with a user:
            | firstname | lastname | number | context |
            | Cookie    | Monster  | 1107   | default |
        Given there are queues with infos:
            | name   | display name | number | context |
            | queue7 | Queue 7      | 3107   | default |
        When I log agent "1107"
        Then the agent "1107" is not a member of the queue "queue7" in asterisk
        When I add the agent with extension "1107@default" to the queue "queue7"
        Then the agent "1107" is a member of the queue "queue7" in asterisk

    Scenario: Add a logged agent to an existing queue and answer a call
        Given I have the following agents with a user:
            | firstname | lastname | number | context |
            | Cookie    | Monster  | 1107   | default |
        Given there are queues with infos:
            | name   | display name | number | context |
            | queue7 | Queue 7      | 3107   | default |
        When I log agent "1107"
        When I add the agent with extension "1107@default" to the queue "queue7"

        Given there is an incall "3107" in context "from-extern" to the "Queue" "queue7" with caller id name "Lord Greg" number "1234"
        Given there are no calls running
        Given there is no "CONNECT" entry in queue "queue7"
        Given there is no "COMPLETEAGENT" entry in queue "queue7"
        Given there is no "ENTERQUEUE" entry in queue "queue7"

        Given I wait call then I answer then I hang up after "3s"
        When there is 1 calls to extension "3107@from-extern" on trunk "to_incall" and wait
        When I wait 10 seconds for the calls processing

        Then I should see 1 "ENTERQUEUE" event in queue "queue7" in the queue log
        Then I should see 1 "CONNECT" event in queue "queue7" in the queue log
        Then I should see 1 "COMPLETEAGENT" event in queue "queue7" in the queue log

    Scenario: Remove a logged agent from an existing queue
        Given I have the following agents with a user:
            | firstname | lastname | number | context |
            | Bugs      | Bunny    | 1108   | default |
        Given there are queues with infos:
            | name   | display name | number | context | agents_number |
            | queue8 | Queue 8      | 3108   | default | 1108          |
        When I log agent "1108"
        Then the agent "1108" is a member of the queue "queue8" in asterisk
        When I remove the agent with extension "1108@default" from the queue "queue8"
        Then the agent "1108" is not a member of the queue "queue8" in asterisk
