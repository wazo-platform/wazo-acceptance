Feature: Stat

    Scenario: Generation of event CLOSED
        Given there are no calls running
        Given there is no "CLOSED" entry in queue "q11"
        Given there is a queue "q11" closed with extension "5011@statscenter"
        Given I wait 5 seconds for the dialplan to be reloaded
        Given there is 2 calls to extension "5011@statscenter" and wait
        Given I wait 5 seconds for the calls processing
        Then i should see 2 "CLOSED" event in queue "q11" in the queue log

