Feature: Queues

    Scenario: Add queue named with non-ASCII characters
        Given I am logged in
        Given there is no queue "Épicerie"
        Given there is no queue with number "3000"
        When I add a queue
        When I set the text field "Name" to "epicerie"
        When I set the text field "Display name" to "Épicerie"
        When I set the text field "Number" to "3000"
        When I submit
        Then queue "Épicerie" is displayed in the list

    Scenario: Cannot add queue named general
        Given I am logged in
        Given there is no queue with number "3001"
        When I add a queue
        When I set the text field "Name" to "general"
        When I set the text field "Display name" to "general"
        When I set the text field "Number" to "3001"
        When I submit with errors
        Then I get errors
