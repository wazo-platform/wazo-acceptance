Feature: Stat

    Scenario: Generation of event ABANDON
        Given there is no queue with name "q2"
        Given there is no queue with number "5002"
        Given there is no agent with number "002"
        Given there is no "ABANDON" entry in queue "q2"
        Given there is a agent "Agent" "002" in context "statscenter" with number "002"
        Given there is a queue "q2" in context "statscenter" with number "5002" with agent "002"
        Given I wait 5 seconds for the dialplan to be reloaded
        Given there is 3 calls to extension "5002" of a duration of 3 seconds
        Given I wait 6 seconds for the calls processing
        Then i should see 3 "ABANDON" event in queue "q2" in the queue log
