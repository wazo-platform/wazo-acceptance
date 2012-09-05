Feature: User

    Scenario: Enable XiVO Client
        Given there is a user "Charles" "Magne"
        When I edit the user "Charles" "Magne"
        When I uncheck the option "Enable XiVO Client"
        When I submit
        When I start the XiVO Client
        Then I can't log in the XiVO Client as "charles", pass "magne"

        When I edit the user "Charles" "Magne"
        When I check the option "Enable XiVO Client"
        When I set the text field "Login" to ""
        When I set the text field "Password" to ""
        When I submit with errors
        When I set the text field "Login" to "charles"
        When I set the text field "Password" to "magne"
        When I submit
        Then I log in the XiVO Client as "charles", pass "magne"
