Feature: User

    Scenario: User ACL generation
        Given there are users with infos:
        | firstname | lastname | number | context | agent_number | cti_login | cti_passwd | cti_profile |
        | Bob       | Marley   |   1101 | default | 1101         | bob       | secret     | Client      |
        When I create a token with infos:
        | username | password | backend   |
        | bob      | secret   | wazo_user |
        Then the token has the following ACLs:
        | ACL                               |
        | agentd.agents.by-number.1101.read |

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

    Scenario: Bus notification on user deleted
        Given there are users with infos:
        | firstname | lastname |
        | Walt      | Longmire |
        Given I listen on the bus for messages:
        | queue        | routing_key         |
        | deleted_user | config.user.deleted |
        When I remove user "Walt" "Longmire"
        Then I receive a "user_deleted" on the queue "deleted_user" with data:
        | id  | uuid |
        | ANY | ANY  |

    Scenario: Add a user in a group
        Given there are users with infos:
        | firstname | lastname | number | context | group_name  |
        | Bob       | Marley   |   1101 | default | rastafarien |
        Given there is no user "Bob" "Dylan"
        When I rename "Bob" "Marley" to "Bob" "Dylan"
        Then I should be at the user list page
        Then "Bob" "Dylan" is in group "rastafarien"

    @skip_old_webi_step
    Scenario: Add user with SIP line and remove it
        Given there is no user "Bill" "Bush"
        Given I have no extension with exten "1632@default"
        When I create a user with infos:
        | firstname | lastname | protocol | number | context |
        | Bill      | Bush     | SIP      |  1632  | Default |
        Then I see a user with infos:
        | fullname  | number | protocol |
        | Bill Bush |   1632 | sip      |
        When I remove user "Bill" "Bush"
        Then user "Bill Bush" is not displayed in the list

    @skip_old_webi_step
    Scenario: Add user with SCCP line and remove it
        Given there is no user "Bill" "Bush"
        Given I have no extension with exten "1632@default"
        When I create a user with infos:
        | firstname | lastname | protocol | number | context |
        | Bill      | Bush     | SCCP     |  1632  | Default |
        Then I see a user with infos:
        | fullname  | number | protocol |
        | Bill Bush |   1632 | sccp     |
        When I remove user "Bill" "Bush"
        Then user "Bill Bush" is not displayed in the list

    @skip_old_webi_step
    Scenario: Add user with SIP line and device and remove it
        Given the plugin "xivo-aastra-3.3.1-SP4" is installed
        Given there are no devices with mac "00:de:ad:be:ef:00"
        Given I have no extension with exten "1632@default"
        Given I have the following devices:
        | mac               | plugin                | model | ip          | vendor |
        | 00:de:ad:be:ef:00 | xivo-aastra-3.3.1-SP4 | 6731i | 10.39.5.104 | Aastra |
        When I search device ""
        Given there is no user "Bill" "Bush"
        When I create a user with infos:
        | firstname | lastname | protocol | number | context | device            |
        | Bill      | Bush     | SIP      |   1632 | Default | 00:de:ad:be:ef:00 |
        Then I see a user with infos:
        | fullname  | number | protocol |
        | Bill Bush |   1632 | sip      |
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

    @skip_old_webi_step
    Scenario: Create a user with a device that only has a MAC
      Given I have the following devices:
          | mac               |
          | dd:11:22:33:44:55 |
      Given there is no user "Abarai" "Renji"
      Given I have no extension with exten "1677@default"
      When I create a user with infos:
          | firstname | lastname | protocol | number | context | device            |
          | Abarai    | Renji    | SIP      | 1677   | Default | dd:11:22:33:44:55 |
      Then I see a user with infos:
          | fullname     | protocol | number |
          | Abarai Renji | sip      | 1677   |

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
        | firstname | lastname | number | context | group_name  |
        | Bob       | Marley   |   1101 | default | rastafarien |
        Then the channel type of group "rastafarien" of user "Bob Marley" is "default"
        When I modify the channel type of group "rastafarien" of user "Bob Marley" to "Local"
        Then the channel type of group "rastafarien" of user "Bob Marley" is "Local"
        Then the "rastafarien" section of "queues.conf" contains the options:
        | name   | value                |
        | member | Local/1101@default,0 |

    @skip_old_webi_step
    Scenario: Update a user with SIP line
    # The problem is that saving the user form may erase values previously
    # set in the line form (bug #2918)
        Given there are users with infos:
          | firstname | lastname | number | context |
          | Tom       | Sawyer   |   1405 | default |
        Given I set the following options in line "1405@default":
          | NAT |
          | No  |
        Then the line "1405" has the following line options:
          | Call limit |
          |         10 |
        When I edit the user "Tom" "Sawyer" without changing anything
        Then the line "1405" has the following line options:
          | NAT | Call limit |
          | No  |         10 |

    @skip_old_webi_step
    Scenario: Delete user
        Given there are users with infos:
          | firstname | lastname | number | context |
          | Tom       | Sawyer   |   1405 | default |
        When I remove user "Tom" "Sawyer"
        Then there is no data about this user remaining in the database.

    @skip_old_webi_step
    Scenario: Delete user in group
        Given there are users with infos:
          | firstname | lastname | number | context | group_name     |
          | Tom       | Sawyer   |   1405 | default | american_dream |
        When I remove user "Tom" "Sawyer"
        Then I see a group "american_dream" with no users

    @skip_old_webi_step
    Scenario: Delete user in queue
        Given there are users with infos:
          | firstname | lastname | number | context |
          | Tom       | Sawyer   |   1405 | default |
        Given there are queues with infos:
          |      name      |  display name  | number | context | users_number |
          | americandream  | American Dream |  3203  | default |    1405      |
        When I remove user "Tom" "Sawyer"
        Then there is no data about this user remaining in the database.

    @skip_old_webi_step
    Scenario: Update user's extension to existing queue's extension
        Given there are contexts with infos:
          | type   | name      | range_start | range_end |
          | user   | samerange | 1000        | 1999      |
          | queue  | samerange | 1000        | 1999      |
        Given there are users with infos:
          | firstname | lastname | number | context   |
          | Fab       | Lab      | 1001   | samerange |
        Given there are queues with infos:
          | name          | display name   | number | context   |
          | americandream | American Dream | 1002   | samerange |
        Given I have no extension with exten "1003@samerange"
        When I modify the extension of user "Fab" "Lab" to "1002" with errors
        When I modify the extension of user "Fab" "Lab" to "1003"
        When I edit the queue "americandream"
        Then I see no errors
