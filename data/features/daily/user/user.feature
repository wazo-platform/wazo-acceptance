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
