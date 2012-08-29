Feature: WEBI Queue Stats

    Scenario: Generate stats for saturated calls
        Given there is no queue with name "q01" or number "5001"
        Given there is no "FULL" entry in queue "q01" between "2012-07-01 08:00:00" and "2012-07-01 11:59:59"
        Given there is no "FULL" entry in queue "q02" between "2012-07-01 08:00:00" and "2012-07-01 11:59:59"
        Given there is no "DIVERT_CA_RATIO" entry in queue "q01" between "2012-07-01 08:00:00" and "2012-07-01 11:59:59"
        Given there is no "DIVERT_HOLDTIME" entry in queue "q01" between "2012-07-01 08:00:00" and "2012-07-01 11:59:59"
        Given there is a queue "q01" with extension "5001@statscenter"
        Given there is a statistic configuration "test" from "8:00" to "12:00" with queue "q01"
        Given I have to following queue_log entries:
          | time                       | callid      | queuename | agent | event           | data1 | data2 | data3 | data4 | data5 |
          | 2012-07-01 08:00:00.000000 | saturated_1 | q01       | NONE  | DIVERT_CA_RATIO |       |       |       |       |       |
          | 2012-07-01 08:59:59.999999 | saturated_2 | q01       | NONE  | FULL            |       |       |       |       |       |
          | 2012-07-01 08:00:00.000001 | saturated_3 | q02       | NONE  | FULL            |       |       |       |       |       |
          | 2012-07-01 09:00:00.000000 | saturated_4 | q01       | NONE  | DIVERT_CA_RATIO |       |       |       |       |       |
          | 2012-07-01 09:59:59.999999 | saturated_5 | q01       | NONE  | DIVERT_HOLDTIME |       |       |       |       |       |
          | 2012-07-01 08:00:00.000001 | saturated_6 | q01       | NONE  | DIVERT_HOLDTIME |       |       |       |       |       |

        Given I clear and generate the statistics cache
        Given I am logged in
        Then I should have the following statististics on "q01" on "2012-07-01" on configuration "test":
          |         | Saturated |
          | 8h-9h   |         3 |
          | 9h-10h  |         2 |
          | 10h-11h |         0 |
          | Total   |         5 |
