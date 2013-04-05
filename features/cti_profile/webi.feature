Feature: Profile

    Scenario: Add a CTI profile
        Given there is no CTI profile "test"
        Given there is no CTI profile "TEST"
        When I add the CTI profile "TEST"
        Then I see no errors
        When I add the CTI profile "test"
        Then I see no errors

    Scenario: Remove a CTI profile that is associated with a user
        Given there are users with infos:
         | firstname | lastname  | number | context | cti_profile |
         | Alfredo   | Buenanote | 1482   | default | Client      |
        Then I can't remove profile "Client"
