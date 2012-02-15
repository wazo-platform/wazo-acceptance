Feature: User Import

    Scenario: Import simple user from CSV file
        Given I am logged in
        Given there is no user "Francis" "Lalannix"
        When I import a user "Francis" "Lalannix" with a SIP line "1000"
        Then user "Francis" "Lalannix" is displayed in the list
        When user "Francis" "Lalannix" is removed
        Then user "Francis" "Lalannix" is not displayed in the list
