Feature: Stat

    Scenario: Generation of event CLOSED
        Given there are no calls running
        Given there is no "CLOSED" entry in queue "q11"
        Given there is a schedule named "always_closed" with the following timetable:
            | hours       | weekdays | monthdays | months |
            | 00:00-00:01 | 1-1      | 1-1       | 1-1    |
        Given there are queues wth infos:
            | name | number | context     | schedule_name |
            | q11  | 5011   | statscenter | always_closed |
        Given I wait 5 seconds for the dialplan to be reloaded
        Given there is 2 calls to extension "5011@statscenter" and wait
        Given I wait 5 seconds for the calls processing
        Then i should see 2 "CLOSED" event in queue "q11" in the queue log

