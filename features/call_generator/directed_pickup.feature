Feature: Directed pickup

    Scenario: Pickup a call
        Given there are no calls running
        Given there is a user "User" "100" with extension "1100@default"
        Given there is a user "User" "101" with extension "1101@default"
        Given there is a user "User" "102" with extension "1102@default"
        Given I wait 5 seconds for the dialplan to be reloaded
        When I register extension "1101@default"
        When I wait call then I do not answer
        When line "1100@default" calls number "1101" then wait
        When line "1102@default" pick up call at number "1101"
        Then the directed pickup is successful

    Scenario: Pickup a call coming from a group
        Given there are no calls running
        Given there is a user "User" "101" with extension "1101@default"
        Given there is a user "User" "102" with extension "1102@default"
        Given there is a group "group1" with extension "2001@default" and users:
          | firstname | lastname |
          | User      | 101      |
        Given I wait 5 seconds for the dialplan to be reloaded
        When I register extension "1101@default"
        When I wait call then I do not answer
        When there is 1 calls to extension "2001@default" and wait
        When line "1102@default" pick up call at number "1101"
        Then the directed pickup is successful

    Scenario: Pickup a call coming from an incoming call
        Given there are no calls running
        Given there is a user "User" "101" with extension "1101@default"
        Given there is a user "User" "102" with extension "1102@default"
        Given there is an incall "1101" in context "from-extern" to the "user" "User 101"
        Given I wait 5 seconds for the dialplan to be reloaded
        When I register extension "1101@default"
        When I wait call then I do not answer
        When there is 1 calls to extension "1101@from-extern" on trunk "to_incall" and wait
        When line "1102@default" pick up call at number "1101"
        Then the directed pickup is successful
