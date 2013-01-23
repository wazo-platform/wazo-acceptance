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
            | Bob       | Smith    | 24101  | default |
        When I create the following queues:
            | name   | display name | number | context | agents        |
            | queue1 | Queue 1      | 3101   | default | 24101@default |
        Then the agent "24101" is not a member of the queue "queue1" in asterisk

    Scenario: Add a logged agent to a new queue
        Given I have the following agents with a user:
            | firstname | lastname | number | context |
            | John      | Doe      | 24102  | default |
        When I log agent "24102"
        Then the agent "24102" is not a member of the queue "queue2" in asterisk
        When I create the following queues:
            | name   | display name | number | context | agents        |
            | queue2 | Queue 2      | 3102   | default | 24102@default |
        Then the agent "24102" is a member of the queue "queue2" in asterisk

    Scenario: Delete a queue with logged agents
        Given I have the following agents with a user:
            | firstname | lastname | number | context |
            | Wayne     | Brady    | 24103  | default |
        Given there are queues with infos:
            | name   | display name | number | context | agents_number |
            | queue3 | Queue 3      | 3103   | default | 24103         |
        When I log agent "24103"
        Then the agent "24103" is a member of the queue "queue3" in asterisk
        When I delete the queue with number "3103"
        Then the queue "queue3" does not exist in asterisk

    Scenario: Add an unlogged agent to an existing queue
        Given I have the following agents with a user:
            | firstname | lastname | number | context |
            | Brad      | Pitt     | 24104  | default |
        Given there are queues with infos:
            | name   | display name | number | context |
            | queue4 | Queue 4      | 3104   | default |
        When I add the agent with extension "24104@default" to the queue "queue4"
        Then the agent "24104" is not a member of the queue "queue4" in asterisk

    Scenario: Remove an unlogged agent from an existing queue
        Given I have the following agents with a user:
            | firstname | lastname   | number | context |
            | Alice     | Wonderland | 24105  | default |
        Given there are queues with infos:
            | name   | display name | number | context | agents_number |
            | queue5 | Queue 5      | 3105   | default | 24105         |
        When I remove the agent with extension "24105@default" from the queue "queue5"
        Then the agent "24105" is not a member of the queue "queue5" in asterisk

    Scenario: Add a logged agent to an existing queue
        Given I have the following agents with a user:
            | firstname | lastname | number | context |
            | Cookie    | Monster  | 24107  | default |
        Given there are queues with infos:
            | name   | display name | number | context |
            | queue7 | Queue 7      | 3107   | default |
        When I log agent "24107"
        Then the agent "24107" is not a member of the queue "queue7" in asterisk
        When I add the agent with extension "24107@default" to the queue "queue7"
        Then the agent "24107" is a member of the queue "queue7" in asterisk

    Scenario: Remove a logged agent from an existing queue
        Given I have the following agents with a user:
            | firstname | lastname | number | context |
            | Bugs      | Bunny    | 24108  | default |
        Given there are queues with infos:
            | name   | display name | number | context | agents_number |
            | queue8 | Queue 8      | 3108   | default | 24108         |
        When I log agent "24108"
        Then the agent "24108" is a member of the queue "queue7" in asterisk
        When I remove the agent with extension "24108@default" from the queue "queue8"
        Then the agent "24108" is not a member of the queue "queue8" in asterisk
