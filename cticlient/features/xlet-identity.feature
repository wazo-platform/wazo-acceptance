Feature: Xlet identity

    Scenario: Display identity infos
        Given I am logged in

        Given there is a context interval for SIP line "151"
        Given there is no user "Yoda" "Kenobi"
        Given there is no SIP line "151"
        Given there is a user "Yoda" "Kenobi" with a SIP line "151" and CTI profile "Client"

        Given I go to the "Resolver" configuration page
        Given I read the field "Hostname"

        When I start the XiVO Client
        When I log in the XiVO Client as "yoda", pass "kenobi"

        Then the Xlet identity shows name as "Yoda" "Kenobi"
        Then the Xlet identity shows server name as field "Hostname"
        Then the Xlet identity shows phone number as "151"

    Scenario: Display voicemail icon and number
        Given I am logged in

        Given there is no user "Bail" "Tarkin"
        Given there is no SIP line "152"
        Given there is a user "Bail" "Tarkin" with a SIP line "152", voicemail and CTI profile "client"

        When I start the XiVO Client
        When I log in the XiVO Client as "bail", pass "tarkin"
        Then the Xlet identity shows a voicemail "152"

    Scenario: Display agent icon and number
        Given I am logged in

        Given there is no user "Darth" "Chewbacca"
        Given there is no agent number "153"
        Given there is a user "Darth" "Chewbacca" with an agent "153" and CTI profile "Client"

        When I start the XiVO Client
        When I log in the XiVO Client as "darth", pass "chewbacca", unlogged agent
        Then the Xlet identity shows an agent "153"

        When I log out of the XiVO Client
        When I delete agent number "153"

        When I log in the XiVO Client as "darth", pass "chewbacca"
        Then the Xlet identity does not show any agent
