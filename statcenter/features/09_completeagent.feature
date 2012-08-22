Feature: Stat

    Scenario: Generation of event COMPLETEAGENT
        Given there is no queue with name "q9"
        Given there is no queue with number "5009"
        Given there is no agent with number "009"
        Given there is no user "User" "009"
        Given there is no "COMPLETEAGENT" entry in queue "q9"
        Given there is a user "User" "009" in context "statscenter" with number "1009"
        Given there is a agent "Agent" "009" in context "statscenter" with number "009"
        Given there is a queue "q9" in context "statscenter" with number "5009" with agent "009"
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I log agent "009" on extension "1009"
        Given I wait 5 seconds for the calls processing
        Given I wait call then hangup after "2s"
        Given I wait 2 seconds for the calls processing
        Given there is 1 calls to extension "5009" and wait
        Given I wait 9 seconds for the calls processing
        Then i should see 1 "COMPLETEAGENT" event in queue "q9" in the queue log
