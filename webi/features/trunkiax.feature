Feature: TrunkIAX

    Scenario: Add a trunkiax
        Given I am logged in
        Given there is no trunkiax "tokyo_paris"
        When I create a trunkiax with name "tokyo_paris"
        Then trunkiax "tokyo_paris" is displayed in the list

    Scenario: Remove a trunkiax
        Given I am logged in
        Given there is a trunkiax "tokyo_paris"
        When I remove the trunkiax "tokyo_paris"
        Then trunkiax "tokyo_paris" is not displayed in the list
