Feature: User

    Scenario: Add a user with first name and last name and remove it
        Given there is no user "Bill" "Bush"
        When I create a user with infos:
        | firstname | lastname |
        | Bill      | Bush     |
        When I search for user "Bill" "Bush"
        Then user "Bill Bush" is displayed in the list
        When I remove user "Bill" "Bush"
        When I search for user "Bill" "Bush"
        Then user "Bill Bush" is not displayed in the list

    Scenario: Add a user in a group
        Given there are users with infos:
        | firstname | lastname | number | context | group_name  |
        | Bob       | Marley   |   1101 | default | rastafarien |
        Given there is no user "Bob" "Dylan"
        When I rename "Bob" "Marley" to "Bob" "Dylan"
        Then I should be at the user list page
        Then "Bob" "Dylan" is in group "rastafarien"

    Scenario: Add user with function keys
        When I add a user "Tom" "Sawyer" with a function key with type Customized and extension "1234"
        Then I see the user "Tom" "Sawyer" exists
        Then i see user with username "Tom" "Sawyer" has a function key with type Customized and extension "1234"

    Scenario: Add user with SIP line and remove it
        Given there is no user "Bill" "Bush"
        Given I have no extension with exten "1632@default"
        When I create a user with infos:
        | firstname | lastname | protocol | number | context |
        | Bill      | Bush     | SIP      |  1632  | default |
        Then I see a user with infos:
        | fullname  | number | protocol | context |
        | Bill Bush |   1632 | sip      | default |
        When I remove user "Bill" "Bush"
        Then user "Bill Bush" is not displayed in the list

    Scenario: Add user with SCCP line and remove it
        Given there is no user "Bill" "Bush"
        Given I have no extension with exten "1632@default"
        When I create a user with infos:
        | firstname | lastname | protocol | number | context |
        | Bill      | Bush     | SCCP     |  1632  | default |
        Then I see a user with infos:
        | fullname  | number | provisioning_code | protocol | context |
        | Bill Bush |   1632 |                 0 | sccp     | default |
        When I remove user "Bill" "Bush"
        Then user "Bill Bush" is not displayed in the list

    Scenario: Add user with SIP line and device and remove it
        Given the plugin "xivo-aastra-3.2.2-SP3" is installed
        Given there are no devices with mac "00:de:ad:be:ef:00"
        Given I have no extension with exten "1632@default"
        Given I have the following devices:
        | mac               | plugin                | model | ip          | vendor |
        | 00:de:ad:be:ef:00 | xivo-aastra-3.2.2-SP3 | 6731i | 10.39.5.104 | Aastra |
        When I search device ""
        Given there is no user "Bill" "Bush"
        When I create a user with infos:
        | firstname | lastname | protocol | number | context | device            |
        | Bill      | Bush     | SIP      |   1632 | default | 00:de:ad:be:ef:00 |
        Then I see a user with infos:
        | fullname  | number | protocol | context |
        | Bill Bush |   1632 | sip      | default |
        Then I see a line with infos:
        | device | number | protocol | user      |
        | True   |   1632 | sip      | Bill Bush |
        Then I see devices with infos:
        | mac               | configured |
        | 00:de:ad:be:ef:00 | True       |
        When I remove user "Bill" "Bush"
        Then user "Bill Bush" is not displayed in the list
        Then I see devices with infos:
        | mac               | configured |
        | 00:de:ad:be:ef:00 | False      |

    Scenario: Create a user with a device that only has a MAC
      Given I have the following devices:
          | mac               |
          | dd:11:22:33:44:55 |
      Given there is no user "Abarai" "Renji"
      Given I have no extension with exten "1632@default"
      When I create a user with infos:
          | firstname | lastname | protocol | number | context | device            |
          | Abarai    | Renji    | SIP      | 1677   | default | dd:11:22:33:44:55 |
      Then I see a user with infos:
          | fullname     | protocol | number | context |
          | Abarai Renji | sip      | 1677   | default |

    Scenario: Find a user by line number
        Given there are users with infos:
        | firstname | lastname | number | context |
        | Bob       | Marley   |   1101 | default |
        | Abraham   | Maharba  |   1456 | default |
        When I search for user with number "1456"
        Then user "Abraham Maharba" is displayed in the list

    Scenario: Update a user
        Given there is no user "Bill" "Bush"
        When I create a user with infos:
        | firstname | lastname |
        | Bill      | Bush     |
        When I search for user "Bill" "Bush"
        Then user "Bill Bush" is displayed in the list
        When I rename "Bill" "Bush" to "George" "Orwell"
        When I search for user "George" "Orwell"
        Then user "George Orwell" is displayed in the list

    Scenario: Update the group's channel type of a user
        Given there are users with infos:
        | firstname | lastname | number | context | group_name
        | Bob       | Marley   |   1101 | default | rastafarien
        Then the channel type of group "rastafarien" of user "Bob Marley" is "default"
        When I modify the channel type of group "rastafarien" of user "Bob Marley" to "Local"
        Then the channel type of group "rastafarien" of user "Bob Marley" is "Local"

    Scenario: Update a user with SIP line
    # The problem is that saving the user form may erase values previously
    # set in the line form (bug #2918)
        Given there are users with infos:
        | firstname | lastname | number | context |
        | Tom       | Sawyer   |   1405 | default |
        Given I set the following options in line "1405":
        | NAT | IP addressing type | IP address |
        | No  | Static             | 10.0.0.1   |
        Then the line "1405" has the following line options:
        | Call limit |
        |         10 |
        When I edit the user "Tom" "Sawyer" without changing anything
        Then the line "1405" has the following line options:
        | NAT | IP addressing type | IP address | Call limit |
        | No  | Static             |   10.0.0.1 |         10 |

    Scenario: Add a voicemail to a user without a line
        Given there are users with infos:
        | firstname | lastname |
        | Indiana   | Jones    |
        Given there is no voicemail with number "1405" and context "default"
        When I add a voicemail "1405" to the user "Indiana" "Jones" with errors
        Then I see errors

    Scenario: Add a voicemail to an existing user
        Given there are users with infos:
         | firstname | lastname | number | context |
         | Tom       | Sawyer   |   1405 | default |
        Given there is no voicemail with number "1405" and context "default"
        When I add a voicemail "" to the user "Tom" "Sawyer" with errors
        Then I see errors
        When I add a voicemail "1405" to the user "Tom" "Sawyer"
        Then voicemail "1405" is displayed in the list

    Scenario: Delete user 
        Given there are users with infos:
         | firstname | lastname | number | context |
         | Tom       | Sawyer   |   1405 | default |
        When I remove user "Tom" "Sawyer"
        Then there is no data about this user remaining in the database.

    Scenario: Delete user in group
        Given there are users with infos:
        | firstname | lastname | number | context | group_name     |
        | Tom       | Sawyer   |   1405 | default | american_dream |
        When I remove user "Tom" "Sawyer"
        Then I see a group "american_dream" with no users

    Scenario: Delete user in queue
        Given there are users with infos:
         | firstname | lastname | number | context |
         | Tom       | Sawyer   |   1405 | default |
        Given there are queues with infos:
            |      name      |  display name  | number | context | users_number |
            | americandream  | American Dream |  3203  | default |    1405      |
        When I remove user "Tom" "Sawyer"
        Then there is no data about this user remaining in the database.

    Scenario: Delete line from user with voicemail
        Given there are users with infos:
         | firstname | lastname | number | context | language | voicemail_name | voicemail_number |
         | Abraham   | Maharba  |   1456 | default | en_US    | 1456           | 1456             |
        When I remove line from user "Abraham" "Maharba" with errors
        Then I see errors
        When I remove line "1456" from lines then I see errors
