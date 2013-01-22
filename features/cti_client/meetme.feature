Feature: Meetme

    Scenario: All conference rooms show up in CTI client
        Given there is a user "Lord" "Sanderson" with extension "1042@default" and CTI profile "Client"
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
        Given there is a user "Lord" "Sanderson" with extension "1042@default" and CTI profile "Client"
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
            | name  | number | pin code |
            | room1 | 4001   | Yes      |
            | room2 | 4002   | No       |

