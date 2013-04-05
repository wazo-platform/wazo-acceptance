Feature: Stat

    Scenario: Generation of event COMPLETEAGENT
        Given there are no calls running
        Given there is no agents logged
        Given there is no "COMPLETEAGENT" entry in queue "q09"
        Given there are users with infos:
         | firstname | lastname | number | context     | agent_number |
         | User      | 009      |   1009 | statscenter | 009          |
        Given there are queues with infos:
            | name | number | context     | agents_number |
            | q09  | 5009   | statscenter | 009           |
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I log agent "009" on extension "1009@statscenter"
        Given I wait 5 seconds for the calls processing
        Given I wait call then i answer then i hang up after "2s"
        Given I wait 2 seconds for the calls processing
        Given there is 1 calls to extension "5009@statscenter" and wait
        Given I wait 9 seconds for the calls processing
        Then i should see 1 "COMPLETEAGENT" event in queue "q09" in the queue log

#    Scenario: Generation of event COMPLETEAGENT
#        Given there is no events for queue "q09" in the queue log
#        Given there is a agent with number "009" in context "statscenter"
#        Given there are queues with infos:
#            | name | number | context     | agents_number |
#            | q09  | 5009   | statscenter | 009           |
#        When agent "009" executes the following actions:
#            | action        | number | time      |
#            | logon         |    009 |           |
#            | wait for call |        |           |
#        When there is an incoming call:
#            | action | number           | time       |
#            | call   | 5009@statscenter | 10 seconds |
#            | hangup |                  |            |
#        Then I should see 1 "COMPLETEAGENT" event on queue "q09" in the queue log
