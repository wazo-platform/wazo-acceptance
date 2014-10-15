Feature: TrunkIAX

    Scenario: Add a trunkiax
        Given there is no trunkiax "tokyo_paris"
        When I create a trunkiax with name "tokyo_paris"
        Then trunkiax "tokyo_paris" is displayed in the list
        Then the "iax.conf" file should contain peer "tokyo_paris"

    Scenario: Remove a trunkiax
        Given there is a trunkiax "tokyo_paris"
        When I remove the trunkiax "tokyo_paris"
        Then trunkiax "tokyo_paris" is not displayed in the list
        Then the "iax.conf" file should not contain peer "tokyo_paris"
