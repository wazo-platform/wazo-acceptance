Feature: Stat

    Scenario: Call a queue that is normally
        Given there is no queue with name "q5"
        Given there is no "ENTERQUEUE" entry in queue "q5"
        Given there is a queue "q5" in context "statscenter" with number "5500"
        Given I wait 5 seconds for the dialplan to be reloaded
        Given there is 3 calls enter in queue "q5" with number "5500@statscenter"
        Then i should see 3 "ENTERQUEUE" calls in queue "q5" in the queue log
