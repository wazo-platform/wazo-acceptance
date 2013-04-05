Feature: Stat

    Scenario: Generation of event EXITWITHTIMEOUT
        Given there are no calls running
        Given there is no agents logged
        Given there is no "EXITWITHTIMEOUT" entry in queue "q12"
        Given there are users with infos:
         | firstname | lastname | number | context     | agent_number |
         | User      | 012      |   1012 | statscenter | 012          |
        Given there are queues with infos:
            | name | number | context     | ringing_time | agents_number |
            | q12  | 5012   | statscenter | 30           | 012           |
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I log agent "012" on extension "1012@statscenter"
        Given I wait 5 seconds for the calls processing
        Given there is 2 calls to extension "5012@statscenter" and wait
        Given I wait 35 seconds for the calls processing
        Then i should see 2 "EXITWITHTIMEOUT" event in queue "q12" in the queue log

    Scenario: Generate corrupt stats with EXITWITHTIMEOUT event
        Given there are a corrupt entry in queue_log
        When execute xivo-stat
        Then I don't should not have an error
