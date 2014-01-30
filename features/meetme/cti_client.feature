Feature: Meetme

    Scenario: All conference rooms show up in CTI client
        Given I have no extension with exten "1042@default"
        Given there are users with infos:
         | firstname | lastname  | number | context | cti_profile |
         | Lord      | Sanderson | 1042   | default | Client      |
        Given there are no conference rooms
        When I add the following conference rooms:
            | name  | number |
            | room1 | 4001   |
            | room2 | 4002   |
            | room3 | 4003   |
        When I start the XiVO Client
        When I log in the XiVO Client as "lord", pass "sanderson"
        Then the following conference rooms appear in the conference room xlet:
            | name  | number |
            | room1 | 4001   |
            | room2 | 4002   |
            | room3 | 4003   |

    Scenario: PIN Code for a conference room shows up in the CTI client
        Given I have no extension with exten "1042@default"
        Given there are users with infos:
         | firstname | lastname  | number | context | cti_profile |
         | Lord      | Sanderson | 1042   | default | Client      |
        Given there are no conference rooms
        When I add the following conference rooms:
            | name  | number |
            | room1 | 4001   |
            | room2 | 4002   |
        When I update the following conference rooms:
            | name  | number | pin code |
            | room1 | 4001   | 1234     |
        When I start the XiVO Client
        When I log in the XiVO Client as "lord", pass "sanderson"
        Then the following conference rooms appear in the conference room xlet:
            | name  | number | pin_required |
            | room1 | 4001   | Yes          |
            | room2 | 4002   | No           |

