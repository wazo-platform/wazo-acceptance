Feature: Stat

    Scenario: Call a queue that is saturated
        Given I am logged in
        Given there is no queue "q1"
        Given there is no "FULL" entry in queue "q1"
        Given there is a queue "q1" with number "5200" that is statured
        Given I wait 5 seconds for the dialplan to be reloaded
        Given there is 3 calls satured in queue "q1" with number "5200"
        Then i should see 3 "FULL" calls in queue "q1" in the queue log
