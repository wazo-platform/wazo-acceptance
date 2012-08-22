Feature: Stat

    Scenario: Generation of event ENTERQUEUE
        Given there is no queue with name "q05" or number "5005"
        Given there is no agent with number "005"
        Given there is no "ENTERQUEUE" entry in queue "q05"
        Given there is a agent "Agent" "005" in context "statscenter" with number "005"
        Given there is a queue "q05" in context "statscenter" with number "5005" with agent "005"
        Given I wait 5 seconds for the dialplan to be reloaded
        Given there is 3 calls to extension "5005" then i hang up after "3s"
        Given I wait 5 seconds for the calls processing
        Then i should see 3 "ENTERQUEUE" event in queue "q05" in the queue log
