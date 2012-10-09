Feature: Profile

    Scenario: Add a CTI profile
        Given there is no profile "test"
        Given there is no profile "TEST"
        When I add a CTI profile
        When I set the profile name to "TEST"
        When I submit with errors
        Then I see errors
        When I set the profile name to "test"
        When I submit
        Then I see no errors

    Scenario: Remove a CTI profile that is associated with a user
        Given there is a user "Alfredo" "Buenanote" with extension "1482@default" and CTI profile "Client"
        Then I can't remove profile "Client"
