Feature: CTI Profile

    Scenario: Start XiVO Client without any services enabled
        Given I am logged in
        Given there is no profile "noservices"
        Given I add a profile
        Given I set the text field "Name" to "noservices"
        Given I set the text field "Display name" to "noservices"
        Given I remove all services
        Given I go to the "Xlets" tab
        Given I add a XLet "Features"
        Given I submit

        Given there is no user "Abraham" "Washington"
        Given I add a user
        Given I set the text field "First name" to "Abraham"
        Given I set the text field "Last name" to "Washington"
        Given I enable the XiVO Client as "abraham" pass "washington" profile "noservices"
        Given I submit

        When I start the XiVO Client
        Then I log in the XiVO Client as "abraham", pass "washington"
