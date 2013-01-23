Feature: Switchboard

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
