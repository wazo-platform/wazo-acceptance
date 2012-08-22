Feature: Stat

    Scenario: Generation of event CONNECT
        Given there is no queue with name "q3"
        Given there is no queue with number "5003"
        Given there is no agent with number "003"
        Given there is no user "User" "003"
        Given there is no "CONNECT" entry in queue "q3"
        Given there is a user "User" "003" in context "statscenter" with number "1003"
        Given there is a agent "Agent" "003" in context "statscenter" with number "003"
        Given there is a queue "q3" in context "statscenter" with number "5003" with agent "003"
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I log agent "003" on extension "1003"
        Given I wait 5 seconds for the calls processing
        Given I wait call then hangup after "3s"
        Given there is 1 calls to extension "5003" and wait
        Given I wait 10 seconds for the calls processing
        Then i should see 1 "CONNECT" event in queue "q3" in the queue log
