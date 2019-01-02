Feature: Switchboard search

    Scenario: Search transfer destination in phonebook
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd |
         | Switch    | Board    | Switchboard | switch    | board      |
        Given the switchboard is configured for internal directory lookup
        Given there are entries in the phonebook "wazo" of entity "xivoentity":
         | first name | last name |      phone |     mobile |
         | Uncle      | Bob       | 8197644444 | 8197621114 |
        When I start the XiVO Client
        When I log in the XiVO Client as "switch", pass "board"
        When I search a transfer destination "uncle bob"
        Then I see transfer destinations:
         | Name      | Number     |
         | Uncle Bob | 8197644444 |
         | Uncle Bob | 8197621114 |

    Scenario: Search transfer destination with different name and same number
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd |
         | Switch    | Board    | Switchboard | switch    | board      |
        Given the switchboard is configured for internal directory lookup
        Given there are entries in the phonebook "wazo" of entity "xivoentity":
         | first name | last name |      phone |     mobile |
         | Alice      | Wonder    |        555 |          1 |
         | Bob        | Gainey    |        555 |          2 |
        When I start the XiVO Client
        When I log in the XiVO Client as "switch", pass "board"
        When I search a transfer destination "Alice"
        Then I see transfer destinations:
         | Name         | Number     |
         | Alice Wonder | 555        |
        When I search a transfer destination "Bob"
        Then I see transfer destinations:
         | Name         | Number     |
         | Bob Gainey   | 555        |
        When I search a transfer destination "555"
        Then I see transfer destinations:
         | Name         | Number     |
         | Alice Wonder | 555        |
         | Bob Gainey   | 555        |

    @skip_old_cti_step
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

    Scenario: Delete user while searching mobile number transfer destination
        Given there are users with infos:
         | firstname | lastname | mobile_number | cti_profile | cti_login | cti_passwd |
         | Alphonse  | Tremblay |               | Switchboard | alphonse  | tremblay   |
         | Germaine  | Tremblay |          1234 |             |           |            |
        When I start the XiVO Client
        When I log in the XiVO Client as "alphonse", pass "tremblay"
        When I search a transfer destination "germaine tremblay"
        Then I see transfer destinations:
         | Name              | Number |
         | Germaine Tremblay | 1234   |
        When I remove user "Germaine" "Tremblay"
        Then I see no transfer destinations

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
