Feature: Sheet

    Scenario: xivo-calleridname variable
        Given I have a sheet model named "testsheet" with the variables:
        | variable          |
        | xivo-calleridnum  |
        | xivo-calleridname |

        Given I assign the sheet "testsheet" to the agent linked event

        Given there is no user "Cédric" "Abunar"
        Given there is no agent with number "1153"
        Given there is a user "Cédric" "Abunar" with an agent "1153@default" and CTI profile "Client"

        Given there is a queue "frere" with extension "3009@default" with agent "1153"

        When I start the XiVO Client
        When I enable screen pop-up
        When I log in the XiVO Client as "cedric", pass "abunar", logged agent

        Given there are no calls running
        Given there is 1 calls to extension "3009@default" and wait
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I log agent "1153" on extension "1153@default"
        Given I wait 5 seconds for the calls processing

        Given I wait call then i answer then i hang up after "3s"
        Given I wait 10 seconds for the calls processing

        Then I see a sheet with the following values:
        | Variable          | Value         |
        | xivo-calleridnum  | 1153          |
        | xivo-calleridname | Cédric Abunar |

        When I log out of the XiVO Client
