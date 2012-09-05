Feature: Profile

    Scenario: Add a CTI profile
        Given there is no profile "test"
        Given there is no profile "TEST"
        When I add a CTI profile
        When I set the profile name to "TEST"
        When I submit with errors
        Then I get errors
        When I set the profile name to "test"
        When I submit
        Then I see no errors
