Feature: User

    Scenario: Add a user with first name and last name and remove it
        Given I am logged in
        Given there is no user "John" "Willis"
        When I create a user "John" "Willis"
        Then user "John Willis" is displayed in the list
        When user "John" "Willis" is removed
        Then user "John Willis" is not displayed in the list

    Scenario: Add a user in a group
        Given I am logged in
        Given a user "Bob" "Marley" in group "rastafarien"
        When I rename "Bob" "Marley" to "Bob" "Dylan"
        Then I should be at the user list page
        Then "Bob" "Dylan" is in group "rastafarien"

    Scenario: Update a user
        Given I am logged in
        Given there is no user "Bill" "Bush"
        When I create a user "Bill" "Bush"
        Then user "Bill Bush" is displayed in the list
        When I rename "Bill" "Bush" to "George" "Clinton"
        Then user "George Clinton" is displayed in the list

    Scenario: Save user and line forms
    # The problem is that saving the user form may erase values previously
    # set in the line form (bug #2918)
        Given I am logged in
        Given there is a user "George" "Clinton" with a SIP line "123"
        When I edit the line "123"
        When I set the select field "NAT" to "No"
        When I go to the "Advanced" tab
        When I set the select field "IP Addressing type" to "Static"
        When I set the text field "IP address" to "10.0.0.1"
        When I submit

        When I edit the line "123"
        When I go to the "IPBX Infos" tab
        Then I see the key "call_limit" has the value "10"

        When I edit the user "George" "Clinton"
        When I submit

        When I edit the line "123"
        Then the select field "NAT" is set to "No"
        When I go to the "Advanced" tab
        Then the select field "IP Addressing type" is set to "Static"
        Then the text field "IP address" is set to "10.0.0.1"
        