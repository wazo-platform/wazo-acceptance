Feature: Group

    Scenario: Add a group with name and number and remove it
        Given there is no group "2000"
        Given there is no group with name "administrative"
        When I create a group "Administrative" with number "2000"
        Then group "administrative" is displayed in the list
        When I remove the group "administrative"
        Then group "administrative" is not displayed in the list

    Scenario: Cannot add a group with a name general
        Given there is no group "2001"
        When I create a group "general" with number "2001" with errors
        Then I see errors
