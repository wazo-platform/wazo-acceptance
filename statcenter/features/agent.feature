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
