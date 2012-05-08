Feature: User Import

    Scenario: Import user from CSV file
        Given I am logged in
        Given there is no voicemail "1000"
        Given there is no line "1000"
        Given there is no user "Francis Lalannix"
        When I import a user "Francis" "Lalannix" with a SIP line "1000"
        Then user "Francis Lalannix" is displayed in the list

    Scenario: Import user with voicemail from CSV file
        Given I am logged in
        Given there is no voicemail "1000"
        Given there is no line "1000"
        Given there is no user "Francis Lalannix"
        When I import a user "Francis" "Lalannix" with a SIP line "1000" and voicemail
        Then user "Francis Lalannix" is displayed in the list
        Then line "1000" is displayed in the list
        Then voicemail "1000" is displayed in the list

    Scenario: Import user with voicemail and incall from CSV file
        Given I am logged in
        Given there is no voicemail "1000"
        Given there is no line "1000"
        Given there is no user "Francis Lalannix"
        Given there is no incall "2000"
        When I import a user "Francis" "Lalannix" with a SIP line "1000" and incall "2000"
        Then user "Francis Lalannix" is displayed in the list
        Then line "1000" is displayed in the list
        Then incall "2000" is displayed in the list

    Scenario: Import user with full infos from CSV file
        Given I am logged in
        Given there is no voicemail "1000"
        Given there is no line "1000"
        Given there is no user "Francis Lalannix"
        Given there is no incall "2000"
        When I import a user "Francis" "Lalannix" with a SIP line "1000" and incall "2000" and voicemail - full
        Then user "Francis Lalannix" is displayed in the list
        Then line "1000" is displayed in the list
        Then voicemail "1000" is displayed in the list
        Then incall "2000" is displayed in the list
