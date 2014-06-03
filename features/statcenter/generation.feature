Feature: Stats generation

    Scenario: 01 Generation of event FULL
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

    Scenario: 02 Generation of event ABANDON
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

    Scenario: 03 Generation of event CONNECT
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

    Scenario: 04 Generation of event RINGNOANSWER
        Given there is no agents logged
        Given there is no "RINGNOANSWER" entry in queue "q04"
        Given there are users with infos:
          | firstname | lastname | number | context     | agent_number | protocol |
          | User      | 004      |   1004 | statscenter | 004          | sip      |
        Given there are queues with infos:
          | name | number | context     | agents_number |
          | q04  | 5004   | statscenter | 004           |
        When "User 004" calls "*31004"
        When chan_test calls "5004@statscenter" with id "5004-1"
        When "User 004" calls "*32004"
        When chan_test hangs up "5004-1"
        Then I should see 1 "RINGNOANSWER" event in queue "q04" in the queue log

    Scenario: 05 Generation of event ENTERQUEUE
        Given there is no "ENTERQUEUE" entry in queue "q05"
        Given there is a agent "Agent" "005" with extension "005@statscenter"
        Given there are queues with infos:
          | name | number | context     | agents_number |
          | q05  | 5005   | statscenter | 005           |
        When chan_test calls "5005@statscenter" with id "5005-1"
        When chan_test calls "5005@statscenter" with id "5005-2"
        When chan_test calls "5005@statscenter" with id "5005-3"
        Given I wait 2 seconds for the calls processing
        When chan_test hangs up "5005-1"
        When chan_test hangs up "5005-2"
        When chan_test hangs up "5005-3"
        Given I wait 1 seconds for the calls processing
        Then i should see 3 "ENTERQUEUE" event in queue "q05" in the queue log

    Scenario: 06 Generation of event JOINEMPTY
        Given there is no "JOINEMPTY" entry in queue "q06"
        Given there are queues with infos:
          | name | number | context     | joinempty   |
          | q06  | 5006   | statscenter | unavailable |
        When chan_test calls "5006@statscenter" with id "5006-1"
        When chan_test calls "5006@statscenter" with id "5006-2"
        When chan_test calls "5006@statscenter" with id "5006-3"
        Given I wait 2 seconds for the calls processing
        When chan_test hangs up "5005-1"
        When chan_test hangs up "5005-2"
        When chan_test hangs up "5005-3"
        Given I wait 1 seconds for the calls processing
        Then i should see 3 "JOINEMPTY" event in queue "q06" in the queue log

    Scenario: 07 Generation of event AGENTCALLBACKLOGIN
        Given there is no agents logged
        Given there is no "AGENTCALLBACKLOGIN" entry for agent "007"
        Given there are users with infos:
         | firstname | lastname | number | context     | agent_number | protocol |
         | User      | 007      |   1007 | statscenter | 007          | sip      |
        When "User 007" calls "*31007"
        Given I wait 2 seconds for the calls processing
        Then I should see 1 "AGENTCALLBACKLOGIN" event for agent "007" in the queue log

    Scenario: 08 Login twice using AGENTCALLBACKLOGIN
        Given there is no agents logged
        Given there is no "AGENTCALLBACKLOGIN" entry for agent "007"
        Given there are users with infos:
         | firstname | lastname | number | context     | agent_number | protocol |
         | User      | 007      |   1007 | statscenter | 007          | sip      |
        When "User 007" calls "*31007"
        Given I wait 2 seconds for the calls processing
        When "User 007" calls "*31007"
        Given I wait 2 seconds for the calls processing
        Then I should see 1 "AGENTCALLBACKLOGIN" event for agent "007" in the queue log

    Scenario: 09 Logoff when not logged in
        Given there is no agents logged
        Given there is no "AGENTCALLBACKLOGOFF" entry for agent "007"
        Given there are users with infos:
         | firstname | lastname | number | context     | agent_number | protocol |
         | User      | 007      |   1007 | statscenter | 007          | sip      |
        When "User 007" calls "*31007"
        Given I wait 2 seconds for the calls processing
        When "User 007" calls "*32007"
        Given I wait 2 seconds for the calls processing
        When "User 007" calls "*32007"
        Given I wait 2 seconds for the calls processing
        Then I should see 1 "AGENTCALLBACKLOGOFF" event for agent "007" in the queue log

    Scenario: 10 Generation of event COMPLETECALLER
        Given there is no agents logged
        Given there is no "COMPLETECALLER" entry in queue "q08"
        Given there are users with infos:
         | firstname | lastname | number | context     | agent_number | protocol |
         | User      | 008      |   1008 | statscenter | 008          | sip      |
        Given there are queues with infos:
            | name | number | context     | agents_number |
            | q08  | 5008   | statscenter | 008           |
        When "User 008" calls "*31008"
        Given I wait 2 seconds for the calls processing
        When chan_test calls "5008@statscenter" with id "5008-1"
        Given I wait 2 seconds for the calls processing
        When "User 008" answers
        When chan_test hangs up "5008-1"
        Then I should see 1 "COMPLETECALLER" event in queue "q08" in the queue log

    Scenario: 11 Generation of event COMPLETEAGENT
        Given there is no agents logged
        Given there is no "COMPLETEAGENT" entry in queue "q09"
        Given there are users with infos:
         | firstname | lastname | number | context     | agent_number | protocol |
         | User      | 009      |   1009 | statscenter | 009          | sip      |
        Given there are queues with infos:
            | name | number | context     | agents_number |
            | q09  | 5009   | statscenter | 009           |
        When "User 009" calls "*31009"
        Given I wait 2 seconds for the calls processing
        When chan_test calls "5009@statscenter" with id "5009-1"
        Given I wait 1 seconds for the calls processing
        When "User 009" answers
        Given I wait 1 seconds for the calls processing
        When "User 009" hangs up
        When chan_test hangs up "5009-1"
        Then i should see 1 "COMPLETEAGENT" event in queue "q09" in the queue log
        