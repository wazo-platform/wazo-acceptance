Feature: REST API Extensions

    Scenario: Delete an extension associated to a queue
        Given there are queues with infos:
            | name     | number | context |
            | ex-queue | 3198   | default |
        When I delete extension "3198@default"
        Then I get a response with status "400"
        Then I get an error message matching "Resource Error - Extension is associated with a queue"
