Feature: WEBI Agent Stats

    Scenario: Generate stats for answered calls
        Given there is no entries in queue_log between "2012-07-01 08:00:00" and "2012-07-01 11:59:59"
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
        Then I should have the following statististics on agent "1" on "2012-07-01" on configuration "test":
          |         | Answered |
          | 8h-9h   |        1 |
          | 9h-10h  |        1 |
          | 10h-11h |        1 |
          | 11h-12h |        0 |
          | Total   |        3 |


    Scenario: Generate stats for total conversation time
        Given there is no entries in queue_log between "2012-01-01 08:00:00" and "2012-01-01 11:59:59"
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
        Then I should have the following statististics on agent "2" on "2012-01-01" on configuration "test_talktime":
          |         | Answered | Conversation |
          | 8h-9h   |        0 |     00:00:00 |
          | 9h-10h  |        3 |     00:00:39 |
          | 10h-11h |        0 |     00:00:00 |
          | 11h-12h |        0 |     00:00:00 |
          | Total   |        3 |     00:00:39 |


    Scenario: Generate stats for total login time
        Given there is no entries in queue_log between "2012-01-01 08:00:00" and "2012-01-01 11:59:59"
        Given there is a agent "Agent" "3" with extension "3@statscenter"
        Given there is a statistic configuration "test_login_time_1" from "8:00" to "12:00" with agent "3"
        Given I have to following queue_log entries:
          | time                       | callid       | queuename | agent    | event               | data1            | data2 | data3         | data4 | data5 |
          | 2012-01-01 09:10:10.777777 | login_time_1 | NONE      | Agent/3  | AGENTCALLBACKLOGIN  | 1002@default     |       |               |       |       |
          | 2012-01-01 09:25:10.777777 | login_time_2 | NONE      | Agent/3  | AGENTCALLBACKLOGOFF | 1001@statscenter | 900   | CommandLogoff |       |       |
          | 2012-01-01 09:25:11.555555 | login_time_3 | NONE      | Agent/3  | UNPAUSEALL          |                  |       |               |       |       |
        Given I clear and generate the statistics cache
        Then I should have the following statististics on agent "3" on "2012-01-01" on configuration "test_login_time_1":
          |         | Login    |
          | 8h-9h   | 00:00:00 |
          | 9h-10h  | 00:15:00 |
          | 10h-11h | 00:00:00 |
          | 11h-12h | 00:00:00 |
          | Total   | 00:15:00 |

    Scenario: Two login session during the same hour
        Given there is no entries in queue_log between "2012-01-01 08:00:00" and "2012-01-01 11:59:59"
        Given there is a agent "Agent" "4" with extension "4@statscenter"
        Given there is a statistic configuration "test_login_time_2" from "8:00" to "12:00" with agent "4"
        Given I have to following queue_log entries:
          | time                       | callid       | queuename | agent   | event               | data1              | data2 | data3         | data4 | data5 |
          | 2012-01-01 09:01:00.000000 | login_time_1 | NONE      | Agent/4 | AGENTCALLBACKLOGIN  | 1003@default       |       |               |       |       |
          | 2012-01-01 09:01:06.000000 | login_time_2 | NONE      | Agent/4 | AGENTCALLBACKLOGOFF | 1003@default       |     6 | CommandLogoff |       |       |
          | 2012-01-01 09:02:00.000000 | login_time_3 | NONE      | Agent/4 | AGENTLOGIN          | SIP/aaaaa-00000001 |       |               |       |       |
          | 2012-01-01 09:02:30.000000 | login_time_3 | NONE      | Agent/4 | AGENTLOGOFF         | SIP/aaaaa-00000001 |    30 | CommandLogoff |       |       |
          | 2012-01-01 09:50:00.000000 | login_time_4 | NONE      | Agent/4 | AGENTCALLBACKLOGIN  | 1003@default       |       |               |       |       |

        Given I clear and generate the statistics cache
        Then I should have the following statististics on agent "4" on "2012-01-01" on configuration "test_login_time_2":
          |         |    Login |
          | 8h-9h   | 00:00:00 |
          | 9h-10h  | 00:10:36 |
          | 10h-11h | 01:00:00 |
          | 11h-12h | 01:00:00 |
          | Total   | 02:10:36 |


    Scenario: Login before the hour, logout during the hour
        Given there is no entries in queue_log between "2012-01-01 08:00:00" and "2012-01-01 11:59:59"
        Given there is a agent "Agent" "5" with extension "5@statscenter"
        Given there is a statistic configuration "test_login_time_3" from "8:00" to "12:00" with agent "5"
        Given I have to following queue_log entries:
          | time                       | callid       | queuename | agent   | event               | data1              | data2 | data3         | data4 | data5 |
          | 2012-01-01 08:50:00.999999 | login_time_1 | NONE      | Agent/5 | AGENTCALLBACKLOGIN  | 1003@default       |       |               |       |       |
          | 2012-01-01 09:01:06.000000 | login_time_2 | NONE      | Agent/5 | AGENTCALLBACKLOGOFF | 1003@default       |   666 | CommandLogoff |       |       |
          | 2012-01-01 09:02:00.000000 | login_time_3 | NONE      | Agent/5 | AGENTLOGIN          | SIP/aaaaa-00000001 |       |               |       |       |
          | 2012-01-01 09:02:30.000000 | login_time_3 | NONE      | Agent/5 | AGENTLOGOFF         | SIP/aaaaa-00000001 |    30 | CommandLogoff |       |       |

        Given I clear and generate the statistics cache
        Then I should have the following statististics on agent "5" on "2012-01-01" on configuration "test_login_time_3":
          |         |    Login |
          | 8h-9h   | 00:09:59 |
          | 9h-10h  | 00:01:36 |
          | 10h-11h | 00:00:00 |
          | 11h-12h | 00:00:00 |
          | Total   | 00:11:35 |


    Scenario: Login before the day, logout after the day
        Given there is no entries in queue_log between "2012-01-01 08:00:00" and "2012-01-03 23:59:59"
        Given there is a agent "Agent" "6" with extension "6@statscenter"
        Given there is a statistic configuration "test_login_time_4" from "8:00" to "12:00" with agent "6"
        Given I have to following queue_log entries:
          | time                       | callid       | queuename | agent   | event               | data1              | data2 | data3         | data4 | data5 |
          | 2012-01-01 08:50:00.999999 | login_time_1 | NONE      | Agent/6 | AGENTCALLBACKLOGIN  | 1003@default       |       |               |       |       |
          | 2012-01-03 09:01:06.000000 | login_time_2 | NONE      | Agent/6 | AGENTCALLBACKLOGOFF | 1003@default       |   666 | CommandLogoff |       |       |
          | 2012-01-03 09:02:00.000000 | login_time_3 | NONE      | Agent/6 | AGENTLOGIN          | SIP/aaaaa-00000001 |       |               |       |       |
          | 2012-01-03 09:02:30.000000 | login_time_3 | NONE      | Agent/6 | AGENTLOGOFF         | SIP/aaaaa-00000001 |    30 | CommandLogoff |       |       |

        Given I clear and generate the statistics cache
        Then I should have the following statististics on agent "6" on "2012-01-02" on configuration "test_login_time_4":
          |         |    Login |
          | 8h-9h   | 01:00:00 |
          | 9h-10h  | 01:00:00 |
          | 10h-11h | 01:00:00 |
          | 11h-12h | 01:00:00 |
          | Total   | 04:00:00 |


    Scenario: Agent implicitly logged in, because he answered calls
        Given there is a agent "Agent" "7" with extension "7@statscenter"
        Given there is a queue "q07" with extension "5007@statscenter"
        Given there is a statistic configuration "test_login_time_5" from "8:00" to "12:00" with queue "q07" and agent "7"
        Given there is no entries in queue_log between "2012-01-01 08:00:00" and "2012-01-01 23:59:59"
        Given there is no "AGENTCALLBACKLOGIN" entry for agent "7"
        Given there is no "AGENTLOGIN" entry for agent "7"
        Given I have to following queue_log entries:
          | time                       | callid       | queuename | agent   | event         | data1 |        data2 | data3 | data4 | data5 |
          | 2012-01-01 08:12:34.999999 | login_time_1 | q07       | NONE    | ENTERQUEUE    |       |       123456 |       |       |       |
          | 2012-01-01 08:13:34.999999 | login_time_1 | q07       | Agent/7 | CONNECT       |    60 | 1111111111.1 |     0 |       |       |
          | 2012-01-01 08:14:34.999999 | login_time_1 | q07       | Agent/7 | COMPLETEAGENT |    60 |           60 |     1 |       |       |
        Given I clear and generate the statistics cache
        Then I should have the following statististics on agent "7" on "2012-01-02" on configuration "test_login_time_5":
          |         |    Login |
          | 8h-9h   | 01:00:00 |
          | 9h-10h  | 01:00:00 |
          | 10h-11h | 01:00:00 |
          | 11h-12h | 01:00:00 |
          | Total   | 04:00:00 |
