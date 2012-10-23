Feature: Xlet identity

    Scenario: Display identity infos
        Given there is no user "Yoda" "Kenobi"
        Given there is no SIP line "1151"
        Given there is a user "Yoda" "Kenobi" with extension "1151@default" and CTI profile "Client"

        Given I go to the "Resolver" configuration page
        Given I read the field "Hostname"

        When I start the XiVO Client
        When I log in the XiVO Client as "yoda", pass "kenobi"

        Then the Xlet identity shows name as "Yoda" "Kenobi"
        Then the Xlet identity shows server name as field "Hostname"
        Then the Xlet identity shows phone number as "1151"

    Scenario: Display voicemail icon and number
        Given there is no user "Bail" "Tarkin"
        Given there is no SIP line "1152"
        Given there is a user "Bail" "Tarkin" with extension "1152@default", voicemail and CTI profile "Client"

        When I start the XiVO Client
        When I log in the XiVO Client as "bail", pass "tarkin"
        Then the Xlet identity shows a voicemail "1152"

    Scenario: Display agent icon and number
        Given there is no user "Darth" "Chewbacca"
        Given there is no agent with number "1153"
        Given there is a user "Darth" "Chewbacca" with an agent "1153@default" and CTI profile "Client"

        When I start the XiVO Client
        When I log in the XiVO Client as "darth", pass "chewbacca", unlogged agent
        Then the Xlet identity shows an agent "1153"

        When I log out of the XiVO Client
        When I delete agent number "1153"

        When I log in the XiVO Client as "darth", pass "chewbacca"
        Then the Xlet identity does not show any agent
