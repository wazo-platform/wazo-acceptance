Feature: Stat

    Scenario: Call a queue that is normally
        Given there is no queue with name "q2"
        Given there is no "ABANDON" entry in queue "q2"
        Given there is a queue "q2" in context "statscenter" with number "5502"
        Given I wait 5 seconds for the dialplan to be reloaded
        Given there is 3 calls enter in queue "q2" with number "5502@statscenter"
        Then i should see 3 "ABANDON" calls in queue "q2" in the queue log
