Feature: Stat

    Scenario: Generation of event RINGNOANSWER
        Given there is no queue with name "q4"
        Given there is no queue with number "5004"
        Given there is no agent with number "004"
        Given there is no user "User" "004"
        Given there is no "RINGNOANSWER" entry in queue "q4"
        Given there is a user "User" "004" in context "statscenter" with number "1004"
        Given there is a agent "Agent" "004" in context "statscenter" with number "004"
        Given there is a queue "q4" in context "statscenter" with number "5004" with agent "004"
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I log agent "004" on extension "1004"
        Given I wait 5 seconds for the calls processing
        Given there is 1 calls to extension "5004" of a duration of 3 seconds
        Given I logout agent "004" on extension "1004"
        Given I wait 5 seconds for the calls processing
        Then i should see 1 "RINGNOANSWER" event in queue "q4" in the queue log
