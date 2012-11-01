Feature: Call daily-script

    Scenario: Call to existant extension with answer
        Given there are no calls running
        Given there is a user "User" "100" with extension "1100@default"
        Given there is a user "User" "101" with extension "1101@default"
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I register extension "1101"
        Given I wait call then I answer and wait
        Given there is 1 calls to extension "1101@default" then I hang up after "3s"
        Given I wait 5 seconds for the calls processing
        Then I see the called extension "1101" by "1100" in call logs page
