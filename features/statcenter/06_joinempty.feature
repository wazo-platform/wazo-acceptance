Feature: Stat

    Scenario: Generation of event JOINEMPTY
        Given there are no calls running
        Given there is no "JOINEMPTY" entry in queue "q06"
        Given there are queues with infos:
            | name | number | context     | joinempty   |
            | q06  | 5006   | statscenter | unavailable |
        Given I wait 5 seconds for the dialplan to be reloaded
        Given there is 3 calls to extension "5006@statscenter"
        Given I wait 7 seconds for the calls processing
        Then i should see 3 "JOINEMPTY" event in queue "q06" in the queue log
