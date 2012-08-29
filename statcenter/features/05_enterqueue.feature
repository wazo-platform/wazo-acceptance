Feature: Stat

    Scenario: Generation of event ENTERQUEUE
        Given there are no calls running
        Given there is no queue with name "q05" or number "5005"
        Given there is no agent with number "005"
        Given there is no "ENTERQUEUE" entry in queue "q05"
        Given there is a agent "Agent" "005" with extension "005@statscenter"
        Given there is a queue "q05" with extension "5005@statscenter" with agent "005"
        Given I wait 5 seconds for the dialplan to be reloaded
        Given there is 3 calls to extension "5005@statscenter" then i hang up after "3s"
        Given I wait 5 seconds for the calls processing
        Then i should see 3 "ENTERQUEUE" event in queue "q05" in the queue log
