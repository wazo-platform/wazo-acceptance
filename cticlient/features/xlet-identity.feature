Feature: Xlet identity

    Scenario: Display identity infos
        Given I am logged in

        Given there is a context interval for SIP line "151"
        Given there is no user "Yoda" "Kenobi"
        Given there is no SIP line "151"
        Given I add a user
        Given I set the text field "First name" to "Yoda"
        Given I set the text field "Last name" to "Kenobi"
        Given I enable the XiVO Client as "yoda" pass "kenobi" profile "Client"
        Given I add a SIP line "151" to the user
        Given I submit

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
        Given there is no voicemail "152"
        Given there is no SIP line "152"
        Given I add a user
        Given I set the text field "First name" to "Bail"
        Given I set the text field "Last name" to "Tarkin"
        Given I set the select field "Language" to "en_US"
        Given I enable the XiVO Client as "bail" pass "tarkin" profile "Client"
        Given I add a SIP line "152" to the user
        Given I add a voicemail "152"
        Given I submit

        When I start the XiVO Client
        When I log in the XiVO Client as "bail", pass "tarkin"
        Then the Xlet identity shows a voicemail "152"

    Scenario: Display agent icon and number
        Given I am logged in

        Given there is an agent "C3PO" with number "153"
        Given there is a user "Darth" "Chewbacca"
        Given I edit the user "Darth" "Chewbacca"
        Given I enable the XiVO Client as "darth" pass "chewbacca" profile "Client"
        Given I submit

        When I edit the user "Darth" "Chewbacca"
        When I go to the "Services" tab
        When I set the select field "Agent" to "C3PO (153@default)"
        When I submit
        When I start the XiVO Client
        When I log in the XiVO Client as "darth", pass "chewbacca", unlogged agent
        Then the Xlet identity shows an agent "153"

        When I log out of the XiVO Client
        When I edit the user "Darth" "Chewbacca"
        When I go to the "Services" tab
        When I set the select field "Agent" to " "
        When I submit
        When I log in the XiVO Client as "darth", pass "chewbacca"
        Then the Xlet identity does not show any agent
