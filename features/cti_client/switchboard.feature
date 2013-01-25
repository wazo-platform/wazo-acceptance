Feature: Switchboard

    Scenario: Search transfer destination in phonebook
        Given there are users with infos:
        | firstname | lastname | cti_profile | cti_login | cti_passwd |
        | Switch    | Board    | Switchboard | switch    | board      |
        Given there are entries in the phonebook:
        | first name | last name | phone |
        | Uncle      | Bob       |   1234 |
        When I start the XiVO Client
        When I log in the XiVO Client as "switch", pass "board"
        When I search a transfer destination "uncle bob"
        Then I see transfer destinations:
        | display_name | phone |
        | Uncle Bob    |  1234 |

    Scenario: Search mobile number of transfer destination
        Given there are users with infos:
        | firstname | lastname   | mobile_number | cti_profile | cti_login | cti_passwd |
        | Felix     | Shrödinger |    5555555555 | Switchboard | felix     | shrodinger |
        When I start the XiVO Client
        When I log in the XiVO Client as "felix", pass "shrodinger"
        When I search a transfer destination "felix"
        Then I see transfer destinations:
        | display_name     |      phone |
        | Felix Shrödinger | 5555555555 |
        When I modify the mobile number of user "Felix" "Shrödinger" to "666"
        Then I see transfer destinations:
        | display_name     | phone |
        | Felix Shrödinger |   666 |
        When I remove the mobile number of user "Felix" "Shrödinger"
        Then I see no transfer destinations
