Feature: Stats generation

    Scenario: 12 Generation of event LEAVEEMPTY
        Given there is no agents logged
        Given there is no "LEAVEEMPTY" entry in queue "q10"
        Given there are users with infos:
          | firstname | lastname | number | context     | agent_number | protocol |
          | User      |      010 |   1010 | statscenter |          010 | sip      |
          | User      |      011 |   1011 | statscenter |              | sip      |
        Given there are queues with infos:
          | name | number | context     | leavewhenempty     | agents_number |
          | q10  | 5010   | statscenter | unavailable,paused | 010           |
        When I log agent "010"
        When chan_test calls "5010@statscenter" with id "5010-1"
        When chan_test calls "5010@statscenter" with id "5010-2"
        When I unlog agent "010"
        When chan_test hangs up "5010-1"
        When chan_test hangs up "5010-2"
        When I wait 3 seconds for the data processing
        Then i should see 2 "LEAVEEMPTY" event in queue "q10" in the queue log
