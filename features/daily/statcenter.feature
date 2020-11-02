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
