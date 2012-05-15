Feature: Profile

    Scenario: Add a CTI profile
        Given I am logged in
        When I add a CTI profile
        When I set the profile name to "TEST"
        When I submit with errors
        Then I get errors
        When I set the profile name to "test"
        When I submit
        Then I see no errors
