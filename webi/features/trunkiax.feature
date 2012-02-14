Feature: TrunkIAX

    Scenario: Add a trunkiax
        Given I am logged in
        Given there is no trunkiax "tokyo_paris"
        When I create a trunkiax with name "tokyo_paris"
        Then there is a trunkiax "tokyo_paris"

    Scenario: Remove a trunkiax
        Given I am logged in
        Given there is a trunkiax "tokyo_paris"
        When I remove the trunkiax "tokyo_paris"
        Then there is no trunkiax "tokyo_paris"
