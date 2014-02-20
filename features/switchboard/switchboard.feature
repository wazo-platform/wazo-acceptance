Feature: Switchboard

    Scenario: Search transfer destination in phonebook
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd |
         | Switch    | Board    | Switchboard | switch    | board      |
        Given the switchboard is configured for internal directory lookup
        Given there are entries in the phonebook:
         | first name | last name |      phone |     mobile |
         | Uncle      | Bob       | 8197644444 | 8197621114 |
        When I start the XiVO Client
        When I log in the XiVO Client as "switch", pass "board"
        When I search a transfer destination "uncle bob"
        Then I see transfer destinations:
         | Name      | Number     |
         | Uncle Bob | 8197644444 |
         | Uncle Bob | 8197621114 |

    Scenario: Search mobile number of transfer destination
        Given there are users with infos:
         | firstname | lastname   | mobile_number | cti_profile | cti_login | cti_passwd |
         | Felix     | Shrödinger |    5555555555 | Switchboard | felix     | shrodinger |
        When I start the XiVO Client
        When I log in the XiVO Client as "felix", pass "shrodinger"
        When I search a transfer destination "felix"
        Then I see transfer destinations:
         | Name             | Number     |
         | Felix Shrödinger | 5555555555 |
        When I modify the mobile number of user "Felix" "Shrödinger" to "666"
        Then I see transfer destinations:
         | Name             | Number |
         | Felix Shrödinger | 666    |
        When I remove the mobile number of user "Felix" "Shrödinger"
        Then I see no transfer destinations

    Scenario: Delete user while searching  mobile number transfer destination
        Given there are users with infos:
         | firstname | lastname | mobile_number | cti_profile | cti_login | cti_passwd |
         | Germaine  | Tremblay |          1234 | Switchboard | germaine  | tremblay   |
        When I start the XiVO Client
        When I log in the XiVO Client as "germaine", pass "tremblay"
        When I search a transfer destination "germaine tremblay"
        Then I see transfer destinations:
         | Name              | Number |
         | Germaine Tremblay | 1234   |
        When I remove user "Germaine" "Tremblay"
        Then I see no transfer destinations

    Scenario: Search transfer destination in ldap server
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd |
         | Switch    | Board    | Switchboard | switch    | board      |
        Given the switchboard is configured for ldap lookup
        Given there are entries in the ldap server:
         | first name | last name |      phone |
         | Robert     | Lébleux   | 0133123456 |
        When I start the XiVO Client
        When I log in the XiVO Client as "switch", pass "board"
        When I search a transfer destination "léb"
        Then I see transfer destinations:
         | Name           | Number     |
         | Robert Lébleux | 0133123456 |

    Scenario: Search transfer location in ldap server
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd | mobile_number |
         | Switch    | Board    | Switchboard | switch    | board      |               |
         | Germaine  | Tremblay | Client      | germaine  | tremblay   |    4186566666 |
        Given the switchboard is configured for ldap lookup with location
        Given there are entries in the ldap server:
         | first name | last name |      phone | location |
         | Robert     | Lébleux   | 0133123456 | USA      |
        When I start the XiVO Client
        When I log in the XiVO Client as "switch", pass "board"
        When I search a transfer destination "usa"
        Then I see transfer destinations:
         | Name           | Number     | Location |
         | Robert Lébleux | 0133123456 | USA      |
        When I search a transfer destination "ger"
        Then I see transfer destinations:
         | Name              |     Number | Location |
         | Germaine Tremblay | 4186566666 |          |

    Scenario: Search transfer destination with 2 columns from ldap
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd | mobile_number |
         | Switch    | Board    | Switchboard | switch    | board      |               |
        Given the switchboard is configured for ldap lookup with location and department
        Given there are entries in the ldap server:
         | first name | last name |      phone | location | department |
         | Robert     | Lébleux   | 0133123456 | USA      | Sales      |
        When I start the XiVO Client
        When I log in the XiVO Client as "switch", pass "board"
        When I search a transfer destination "sale"
        Then I see transfer destinations:
         | Name           | Number     | Location | Department |
         | Robert Lébleux | 0133123456 | USA      | Sales      |
        When I search a transfer destination "usa"
        Then I see transfer destinations:
         | Name           | Number     | Location | Department |
         | Robert Lébleux | 0133123456 | USA      | Sales      |

    Scenario: Search transfer destination both in internal directory and ldap
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd | number | context |
         | Switch    | Board    | Switchboard | switch    | board      |        |         |
         | Robert    | Lébleux  | Client      | robert    | lebleux    | 1423   | default |
        Given the switchboard is configured for ldap lookup with location
        Given there are entries in the ldap server:
         | first name | last name | phone | location |
         | Robert     | Lébleux   | 1423  | USA      |
        When I start the XiVO Client
        When I log in the XiVO Client as "switch", pass "board"
        When I search a transfer destination "robe"
        Then I see transfer destinations:
         | Name           | Number | Location |
         | Robert Lébleux | 1423   | USA      |

    Scenario: Search transfer destination in ldap with 2 numbers
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd | number | context | mobile_number |
         | Switch    | Board    | Switchboard | switch    | board      |        |         |               |
         | Robert    | Lébleux  | Client      | robert    | lebleux    | 1423   | default | 5551234567    |
        Given the switchboard is configured for ldap lookup with location
        Given there are entries in the ldap server:
         | first name | last name | phone | location |
         | Robert     | Lébleux   | 1423  | USA      |
        When I start the XiVO Client
        When I log in the XiVO Client as "switch", pass "board"
        When I search a transfer destination "robe"
        Then I see transfer destinations:
         | Name           | Number     | Location |
         | Robert Lébleux | 1423       | USA      |
         | Robert Lébleux | 5551234567 |          |

    Scenario: Search transfer destination with an arbitrary number
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd |
         | Switch    | Board    | Switchboard | switch    | board      |
        When I start the XiVO Client
        When I log in the XiVO Client as "switch", pass "board"
        When I search a transfer destination "6543"
        Then I see transfer destinations:
         | Name | Number |
         |      | 6543   |

    Scenario: Answer second incoming call
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd | number | context | protocol | agent_number |
         | Switch    | Board    | Switchboard | switch    | board      |   1631 | default | sip      |         1631 |
         | Alice     | A        |             |           |            |   1632 | default | sip      |              |
         | Bob       | B        |             |           |            |   1633 | default | sip      |              |
        Given there is a switchboard configured as:
         | incalls queue name | hold calls queue name | incalls queue number | incalls queue context | hold calls queue number | hold calls queue context | agents       |
         | __switchboard      | __switchboard_hold    |                 3009 | default               |                    3010 | default                  | 1631@default |
        When I start the XiVO Client
        When I log in the XiVO Client as "switch", pass "board", logged agent
        When "Alice A" calls "3009"
        When "Bob B" calls "3009"
        When the switchboard "Switch Board" answers the call from "Bob B" number "1633"
        Then the switchboard is talking to "Bob B" number "1633"
