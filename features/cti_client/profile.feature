Feature: CTI Profile

    Scenario: Start XiVO Client without any services enabled
        Given there is a profile "noservices" with no services and xlets:
        | xlet     |
        | Features |

        Given there is a user "Abraham" "Washington" with CTI profile "noservices"

        When I start the XiVO Client
        Then I can connect the CTI Client of "Abraham" "Washington"
