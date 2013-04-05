Feature: Stat

    Scenario: Generation of event LEAVEEMPTY
        Given there are no calls running
        Given there is no agents logged
        Given there is no "LEAVEEMPTY" entry in queue "q10"
        Given there are users with infos:
         | firstname | lastname | number | context     | agent_number |
         | User      | 010      |   1010 | statscenter | 010          |
        Given there are queues with infos:
            | name | number | context     | leavewhenempty     | agents_number |
            | q10  | 5010   | statscenter | unavailable,paused | 010           |
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I log agent "010" on extension "1010@statscenter"
        Given I wait 5 seconds for the calls processing
        Given there is 2 calls to extension "5010@statscenter" and wait
        Given I logout agent "010" on extension "1010@statscenter"
        Given I wait 25 seconds for the calls processing
        Then i should see 2 "LEAVEEMPTY" event in queue "q10" in the queue log

