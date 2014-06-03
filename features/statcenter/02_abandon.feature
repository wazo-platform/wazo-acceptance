Feature: Stat

    Scenario: Generation of event ABANDON
        Given there is no "ABANDON" entry in queue "q02"
        Given there is a agent "Agent" "002" with extension "002@statscenter"
        Given there are queues with infos:
            | name | number | context     | agents_number |
            | q02  | 5002   | statscenter | 002           |
        When chan_test calls "5002@statscenter" with id "5002-1"
        When chan_test calls "5002@statscenter" with id "5002-2"
        When chan_test calls "5002@statscenter" with id "5002-3"
        Given I wait 2 seconds for the calls processing
        When chan_test hangs up "5002-1"
        When chan_test hangs up "5002-2"
        When chan_test hangs up "5002-3"
        Given I wait 1 seconds for the calls processing
        Then i should see 3 "ABANDON" event in queue "q02" in the queue log
