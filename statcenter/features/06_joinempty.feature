Feature: Stat

    Scenario: Generation of event JOINEMPTY
        Given there is no queue with name "q06"
        Given there is no queue with number "5006"
        Given there is no "JOINEMPTY" entry in queue "q06"
        Given there is a queue "q06" in context "statscenter" with number "5006"
        Given I wait 5 seconds for the dialplan to be reloaded
        Given there is 3 calls to extension "5006"
        Given I wait 7 seconds for the calls processing
        Then i should see 3 "JOINEMPTY" event in queue "q06" in the queue log
