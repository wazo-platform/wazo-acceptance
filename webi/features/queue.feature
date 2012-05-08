Feature: Queues

    Scenario: Add queue named with non-ASCII characters
        Given I am logged in
        Given there is no queue "Épicerie"
        Given there is no queue with number "301"
        Given there is a context interval for queue "301"
        When I add a queue
        When I set the text field "Name" to "epicerie"
        When I set the text field "Display name" to "Épicerie"
        When I set the text field "Number" to "301"
        When I submit
        Then queue "Épicerie" is displayed in the list
