Feature: User Import

    Scenario: Import user from CSV file
        Given I am logged in
        When I import a list of users:
        | firstname | lastname | linenumber |
        | Francis   | Lalannix | 1900       |
        | Bob       | Marley   | 1901       |
        Then user "Francis Lalannix" is displayed in the list
        Then line "1900" is displayed in the list
        Then user "Bob Marley" is displayed in the list
        Then line "1901" is displayed in the list

    Scenario: Import user with voicemail from CSV file
        Given I am logged in
        When I import a list of users with voicemail:
        | firstname | lastname | linenumber | voicemail |
        | Francis   | Lalannix | 1900       | 1900      |
        | Bob       | Marley   | 1901       | 1901      |
        Then user "Francis Lalannix" is displayed in the list
        Then line "1900" is displayed in the list
        Then voicemail "1900" is displayed in the list
        Then user "Bob Marley" is displayed in the list
        Then line "1901" is displayed in the list
        Then voicemail "1901" is displayed in the list

    Scenario: Import user with voicemail and incall from CSV file
        Given I am logged in
        When I import a list of users with incall:
        | firstname | lastname | linenumber | incall |
        | Francis   | Lalannix | 1900       | 1900   |
        | Bob       | Marley   | 1901       | 1901   |
        Then user "Francis Lalannix" is displayed in the list
        Then line "1900" is displayed in the list
        Then incall "1900" is displayed in the list
        Then user "Bob Marley" is displayed in the list
        Then line "1901" is displayed in the list
        Then incall "1901" is displayed in the list

    Scenario: Import user with full infos from CSV file
        Given I am logged in
        When I import a list of users with incall and voicemail - full:
        | firstname | lastname | linenumber | voicemail | incall |
        | Francis   | Lalannix | 1900       | 1900      | 1900   |
        | Bob       | Marley   | 1901       | 1901      | 1901   |
        Then user "Francis Lalannix" is displayed in the list
        Then line "1900" is displayed in the list
        Then incall "1900" is displayed in the list
        Then voicemail "1900" is displayed in the list
        Then user "Bob Marley" is displayed in the list
        Then line "1901" is displayed in the list
        Then voicemail "1901" is displayed in the list
        Then incall "1901" is displayed in the list
