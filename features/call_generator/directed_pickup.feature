Feature: Directed pickup

    Scenario: Pickup a call
        Given there are no calls running
        Given there are users with infos:
         | firstname | lastname | number | context |
         | User      | 100      |   1100 | default |
         | User      | 101      |   1101 | default |
         | User      | 102      |   1102 | default |
        Given I wait 5 seconds for the dialplan to be reloaded
        When I register extension "1101@default"
        When I wait call then I do not answer
        When line "1100@default" calls number "1101" then wait
        When line "1102@default" pick up call at number "1101"
        Then the directed pickup is successful

    Scenario: Pickup a call coming from a group
        Given there are no calls running
        Given there are users with infos:
         | firstname | lastname | number | context |
         | User      | 101      |   1101 | default |
         | User      | 102      |   1102 | default |
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
        Given there are users with infos:
         | firstname | lastname | number | context |
         | User      | 143      |   1143 | default |
         | User      | 148      |   1148 | default |
        Given there is an incall "1143" in context "from-extern" to the "user" "User 143"
        Given I wait 5 seconds for the dialplan to be reloaded
        When I register extension "1143@default"
        When I wait call then I do not answer
        When there is 1 calls to extension "1143@from-extern" on trunk "to_incall" and wait
        When line "1148@default" pick up call at number "1143"
        Then the directed pickup is successful
