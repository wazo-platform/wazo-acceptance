Feature: Profile

    Scenario: Add a CTI profile
        Given there is no CTI profile "test"
        Given there is no CTI profile "TEST"
        When I add the CTI profile "TEST"
        Then I see no errors
        When I add the CTI profile "test"
        Then I see no errors

    Scenario: Remove a CTI profile that is associated with a user
        Given there is a user "Alfredo" "Buenanote" with extension "1482@default" and CTI profile "Client"
        Then I can't remove profile "Client"
