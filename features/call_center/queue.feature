Feature: Queues

    Scenario: Add queue named with non-ASCII characters
        When I add the queue "epicerie" with display name "Épicerie" with extension "3000" in "default"
        Then queue "Épicerie" is displayed in the list

    Scenario: Cannot add queue named general
        When I add the queue "general" with display name "general" with extension "3001" in "default" with errors
        Then I see errors

    Scenario: Queue strategy ring linear
        When I add the queue "green" with extension "3500@default" with ring strategy at "Linear"
        Then I see no errors
        When I edit the queue "green"
        Then I see no errors
        When I edit the queue "green" and set ring strategy at "Ring All"
        Then I see no errors
        When I edit the queue "green" and set ring strategy at "Linear" with errors
        Then I see errors

    Scenario: Add an unlogged agent to a queue
        Given I have the following agents with a user:
            | firstname | lastname | number | context |
            | Bob       | Smith    | 24100  | default |
        When I create the following queues:
            | name   | display name | number | context | agents        |
            | queue1 | Queue 1      | 3101   | default | 24100@default |
        Then the agent "24100" is not logged in
        Then the agent "24100" is not a member of the queue "queue1" in asterisk
