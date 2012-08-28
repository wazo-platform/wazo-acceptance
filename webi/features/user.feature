Feature: User

    Scenario: Add a user with first name and last name and remove it
        Given I am logged in
        Given there is no user "John" "Willis"
        When I create a user "John" "Willis"
        Then user "John Willis" is displayed in the list
        When I remove user "John" "Willis"
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
        When I rename "Bill" "Bush" to "George" "Orwell"
        Then user "George Orwell" is displayed in the list

    Scenario: Save user and line forms
    # The problem is that saving the user form may erase values previously
    # set in the line form (bug #2918)
        Given I am logged in
        Given there is a user "Tom" "Sawyer" with a SIP line "1001"
        When I edit the line "1001"
        When I set the select field "NAT" to "No"
        When I go to the "Advanced" tab
        When I set the select field "IP Addressing type" to "Static"
        When I set the text field "IP address" to "10.0.0.1"
        When I submit

        Then I see the line "1001" has its call limit to "10"

        When I edit the user "Tom" "Sawyer"
        When I submit

        When I edit the line "1001"
        Then the select field "NAT" is set to "No"
        When I go to the "Advanced" tab
        Then the select field "IP Addressing type" is set to "Static"
        Then the text field "IP address" is set to "10.0.0.1"

    Scenario: Save user and voicemail forms
        Given I am logged in
        Given there is a user "Tom" "Sawyer" with a SIP line "1001"
        Given there is no voicemail "1001"
        When I edit the user "Tom" "Sawyer"
        When I set the select field "Language" to "en_US"
        When I go to the "Voicemail" tab
        When I set the select field "Voice Mail" to "Asterisk"
        When I check the option "Enable voicemail"
        When I set the text field "Voicemail" to ""
        When I submit with errors
        When I go to the "Voicemail" tab
        When I set the text field "Voicemail" to "1001"
        When I submit
        Then user "Tom Sawyer" is displayed in the list
        # Last step needed to avoid eventual problems from bug #3396.
        Given there is no voicemail "1001"

    Scenario: Delete user in group
        Given I am logged in
        Given there is a group "american_dream" number "2000" with no users
        Given there is a user "Tom" "Sawyer" with a SIP line "1001" in group "american_dream"
        When I remove user "Tom" "Sawyer"
        Then I see a group "american_dream" with no users


   Scenario: Add user with function keys
       Given I am logged in
       When I add a user "Tom" "Sawyer" with a function key with type Customized and extension "1234"
       Then I see the user "Tom" "Sawyer" exists
       Then i see user with username "Tom" "Sawyer" has a function key with type Customized and extension "1234"


    Scenario: Delete line from user with voicemail (X-398)
        #Given there is a user "Abraham" "Maharba" with a SIP line "1456", voicemail and CTI profile "client"
        Given I am logged in
        Given there is a user "Abraham" "Maharba" with a SIP line "1456"
        When I edit the user "Abraham" "Maharba"
        When I set the select field "Language" to "en_US"
        When I go to the "Voicemail" tab
        When I set the select field "Voice Mail" to "Asterisk"
        When I check the option "Enable voicemail"
        When I set the text field "Voicemail" to "1456"
        When I submit
        When I edit the user "Abraham" "Maharba"
        When I remove line "1456" from user
        When I submit with errors
        When I remove line "1456" from lines
        Then I get errors
