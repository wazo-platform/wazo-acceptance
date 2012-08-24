Feature: Stat

    Scenario: Generation of event ABANDON
        Given there is no queue with name "q02" or number "5002"
        Given there is no agent with number "002"
        Given there is no "ABANDON" entry in queue "q02"
        Given there is a agent "Agent" "002" with extension "002@statscenter"
        Given there is a queue "q02" with extension "5002@statscenter" with agent "002"
        Given I wait 5 seconds for the dialplan to be reloaded
        Given there is 3 calls to extension "5002@statscenter" then i hang up after "3s"
        Given I wait 6 seconds for the calls processing
        Then i should see 3 "ABANDON" event in queue "q02" in the queue log
