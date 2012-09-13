Feature: Callgen

    Scenario: Call to inexistant extension
        Given there is a user "User" "100" with extension "1100@default"
        When I call extension "1190@default"
        When I wait 5 seconds for the calls processing
        Then I see rejected call to extension "1100@default" in asterisk log

    Scenario: Call to existant extension with answer
        Given there is a user "User" "100" with extension "1100@default"
        Given there is a user "User" "101" with extension "1101@default"
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I register extension "1101"
        Given I wait call then i answer and wait
        Given there is 1 calls to extension "1101@default" then i hang up after "3s"
        Given I wait 5 seconds for the calls processing
        Then i see the called extension "1101" in call logs page
