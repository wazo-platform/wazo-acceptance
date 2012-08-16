Feature: Saturated calls

    Scenario: Generate stats for saturated calls
        Given there is no queue with name "q1"
        Given there is no "FULL" entry in queue "q1" between "2012-07-01 08:00:00" and "2012-07-01 11:59:59"
        Given there is no "DIVERT_CA_RATIO" entry in queue "q1" between "2012-07-01 08:00:00" and "2012-07-01 11:59:59"
        Given there is no "DIVERT_HOLTIME" entry in queue "q1" between "2012-07-01 08:00:00" and "2012-07-01 11:59:59"
        Given there is a queue "q1" in context "statscenter" with number "5502"
        Given there is a statistic configuration "test" from "8" to "12" with queue "q1"
        Given I have to following queue_log entries:
          | time                       | callid      | queuename | agent | event           | data1 | data2 | data3 | data4 | data5 |
          | 2012-07-01 08:00:00.000000 | saturated_1 | q1        | NONE  | DIVERT_CA_RATIO |       |       |       |       |       |
          | 2012-07-01 08:59:59.999999 | saturated_2 | q1        | NONE  | FULL            |       |       |       |       |       |
          | 2012-07-01 08:00:00.000001 | saturated_3 | q2        | NONE  | FULL            |       |       |       |       |       |
          | 2012-07-01 09:00:00.000000 | saturated_4 | q1        | NONE  | DIVERT_CA_RATIO |       |       |       |       |       |
        Given I clear and generate the statistics cache
        Then I should have the following statististics on "q1" on "2012-07-01" on configuration "test":
          | time    | Saturated |
          | 8h-9h   |         2 |
          | 9h-10h  |         1 |
          | 10h-11h |         0 |
          | total   |         3 |
