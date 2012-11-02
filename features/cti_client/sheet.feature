Feature: Sheet

    Scenario: xivo-calleridname variable on agent linked
        Given I have a sheet model named "testsheet" with the variables:
        | variable          |
        | xivo-calleridnum  |
        | xivo-calleridname |

        Given I assign the sheet "testsheet" to the "Agent linked" event

        Given there is a user "Cedric" "Abunar" with an agent "1153@default" and CTI profile "Client"

        Given there is a queue "frere" with extension "3009@default" with agent "1153"
        Given there is an incall "3001" in context "from-extern" to the "Queue" "frere" with caller id name "Laurent Demange" number "1234"

        When I start the XiVO Client
        When I enable screen pop-up
        When I log in the XiVO Client as "cedric", pass "abunar", unlogged agent

        Given there are no calls running
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I log agent "1153" on extension "1153@default"
        Given I wait 5 seconds for the calls processing
        Given I wait call then I answer then I hang up after "3s"
        When there is 1 calls to extension "3001@from-extern" on trunk "to_incall" and wait

        Given I wait 10 seconds for the calls processing

        Then I see a sheet with the following values:
        | Variable          | Value           |
        | xivo-calleridnum  | 1234            |
        | xivo-calleridname | Laurent Demange |

    Scenario: Variables on link event to a User
        Given I have a sheet model named "testsheet" with the variables:
        | variable          |
        | xivo-calledidname |
        | xivo-calledidnum  |
        Given I assign the sheet "testsheet" to the "Link" event

        Given there is a user "Alice" "Gopher" with extension "1007@default" and CTI profile "Client"
        Given there is an incall "1007" in context "from-extern" to the "User" "Alice Gopher" with caller id name "Tux" number "5555555555"

        When I start the XiVO Client
        When I enable screen pop-up
        When I log in the XiVO client as "alice", pass "gopher"

        Given there are no calls running
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I register extension "1007"
        Given I wait call then I answer then I hang up after "3s"
        When there is 1 calls to extension "1007@from-extern" on trunk "to_incall" and wait

        Given I wait 10 seconds for the call processing

        Then I see a sheet with the following values:
        | Variable          | Value        |
        | xivo-calledidname | Alice Gopher |
        | xivo-calledidnum  | 1007         |

    Scenario: Variables on link event to a Queue
        Given I have a sheet model named "testsheet" with the variables:
        | variable          |
        | xivo-calledidname |
        | xivo-calledidnum  |
        Given I assign the sheet "testsheet" to the "Link" event

        Given there is a user "Alice" "Gopher" with extension "1007@default" and CTI profile "Client"
        Given there is a queue "frere" with extension "3001@default" with user "1007"
        Given there is an incall "3001" in context "from-extern" to the "Queue" "frere" with caller id name "Tux" number "5555555555"

        When I start the XiVO Client
        When I enable screen pop-up
        When I log in the XiVO client as "alice", pass "gopher"

        Given there are no calls running
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I register extension "1007"
        Given I wait call then I answer then I hang up after "3s"
        When there is 1 calls to extension "3001@from-extern" on trunk "to_incall" and wait

        Given I wait 10 seconds for the call processing

        Then I see a sheet with the following values:
        | Variable          | Value |
        | xivo-calledidname | frere |
        | xivo-calledidnum  | 3001  |

    Scenario: Variables on link event to a Group
        Given I have a sheet model named "testsheet" with the variables:
        | variable          |
        | xivo-calledidname |
        | xivo-calledidnum  |
        Given I assign the sheet "testsheet" to the "Link" event

        Given there is a user "Alice" "Gopher" with extension "1007@default" and CTI profile "Client"
        Given there is a group "main" with extension "2006@default" and users:
          | firstname | lastname |
          | Alice     | Gopher   |
        Given there is an incall "2006" in context "from-extern" to the "Group" "main" with caller id name "Tux" number "5555555555"

        When I start the XiVO Client
        When I enable screen pop-up
        When I log in the XiVO client as "alice", pass "gopher"

        Given there are no calls running
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I register extension "1007"
        Given I wait call then I answer then I hang up after "3s"
        When there is 1 calls to extension "2006@from-extern" on trunk "to_incall" and wait

        Given I wait 10 seconds for the call processing

        Then I see a sheet with the following values:
        | Variable          | Value |
        | xivo-calledidname | main  |
        | xivo-calledidnum  | 2006  |

  Scenario: Variables on dial event to group
        Given I have a sheet model named "testsheet" with the variables:
        | variable          |
        | xivo-calledidname |
        | xivo-calledidnum  |
        Given I assign the sheet "testsheet" to the "Dial" event

        Given there is a user "Alice" "Gopher" with extension "1007@default" and CTI profile "Client"
        Given there is a user "Gnu" "Linux" with extension "1006@default" and CTI profile "Client"
        Given there is a group "main" with extension "2006@default" and users:
          | firstname | lastname |
          | Alice     | Gopher   |
        Given there is an incall "2006" in context "from-extern" to the "Group" "main" with caller id name "Tux" number "5555555555"

        When I start the XiVO Client
        When I enable screen pop-up
        When I log in the XiVO client as "alice", pass "gopher"

        Given there are no calls running
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I register extension "1007"
        Given I wait call then I answer then I hang up after "3s"
        When there is 1 calls to extension "2006@from-extern" on trunk "to_incall" and wait

        Given I wait 10 seconds for the call processing

        Then I see a sheet with the following values:
        | Variable          | Value |
        | xivo-calledidname | main  |
        | xivo-calledidnum  | 2006  |

        When I log out of the XiVO Client
        When I log in the XiVO client as "gnu", pass "linux"

        Given there are no calls running
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I wait call then I answer then I hang up after "3s"
        When there is 1 calls to extension "2006@from-extern" on trunk "to_incall" and wait

        Given I wait 10 seconds for the call processing

        Then I should not see any sheet
