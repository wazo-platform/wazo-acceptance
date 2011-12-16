Feature: TrunkIAX

    Scenario: Add an trunkiax
        Given I am logged in
        Given there is no trunkiax "tokyo_paris"
        When I create an trunkiax with name "tokyo_paris"
        Then there is an trunkiax "tokyo_paris"

    Scenario: Remove an trunkiax
        Given I am logged in
        Given there is an trunkiax "tokyo_paris"
        When I remove the trunkiax "tokyo_paris"
        Then there is no trunkiax "tokyo_paris"
