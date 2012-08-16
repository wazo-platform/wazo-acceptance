Feature: Stat

    Scenario: Call a queue that is normally
        Given there is no queue with name "q5"
        Given there is no queue with number "5005"
        Given there is no "ENTERQUEUE" entry in queue "q5"
        Given there is a queue "q5" in context "statscenter" with number "5005"
        Given I wait 5 seconds for the dialplan to be reloaded
        Given there is 3 calls to extension "5005"
        Given I wait 5 seconds for the calls processing
        Then i should see 3 "ENTERQUEUE" event in queue "q5" in the queue log
