Feature: WEBI Queue Stats


    Scenario: Statistics for calls distributed to two queues at the boundaries of a xivo-stat deletion limit
        Given there is no entries in queue_log between "2013-11-08 08:00:00" and "2013-11-09 00:00:00"
        Given there are queues with infos:
            | name | number | context     |
            | q01  | 5001   | statscenter |
            | q02  | 5002   | statscenter |
        Given there is a statistic configuration "testq1" from "9:00" to "11:00" with queue "q01"
        Given there is a statistic configuration "testq2" from "9:00" to "11:00" with queue "q02"
        Given I have the following queue_log entries:
            | time                       |            callid | queuename | agent      | event          | data1 |             data2 | data3 | data4 | data5 |
            | 2013-11-08 09:53:09.948070 | 1383900788.167039 | q01       | NONE       | ENTERQUEUE     |       |        5555555555 |     1 |       |       |
            | 2013-11-08 09:53:12.684547 | 1383900788.167039 | q01       | Agent/1240 | CONNECT        |     3 | 1383900789.167040 |     2 |       |       |
            | 2013-11-08 10:02:30.219402 | 1383900788.167039 | q01       | Agent/1240 | COMPLETECALLER |     3 |               558 |     1 |       |       |
            | 2013-11-08 10:02:30.569451 | 1383900788.167039 | q02       | NONE       | ENTERQUEUE     |       |        5555555555 |     1 |       |       |
            | 2013-11-08 10:02:30.686291 | 1383900788.167039 | q02       | Agent/1255 | RINGNOANSWER   |     0 |                   |       |       |       |
            | 2013-11-08 10:02:32.770339 | 1383900788.167039 | q02       | Agent/1246 | CONNECT        |     2 | 1383901350.167967 |     2 |       |       |
            | 2013-11-08 10:04:19.485883 | 1383900788.167039 | q02       | Agent/1246 | COMPLETECALLER |     2 |               107 |     1 |       |       |
        Given I clear and generate the statistics cache
        Then I should have the following statististics on "q01" on "2013-11-08" on configuration "testq1":
          |         | Received | Answered |
          | 9h-10h  |        1 |        1 |
          | 10h-11h |        0 |        0 |
          | Total   |        1 |        1 |
        Then I should have the following statististics on "q02" on "2013-11-08" on configuration "testq2":
          |         | Received | Answered |
          | 9h-10h  |        0 |        0 |
          | 10h-11h |        1 |        1 |
          | Total   |        1 |        1 |

    Scenario: Generate stats for received/abandoned calls
        Given there is no entries in queue_log between "2012-07-01 08:00:00" and "2012-07-01 11:59:59"
        Given there are queues with infos:
            | name | number | context     |
            | q01  | 5001   | statscenter |
        Given there is a statistic configuration "test" from "8:00" to "12:00" with queue "q01"
        Given I have the following queue_log entries:
          | time                       | callid     | queuename | agent | event      | data1 | data2 | data3 | data4 | data5 |
          | 2012-07-01 08:00:00.000000 | received_1 | q01       | NONE  | ENTERQUEUE |       |       |       |       |       |
          | 2012-07-01 08:10:00.000000 | received_1 | q01       | NONE  | ABANDON    | 1     | 1     | 4     |       |       |
          | 2012-07-01 08:00:00.000001 | received_6 | q01       | NONE  | ENTERQUEUE |       |       |       |       |       |
          | 2012-07-01 08:11:00.000001 | received_6 | q01       | NONE  | ABANDON    | 2     | 3     | 5     |       |       |
          | 2012-07-01 08:00:00.000001 | received_3 | q02       | NONE  | ENTERQUEUE |       |       |       |       |       |
          | 2012-07-01 08:11:00.000001 | received_3 | q02       | NONE  | ABANDON    | 1     | 1     | 3     |       |       |
          | 2012-07-01 08:59:59.999999 | received_2 | q01       | NONE  | ENTERQUEUE |       |       |       |       |       |
          | 2012-07-01 09:59:59.999999 | received_2 | q01       | NONE  | ABANDON    | 2     | 2     | 2     |       |       |
          | 2012-07-01 09:00:00.000000 | received_4 | q01       | NONE  | ENTERQUEUE |       |       |       |       |       |
          | 2012-07-01 09:10:00.000000 | received_4 | q01       | NONE  | ABANDON    | 4     | 3     | 4     |       |       |
          | 2012-07-01 09:59:59.999999 | received_5 | q01       | NONE  | ENTERQUEUE |       |       |       |       |       |
          | 2012-07-01 10:59:59.999999 | received_5 | q01       | NONE  | ABANDON    | 1     | 4     | 2     |       |       |
        Given I clear and generate the statistics cache
        Then I should have the following statististics on "q01" on "2012-07-01" on configuration "test":
          |         | Received  | Abandoned | AWT      | Answered rate | QoS   |
          | 8h-9h   |         3 |         3 | 00:00:03 |           0 % |       |
          | 9h-10h  |         2 |         2 | 00:00:03 |           0 % |       |
          | 10h-11h |         0 |         0 |          |               |       |
          | 11h-12h |         0 |         0 |          |               |       |
          | Total   |         5 |         5 | 00:00:03 |           0 % |       |


    Scenario: Generate stats for received/answered calls
        Given there is no entries in queue_log between "2012-07-01 08:00:00" and "2012-07-01 11:59:59"
        Given there are queues with infos:
            | name | number | context     |
            | q01  | 5001   | statscenter |
        Given there is a statistic configuration "test" from "8:00" to "12:00" with queue "q01"
        Given I have the following queue_log entries:
          | time                       | callid     | queuename | agent     | event          | data1 | data2 | data3 | data4 | data5 |
          | 2012-07-01 08:00:00.000000 | received_1 | q01       | NONE      | ENTERQUEUE     |       |       |       |       |       |
          | 2012-07-01 08:00:03.000000 | received_1 | q01       | Agent/001 | CONNECT        | 3     |       |       |       |       |
          | 2012-07-01 08:00:06.000000 | received_1 | q01       | Agent/001 | COMPLETECALLER | 3     | 6     | 1     |       |       |
          | 2012-07-01 08:00:00.000001 | received_6 | q01       | NONE      | ENTERQUEUE     |       |       |       |       |       |
          | 2012-07-01 08:00:03.000001 | received_6 | q01       | Agent/001 | CONNECT        | 3     |       |       |       |       |
          | 2012-07-01 08:00:06.000001 | received_6 | q01       | Agent/001 | COMPLETEAGENT  | 3     | 6     | 1     |       |       |
          | 2012-07-01 08:00:00.000001 | received_3 | q02       | NONE      | ENTERQUEUE     |       |       |       |       |       |
          | 2012-07-01 08:00:03.000001 | received_3 | q02       | Agent/002 | CONNECT        | 3     |       |       |       |       |
          | 2012-07-01 08:00:06.000001 | received_3 | q02       | Agent/002 | COMPLETEAGENT  | 3     | 6     | 1     |       |       |
          | 2012-07-01 08:59:59.999999 | received_2 | q01       | NONE      | ENTERQUEUE     |       |       |       |       |       |
          | 2012-07-01 08:00:02.999999 | received_2 | q01       | Agent/001 | CONNECT        | 3     |       |       |       |       |
          | 2012-07-01 08:00:05.999999 | received_2 | q01       | Agent/001 | COMPLETEAGENT  | 3     | 5     | 1     |       |       |
          | 2012-07-01 09:00:00.000000 | received_4 | q01       | NONE      | ENTERQUEUE     |       |       |       |       |       |
          | 2012-07-01 08:00:03.000000 | received_4 | q01       | Agent/001 | CONNECT        | 3     |       |       |       |       |
          | 2012-07-01 08:00:06.000000 | received_4 | q01       | Agent/001 | COMPLETEAGENT  | 3     | 4     | 1     |       |       |
          | 2012-07-01 09:59:59.999999 | received_5 | q01       | NONE      | ENTERQUEUE     |       |       |       |       |       |
          | 2012-07-01 08:00:02.999999 | received_5 | q01       | Agent/001 | CONNECT        | 3     |       |       |       |       |
          | 2012-07-01 08:00:05.999999 | received_5 | q01       | Agent/001 | COMPLETECALLER | 3     | 7     | 1     |       |       |
        Given I clear and generate the statistics cache
        Then I should have the following statististics on "q01" on "2012-07-01" on configuration "test":
          |         | Received  | Answered  | AWT      | Answered rate | QoS   |
          | 8h-9h   |         3 |         3 | 00:00:03 |         100 % | 100 % |
          | 9h-10h  |         2 |         2 | 00:00:03 |         100 % | 100 % |
          | 10h-11h |         0 |         0 |          |               |       |
          | 11h-12h |         0 |         0 |          |               |       |
          | Total   |         5 |         5 | 00:00:03 |         100 % | 100 % |


    Scenario: Generate stats for received/blocking calls
        Given there is no entries in queue_log between "2012-07-01 08:00:00" and "2012-07-01 11:59:59"
        Given there are queues with infos:
            | name | number | context     |
            | q01  | 5001   | statscenter |
        Given there is a statistic configuration "test" from "8:00" to "12:00" with queue "q01"
        Given I have the following queue_log entries:
          | time                       | callid     | queuename | agent | event      | data1 | data2 | data3 | data4 | data5 |
          | 2012-07-01 08:00:00.000000 | received_1 | q01       | NONE  | JOINEMPTY  |       |       |       |       |       |
          | 2012-07-01 08:00:00.000001 | received_6 | q01       | NONE  | JOINEMPTY  |       |       |       |       |       |
          | 2012-07-01 08:00:00.000001 | received_3 | q02       | NONE  | JOINEMPTY  |       |       |       |       |       |
          | 2012-07-01 08:59:59.999999 | received_2 | q01       | NONE  | JOINEMPTY  |       |       |       |       |       |
          | 2012-07-01 09:00:00.000000 | received_4 | q01       | NONE  | JOINEMPTY  |       |       |       |       |       |
          | 2012-07-01 09:59:59.999999 | received_5 | q01       | NONE  | JOINEMPTY  |       |       |       |       |       |
        Given I clear and generate the statistics cache
        Then I should have the following statististics on "q01" on "2012-07-01" on configuration "test":
          |         | Received  | Blocking  |
          | 8h-9h   |         3 |         3 |
          | 9h-10h  |         2 |         2 |
          | 10h-11h |         0 |         0 |
          | 11h-12h |         0 |         0 |
          | Total   |         5 |         5 |


    Scenario: Generate stats for closed queue
        Given there is no entries in queue_log between "2012-07-01 08:00:00" and "2012-07-01 11:59:59"
        Given there are queues with infos:
            | name | number | context     |
            | q01  | 5001   | statscenter |
        Given there is a statistic configuration "test" from "8:00" to "12:00" with queue "q01"
        Given I have the following queue_log entries:
          | time                       | callid     | queuename | agent | event   | data1 | data2 | data3 | data4 | data5 |
          | 2012-07-01 08:00:00.000000 | received_1 | q01       | NONE  | CLOSED  |       |       |       |       |       |
          | 2012-07-01 08:00:00.000001 | received_6 | q01       | NONE  | CLOSED  |       |       |       |       |       |
          | 2012-07-01 08:00:00.000001 | received_3 | q02       | NONE  | CLOSED  |       |       |       |       |       |
          | 2012-07-01 08:59:59.999999 | received_2 | q01       | NONE  | CLOSED  |       |       |       |       |       |
          | 2012-07-01 09:00:00.000000 | received_4 | q01       | NONE  | CLOSED  |       |       |       |       |       |
          | 2012-07-01 09:59:59.999999 | received_5 | q01       | NONE  | CLOSED  |       |       |       |       |       |
        Given I clear and generate the statistics cache
        Then I should have the following statististics on "q01" on "2012-07-01" on configuration "test":
          |         | Received  | Closed  |
          | 8h-9h   |         3 |       3 |
          | 9h-10h  |         2 |       2 |
          | 10h-11h |         0 |       0 |
          | 11h-12h |         0 |       0 |
          | Total   |         5 |       5 |


    Scenario: Generate stats for saturated calls
        Given there is no entries in queue_log between "2012-07-01 08:00:00" and "2012-07-01 11:59:59"
        Given there are queues with infos:
            | name | number | context     |
            | q01  | 5001   | statscenter |
        Given there is a statistic configuration "test" from "8:00" to "12:00" with queue "q01"
        Given I have the following queue_log entries:
          | time                       | callid      | queuename | agent | event           | data1 | data2 | data3 | data4 | data5 |
          | 2012-07-01 08:00:00.000000 | saturated_1 | q01       | NONE  | DIVERT_CA_RATIO |       |       |       |       |       |
          | 2012-07-01 08:59:59.999999 | saturated_2 | q01       | NONE  | FULL            |       |       |       |       |       |
          | 2012-07-01 08:00:00.000001 | saturated_3 | q02       | NONE  | FULL            |       |       |       |       |       |
          | 2012-07-01 09:00:00.000000 | saturated_4 | q01       | NONE  | DIVERT_CA_RATIO |       |       |       |       |       |
          | 2012-07-01 09:59:59.999999 | saturated_5 | q01       | NONE  | DIVERT_HOLDTIME |       |       |       |       |       |
          | 2012-07-01 08:00:00.000001 | saturated_6 | q01       | NONE  | DIVERT_HOLDTIME |       |       |       |       |       |
        Given I clear and generate the statistics cache
        Then I should have the following statististics on "q01" on "2012-07-01" on configuration "test":
          |         | Received  | Saturated |
          | 8h-9h   |         3 |         3 |
          | 9h-10h  |         2 |         2 |
          | 10h-11h |         0 |         0 |
          | 11h-12h |         0 |         0 |
          | Total   |         5 |         5 |


    Scenario: Generate stats for answered rate with calls on closed queue
        Given there is no entries in queue_log between "2012-07-01 08:00:00" and "2012-07-01 11:59:59"
        Given there are queues with infos:
            | name | number | context     |
            | q01  | 5001   | statscenter |
        Given there is a statistic configuration "test" from "8:00" to "12:00" with queue "q01"
        Given I have the following queue_log entries:
          | time                       | callid        | queuename | agent | event         | data1 | data2         | data3 | data4 | data5 |
          | 2012-07-01 11:02:29.141759 | 1394463745.0  | q01       | NONE  | ENTERQUEUE    |       | 1003          | 1     |       |       |
          | 2012-07-01 11:02:51.940581 | MANAGER       | q01       | NONE  | ADDMEMBER     |       |               |       |       |       |
          | 2012-07-01 11:03:00.781150 | 1394463745.0  | q01       | NONE  | CONNECT       | 32    | 1394463774.2  | 6     |       |       |
          | 2012-07-01 11:03:02.973847 | 1394463745.0  | q01       | NONE  | COMPLETEAGENT | 32    | 2             | 1     |       |       |
          | 2012-07-01 11:03:05.774385 | 1394463784.6  | q01       | NONE  | ENTERQUEUE    |       | 1003          | 1     |       |       |
          | 2012-07-01 11:03:06.651541 | 1394463784.6  | q01       | NONE  | CONNECT       | 1     | 1394463785.7  | 0     |       |       |
          | 2012-07-01 11:03:08.573800 | 1394463784.6  | q01       | NONE  | COMPLETEAGENT | 1     | 2             | 1     |       |       |
          | 2012-07-01 11:03:17.222916 | 1394463795.10 | q01       | NONE  | ENTERQUEUE    |       | 1003          | 1     |       |       |
          | 2012-07-01 11:03:18.517792 | 1394463795.10 | q01       | NONE  | ABANDON       | 1     | 1             | 1     |       |       |
          | 2012-07-01 11:03:20.875825 | 1394463799.14 | q01       | NONE  | ENTERQUEUE    |       | 1003          | 1     |       |       |
          | 2012-07-01 11:03:21.528519 | 1394463799.14 | q01       | NONE  | ABANDON       | 1     | 1             | 1     |       |       |
          | 2012-07-01 11:34:11.154600 | 1394465650.18 | q01       | NONE  | CLOSED        |       |               |       |       |       |
          | 2012-07-01 11:39:16.945240 | 1394465954.19 | q01       | NONE  | ENTERQUEUE    |       | 1003          | 1     |       |       |
          | 2012-07-01 11:39:18.917060 | 1394465954.19 | q01       | NONE  | CONNECT       | 2     | 1394465957.20 | 1     |       |       |
          | 2012-07-01 11:39:20.227727 | 1394465954.19 | q01       | NONE  | COMPLETEAGENT | 3     | 1             | 1     |       |       |
          | 2012-07-01 11:42:52.852573 | 1394466171.23 | q01       | NONE  | ENTERQUEUE    |       | 1003          | 1     |       |       |
          | 2012-07-01 11:42:54.248786 | 1394466171.23 | q01       | NONE  | CONNECT       | 2     | 1394466172.24 | 1     |       |       |
          | 2012-07-01 11:42:55.780864 | 1394466171.23 | q01       | NONE  | COMPLETEAGENT | 2     | 1             | 1     |       |       |
          | 2012-07-01 11:42:58.788076 | 1394466177.27 | q01       | NONE  | ENTERQUEUE    |       | 1003          | 1     |       |       |
          | 2012-07-01 11:42:59.754986 | 1394466177.27 | q01       | NONE  | ABANDON       | 1     | 1             | 1     |       |       |
          | 2012-07-01 11:43:02.353859 | 1394466181.31 | q01       | NONE  | ENTERQUEUE    |       | 1003          | 1     |       |       |
          | 2012-07-01 11:43:17.360803 | 1394466181.31 | q01       | NONE  | RINGNOANSWER  | 15000 |               |       |       |       |
          | 2012-07-01 11:43:37.575660 | 1394466181.31 | q01       | NONE  | RINGNOANSWER  | 15000 |               |       |       |       |
          | 2012-07-01 11:43:40.247292 | 1394466181.31 | q01       | NONE  | ABANDON       | 1     | 1             | 38    |       |       |
        Given I clear and generate the statistics cache
        Then I should have the following statististics on "q01" on "2012-07-01" on configuration "test":
          |         | Received | Answered | Closed | Answered rate |
          | 8h-9h   | 0        | 0        | 0      |               |
          | 9h-10h  | 0        | 0        | 0      |               |
          | 10h-11h | 0        | 0        | 0      |               |
          | 11h-12h | 9        | 4        | 1      | 50 %          |
          | Total   | 9        | 4        | 1      | 50 %          |

    Scenario: Answered rate when all calls are closed should be empty
        Given there is no entries in queue_log between "2012-07-01 08:00:00" and "2012-07-01 11:59:59"
        Given there are queues with infos:
            | name | number | context     |
            | q01  | 5001   | statscenter |
        Given there is a statistic configuration "test" from "8:00" to "12:00" with queue "q01"
        Given I have the following queue_log entries:
          | time                       | callid        | queuename | agent | event         | data1 | data2         | data3 | data4 | data5 |
          | 2012-07-01 11:34:11.154600 | 1394465650.18 | q01       | NONE  | CLOSED        |       |               |       |       |       |
        Given I clear and generate the statistics cache
        Then I should have the following statististics on "q01" on "2012-07-01" on configuration "test":
          |         | Received | Answered | Closed | Answered rate |
          | 8h-9h   |        0 |        0 |      0 |               |
          | 9h-10h  |        0 |        0 |      0 |               |
          | 10h-11h |        0 |        0 |      0 |               |
          | 11h-12h |        1 |        0 |      1 |               |
          | Total   |        1 |        0 |      1 |               |
