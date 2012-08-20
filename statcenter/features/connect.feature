Feature: Stat

    Scenario: Generation of event "CONNECT"
        Given there is no queue with name "q3"
        Given there is no queue with number "5003"
        Given there is a user "Rocky" "Balboa" in context "statscenter" with number "1003"
        Given there is no "CONNECT" entry in queue "q3"
        Given there is a queue "q3" in context "statscenter" with number "5003"
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I log agent "7878" on extension "1003"
        Given I wait call during "7s"
        Given there is 1 calls to extension "5003" and wait
        Given I wait 10 seconds for the calls processing
        Then i should see 1 "CONNECT" event in queue "q3" in the queue log
