Feature: User Import

    Scenario: Import user from CSV file
        When I import a list of users:
        | firstname | lastname | linenumber | context |
        | Francis   | Lalannix | 1900       | default |
        | Bob       | Marley   | 1901       | default |
        Then user with name "Francis Lalannix" exists
        Then line with number "1900@default" exists
        Then user with name "Bob Marley" exists
        Then line with number "1901@default" exists

    Scenario: Import user from CSV file enablexfer is enabled by default
        When I import a list of users:
        | firstname | lastname | linenumber | context |
        | Francis   | Lalannix | 1900       | default |
        Then "Francis Lalannix" has enablexfer "enabled"

    Scenario: Import user from CSV file enablexfer field
        When I import a list of users:
        | firstname | lastname | linenumber | context | enable_transfer |
        | Francis   | Lalannix | 1900       | default |               1 |
        | Bob       | Marley   | 1901       | default |               0 |
        | Monsieur  | Patate   | 1902       | default |                 |
        Then "Francis Lalannix" has enablexfer "enabled"
        Then "Bob Marley" has enablexfer "disabled"
        Then "Monsieur Patate" has enablexfer "enabled"

    Scenario: Import user with voicemail from CSV file
        When I import a list of users with voicemail:
        | firstname | lastname | linenumber | context | voicemail |
        | Francis   | Lalannix | 1900       | default | 1900      |
        | Bob       | Marley   | 1901       | default | 1901      |
        Then user with name "Francis Lalannix" exists
        Then line with number "1900@default" exists
        Then voicemail "1900" is displayed in the list
        Then user with name "Bob Marley" exists
        Then line with number "1901@default" exists
        Then voicemail "1901" is displayed in the list

    Scenario: Import user with voicemail and incall from CSV file
        When I import a list of users with incall:
        | firstname | lastname | linenumber | context | incall |
        | Francis   | Lalannix | 1900       | default | 1900   |
        | Bob       | Marley   | 1901       | default | 1901   |
        Then user with name "Francis Lalannix" exists
        Then line with number "1900@default" exists
        Then incall "1900" is displayed in the list
        Then user with name "Bob Marley" exists
        Then line with number "1901@default" exists
        Then incall "1901" is displayed in the list

    Scenario: Import user with full infos from CSV file
        When I import a list of users with incall and voicemail - full:
        | firstname | lastname | linenumber | linesecret | context | voicemail | incall |
        | Francis   | Lalannix | 1900       | toto       | default | 1900      | 1900   |
        | Bob       | Marley   | 1901       |            | default | 1901      | 1901   |
        Then user with name "Francis Lalannix" exists
        Then line with number "1900@default" exists with password "toto"
        Then incall "1900" is displayed in the list
        Then voicemail "1900" is displayed in the list
        Then user with name "Bob Marley" exists
        Then line with number "1901@default" exists
        Then voicemail "1901" is displayed in the list
        Then incall "1901" is displayed in the list
