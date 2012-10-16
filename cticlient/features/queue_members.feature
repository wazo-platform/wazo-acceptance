Feature: Queue Member xlet

    Scenario: No selected queue
        Given there is a group with "2" users
        Given there is a user "Bertrand" "Caron" with CTI profile "agentsup"

        When I start the XiVO Client
        When I log in the XiVO Client as "bertrand", pass "caron"
        Then the Queue members xlet is empty
