Feature: WEBI Agent Stats

    Scenario: Generate stats for answered calls
        Given there is no queue with name "q01" and number "5001"
        Given there is no agent with number "1"
        Given there is no "COMPLETECALLER" entry in queue "q01" between "2012-07-01 08:00:00" and "2012-07-01 11:59:59"
        Given there is no "CONNECT" entry in queue "q01" between "2012-07-01 08:00:00" and "2012-07-01 11:59:59"
        Given there is no "TRANSFER" entry in queue "q01" between "2012-07-01 08:00:00" and "2012-07-01 11:59:59"
        Given there is no "ENTERQUEUE" entry in queue "q01" between "2012-07-01 08:00:00" and "2012-07-01 11:59:59"
        Given there is a queue "q01" with extension "5001@statscenter"
        Given there is a agent "Agent" "1" with extension "1@statscenter"
        Given there is a statistic configuration "test" from "8:00" to "12:00" with queue "q01" and agent "1"
        Given I have to following queue_log entries:
          | time                       | callid      | queuename | agent     | event               | data1 | data2          | data3 | data4 | data5 |
          | 2012-07-01 10:58:39.750413 | answered_1  | q01       | Agent/1   | COMPLETECALLER      | 1     | 6              | 1     |       |       |
          | 2012-07-01 10:58:33.643463 | answered_1  | q01       | Agent/1   | CONNECT             | 1     | 1346165912.457 | 1     |       |       |
          | 2012-07-01 10:58:32.192729 | answered_1  | q01       | NONE      | ENTERQUEUE          |       | 1201           | 1     |       |       |
          | 2012-07-01 09:54:49.776142 | answered_2  | q01       | Agent/1   | TRANSFER            | s     | user           | 1     | 9     | 1     |
          | 2012-07-01 09:54:40.233811 | answered_2  | q01       | Agent/1   | CONNECT             | 1     | 1346165679.450 | 1     |       |       |
          | 2012-07-01 09:54:39.109284 | answered_2  | q01       | NONE      | ENTERQUEUE          |       | 1201           | 1     |       |       |
          | 2012-07-01 08:54:23.674291 | answered_3  | q01       | Agent/1   | COMPLETECALLER      | 1     | 5              | 1     |       |       |
          | 2012-07-01 08:54:18.711465 | answered_3  | q01       | Agent/1   | CONNECT             | 1     | 1346165657.444 | 1     |       |       |
          | 2012-07-01 08:54:17.039559 | answered_3  | q01       | NONE      | ENTERQUEUE          |       | 1201           | 1     |       |       |

        Given I clear and generate the statistics cache
        Given I am logged in
        Then I should have the following statististics on agent "1" on "2012-07-01" on configuration "test":
          |         | Answered |
          | 8h-9h   |        1 |
          | 9h-10h  |        1 |
          | 10h-11h |        1 |
          | 11h-12h |        0 |
          | Total   |        3 |

    Scenario: Generate stats for total conversation time
        Given there is no queue with name "q02" and number "5002"
        Given there is no agent with number "2"
        Given there is no "COMPLETECALLER" entry in queue "q02" between "2012-01-01 08:00:00" and "2012-01-01 11:59:59"
        Given there is no "COMPLETEAGENT" entry in queue "q02" between "2012-01-01 08:00:00" and "2012-01-01 11:59:59"
        Given there is no "CONNECT" entry in queue "q02" between "2012-01-01 08:00:00" and "2012-01-01 11:59:59"
        Given there is no "TRANSFER" entry in queue "q02" between "2012-01-01 08:00:00" and "2012-01-01 11:59:59"
        Given there is no "ENTERQUEUE" entry in queue "q02" between "2012-01-01 08:00:00" and "2012-01-01 11:59:59"
        Given there is a queue "q02" with extension "5002@statscenter"
        Given there is a agent "Agent" "2" with extension "2@statscenter"
        Given there is a statistic configuration "test_talktime" from "8:00" to "12:00" with queue "q02" and agent "2"
        Given I have to following queue_log entries:
          | time                       | callid      | queuename | agent    | event          | data1 | data2        | data3 | data4 | data5 |
          | 2012-01-01 09:01:06.555555 | talk_time_1 | q02       | Agent/2  | ENTERQUEUE     |       |              |       |       |       |
          | 2012-01-01 09:01:06.666666 | talk_time_1 | q02       | Agent/2  | CONNECT        | 4     | 123456.435   |       |       |       |
          | 2012-01-01 09:01:10.777777 | talk_time_1 | q02       | Agent/2  | COMPLETEAGENT  | 4     | 10           |       |       |       |
          | 2012-01-01 09:02:06.555555 | talk_time_2 | q02       | Agent/2  | ENTERQUEUE     |       |              |       |       |       |
          | 2012-01-01 09:02:06.666666 | talk_time_2 | q02       | Agent/2  | CONNECT        | 5     | 12334234.435 |       |       |       |
          | 2012-01-01 09:02:10.777777 | talk_time_2 | q02       | Agent/2  | COMPLETECALLER | 4     | 7            |       |       |       |
          | 2012-01-01 09:03:06.555555 | talk_time_3 | q02       | Agent/2  | ENTERQUEUE     |       |              |       |       |       |
          | 2012-01-01 09:03:06.666666 | talk_time_3 | q02       | Agent/2  | CONNECT        | 6     | 2222456.435  |       |       |       |
          | 2012-01-01 09:03:10.777777 | talk_time_3 | q02       | Agent/2  | TRANSFER       | 4     | 0            | 0     | 22    |       |

        Given I clear and generate the statistics cache
        Given I am logged in
        Then I should have the following statististics on agent "2" on "2012-01-01" on configuration "test_talktime":
          |         | Conversation |
          | 8h-9h   |     00:00:00 |
          | 9h-10h  |     00:00:39 |
          | 10h-11h |     00:00:00 |
          | 11h-12h |     00:00:00 |
          | Total   |     00:00:39 |
