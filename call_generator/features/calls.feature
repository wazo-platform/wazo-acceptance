Feature: Callgen

    Scenario: Call to inexistant extension
        Given there is a user "User" "100" with extension "1100@default"
        When I call extension "1190@default"
        When I wait 5 seconds for the calls processing
        Then I see rejected call to extension "1100@default" in asterisk log

