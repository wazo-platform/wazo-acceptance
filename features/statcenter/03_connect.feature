Feature: Stat

    Scenario: Generation of event CONNECT
        Given there is no agents logged
        Given there is no "CONNECT" entry in queue "q03"
        Given there are users with infos:
          | firstname | lastname | number | context     | agent_number | protocol |
          | User      | 003      |   1003 | statscenter | 003          | sip      |
        Given there are queues with infos:
          | name | number | context     | agents_number |
          | q03  | 5003   | statscenter | 003           |
        
        When "User 003" calls "*31003"
        Given I wait 2 seconds for the calls processing
        When chan_test calls "5003@statscenter" with id "5003-1"
        Given I wait 2 seconds for the calls processing
        When "User 003" answers
        When chan_test hangs up "5003-1"
        Given I wait 1 seconds for the calls processing
        Then i should see 1 "CONNECT" event in queue "q03" in the queue log
