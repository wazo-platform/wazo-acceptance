Feature: Stats generation

    Scenario: 01 Generation of event FULL
        Given there is no queue_log for queue "q01"
        Given there are agents with infos:
          | number |
          | 001    |
        Given there are queues with infos:
          | name | exten | context | option_maxlen | agents |
          | q01  | 3501  | default | 1             | 001    |
        When chan_test calls "3501@default" with id "3501-1"
        When chan_test calls "3501@default" with id "3501-2"
        When chan_test calls "3501@default" with id "3501-3"
        When chan_test calls "3501@default" with id "3501-4"
        When I wait 3 seconds for the call processing
        Then queue_log contains 3 "FULL" events for queue "q01"

    Scenario: 02 Generation of event ABANDON
        Given there is no queue_log for queue "q02"
        Given there are agents with infos:
          | number |
          | 002    |
        Given there are queues with infos:
          | name | exten | context | agents |
          | q02  | 3502  | default | 002    |
        When chan_test calls "3502@default" with id "3502-1"
        When chan_test calls "3502@default" with id "3502-2"
        When chan_test calls "3502@default" with id "3502-3"
        When I wait 3 seconds to simulate call center
        When chan_test hangs up channel with id "3502-1"
        When chan_test hangs up channel with id "3502-2"
        When chan_test hangs up channel with id "3502-3"
        When I wait 3 seconds for the call processing
        Then queue_log contains 3 "ABANDON" events for queue "q02"

    Scenario: 03 Generation of event CONNECT
        Given there is no queue_log for queue "q03"
        Given there are telephony users with infos:
          | firstname | lastname | exten | context | with_phone | agent_number |
          | Agent     | 003      | 1503  | default | yes        | 003          |
        Given there are queues with infos:
          | name | exten | context | agents |
          | q03  | 3503  | default | 003    |
        Given agent "003" is logged
        When chan_test calls "3503@default" with id "3503-1"
        When I wait 2 seconds for the call processing
        When "Agent 003" answers
        When chan_test hangs up channel with id "3503-1"
        When I wait 3 seconds for the call processing
        Then queue_log contains 1 "CONNECT" events for queue "q03"

    Scenario: 04 Generation of event RINGNOANSWER
        Given there is no queue_log for queue "q04"
        Given there are telephony users with infos:
          | firstname | lastname | exten | context | with_phone | agent_number |
          | Agent     | 004      | 1504  | default | yes        | 004          |
        Given there are queues with infos:
          | name | exten | context | agents | option_timeout |
          | q04  | 3504  | default | 004    | 5                           |
        Given agent "004" is logged
        When chan_test calls "3504@default" with id "3504-1"
        When I wait 6 seconds for the timeout to expire
        When chan_test hangs up channel with id "3504-1"
        When I wait 3 seconds for the call processing
        Then queue_log contains 1 "RINGNOANSWER" events for queue "q04"

    Scenario: 05 Generation of event ENTERQUEUE
        Given there is no queue_log for queue "q05"
        Given there are agents with infos:
          | number |
          | 005    |
        Given there are queues with infos:
          | name | exten | context | agents |
          | q05  | 3505  | default | 005    |
        When chan_test calls "3505@default" with id "3505-1"
        When chan_test calls "3505@default" with id "3505-2"
        When chan_test calls "3505@default" with id "3505-3"
        When I wait 3 seconds to simulate call center
        When chan_test hangs up channel with id "3505-1"
        When chan_test hangs up channel with id "3505-2"
        When chan_test hangs up channel with id "3505-3"
        When I wait 3 seconds for the call processing
        Then queue_log contains 3 "ENTERQUEUE" events for queue "q05"

    Scenario: 06 Generation of event JOINEMPTY
        Given there is no queue_log for queue "q06"
        Given there are queues with infos:
          | name | exten | context | option_joinempty |
          | q06  | 3506  | default | unavailable      |
        When chan_test calls "3506@default" with id "3506-1"
        When chan_test calls "3506@default" with id "3506-2"
        When chan_test calls "3506@default" with id "3506-3"
        When I wait 3 seconds to simulate call center
        When chan_test hangs up channel with id "3506-1"
        When chan_test hangs up channel with id "3506-2"
        When chan_test hangs up channel with id "3506-3"
        When I wait 3 seconds for the call processing
        Then queue_log contains 3 "JOINEMPTY" events for queue "q06"

    Scenario: 07 Generation of event AGENTCALLBACKLOGIN
        Given there is no queue_log for agent "007"
        Given there are telephony users with infos:
          | firstname | lastname | exten | context | with_phone | agent_number |
          | Agent     | 007      | 1507  | default | yes        | 007          |
        When I log agent "007" from phone
        When I wait 3 seconds for the call processing
        # Login twice = failure = only one event
        When I log agent "007" from phone
        When I wait 3 seconds for the call processing
        Then queue_log contains 1 "AGENTCALLBACKLOGIN" events for agent "007"

    Scenario: 08 Generation of event AGENTCALLBACKLOGOFF
        Given there is no queue_log for agent "008"
        Given there are telephony users with infos:
          | firstname | lastname | exten | context | with_phone | agent_number |
          | Agent     | 008      | 1508  | default | yes        | 008          |
        When I log agent "008" from phone
        When I wait 3 seconds for the call processing
        When I unlog agent "008" from phone
        When I wait 3 seconds for the call processing
        # Logoff twice = failure = only one event
        When I unlog agent "008" from phone
        When I wait 3 seconds for the call processing
        Then queue_log contains 1 "AGENTCALLBACKLOGOFF" events for agent "008"

    Scenario: 09 Generation of event COMPLETECALLER
        Given there is no queue_log for queue "q09"
        Given there are telephony users with infos:
          | firstname | lastname | exten | context | with_phone | agent_number |
          | Agent     | 009      | 1509  | default | yes        | 009          |
        Given there are queues with infos:
          | name | exten | context | agents |
          | q09  | 3509  | default | 009    |
        Given agent "009" is logged
        When chan_test calls "3509@default" with id "3509-1"
        When I wait 2 seconds to simulate call center
        When "Agent 009" answers
        When chan_test hangs up channel with id "3509-1"
        When I wait 3 seconds for the call processing
        Then queue_log contains 1 "COMPLETECALLER" events for queue "q09"

    Scenario: 10 Generation of event COMPLETEAGENT
        Given there is no queue_log for queue "q10"
        Given there are telephony users with infos:
          | firstname | lastname | exten | context | with_phone | agent_number |
          | Agent     | 010      | 1510  | default | yes        | 010          |
        Given there are queues with infos:
          | name | exten | context | agents |
          | q10  | 3510  | default | 010    |
        Given agent "010" is logged
        When chan_test calls "3510@default" with id "3510-1"
        When I wait 1 seconds to simulate call center
        When "Agent 010" answers
        When I wait 1 seconds to simulate call center
        When "Agent 010" hangs up
        When I wait 3 seconds for the call processing
        Then queue_log contains 1 "COMPLETEAGENT" events for queue "q10"

    Scenario: 11 Generation of event CLOSED
        Given there is no queue_log for queue "q11"
        Given I have a schedule "always_closed" in "America/Montreal" with the following schedules:
          | periods | months | month_days | week_days | hours_start | hours_end |
          | open    |      1 |          1 |         1 |       00:00 |     00:01 |
        Given there are queues with infos:
          | name | exten | context | schedule      |
          | q11  | 3511  | default | always_closed |
        When chan_test calls "3511@default" with id "3511-1"
        When chan_test calls "3511@default" with id "3511-2"
        When I wait 2 seconds to simulate call center
        When chan_test hangs up channel with id "3511-1"
        When chan_test hangs up channel with id "3511-2"
        When I wait 3 seconds for the call processing
        Then queue_log contains 2 "CLOSED" events for queue "q11"

    Scenario: 12 Generation of event EXITWITHTIMEOUT
        Given there is no queue_log for queue "q12"
        Given there are telephony users with infos:
          | firstname | lastname | exten | context | with_phone | agent_number |
          | Agent     | 012      | 1512  | default | yes        | 012          |
        Given there are queues with infos:
          | name | exten | context | timeout | option_timeout | agents | 
          | q12  | 3512  | default | 10      | 5              | 012    |
        Given agent "012" is logged
        When chan_test calls "3512@default" with id "3512-1"
        When chan_test calls "3512@default" with id "3512-2"
        When I wait 12 seconds for the timeout to expire
        When chan_test hangs up channel with id "3512-1"
        When chan_test hangs up channel with id "3512-2"
        Then queue_log contains 2 "EXITWITHTIMEOUT" events for queue "q12"
