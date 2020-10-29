Feature: Stats generation

    Scenario: 01 Generation of event FULL
        Given there is no queue_log for queue "q01"
        Given there are agents with infos:
          | number |
          | 001    |
        Given there are queues with infos:
          | name | exten | context     | maxlen | agents |
          | q01  | 3501   | default | 1      | 001           |
        When chan_test calls "3501@default" with id "3501-1"
        When chan_test calls "3501@default" with id "3501-2"
        When chan_test calls "3501@default" with id "3501-3"
        When chan_test calls "3501@default" with id "3501-4"
        When I wait "3" seconds for the call to be forwarded
        Then queue_log contains 3 "FULL" events for queue "q01"
