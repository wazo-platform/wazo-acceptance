Feature: Stat

    Scenario: Generation of event FULL
        Given there is no "FULL" entry in queue "q01"
        Given there is a agent "Agent" "001" with extension "001@statscenter"
        Given there are queues with infos:
            | name | number | context     | maxlen | agent_numbers |
            | q01  | 5001   | statscenter | 1      | 001           |

        When chan_test calls "5001@statscenter" with id "5001-1"
        When chan_test calls "5001@statscenter" with id "5001-2"
        When chan_test calls "5001@statscenter" with id "5001-3"
        When chan_test calls "5001@statscenter" with id "5001-4"
        Given I wait 2 seconds for the calls processing
        Then i should see 3 "FULL" event in queue "q01" in the queue log
        When chan_test hangs up "5001-1"
        When chan_test hangs up "5001-2"
        When chan_test hangs up "5001-3"
        When chan_test hangs up "5001-4"