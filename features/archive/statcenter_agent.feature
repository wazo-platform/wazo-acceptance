# Should be in xivo-stat integration tests
Feature: WEBI Agent Stats

    Scenario: Generate stats for answered calls
        Given there is no entries in queue_log between "2012-07-01 08:00:00" and "2012-07-01 11:59:59"
        Given there are queues with infos:
           | name | number | context     |
           | q01  | 5001   | statscenter |
        Given there is a agent "Agent" "1" with number "1"
        Given there is a statistic configuration "test" from "8:00" to "12:00" with queue "q01" and agent "1"
        Given I have the following queue_log entries:
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
        Then I should have the following statistics on agent "1" on "2012-07-01" on configuration "test":
          |         | Answered |
          | 8h-9h   |        1 |
          | 9h-10h  |        1 |
          | 10h-11h |        1 |
          | 11h-12h |        0 |
          | Total   |        3 |


    Scenario: Generate stats for total conversation time
        Given there is no entries in queue_log between "2012-01-01 08:00:00" and "2012-01-01 11:59:59"
        Given there are queues with infos:
           | name | number | context     |
           | q02  | 5002   | statscenter |
        Given there is a agent "Agent" "2" with number "2"
        Given there is a statistic configuration "test_talktime" from "8:00" to "12:00" with queue "q02" and agent "2"
        Given I have the following queue_log entries:
          | time                       | callid      | queuename | agent    | event            | data1  | data2        | data3   | data4 | data5  |
          | 2012-01-01 09:01:06.555555 | talk_time_1 | q02       | Agent/2  | ENTERQUEUE       |        |              |         |       |        |
          | 2012-01-01 09:01:06.666666 | talk_time_1 | q02       | Agent/2  | CONNECT          | 4      | 123456.435   |         |       |        |
          | 2012-01-01 09:01:10.777777 | talk_time_1 | q02       | Agent/2  | COMPLETEAGENT    | 4      | 10           |         |       |        |
          | 2012-01-01 09:02:06.555555 | talk_time_2 | q02       | Agent/2  | ENTERQUEUE       |        |              |         |       |        |
          | 2012-01-01 09:02:06.666666 | talk_time_2 | q02       | Agent/2  | CONNECT          | 5      | 12334234.435 |         |       |        |
          | 2012-01-01 09:02:10.777777 | talk_time_2 | q02       | Agent/2  | COMPLETECALLER   | 4      | 10           |         |       |        |
          | 2012-01-01 09:03:06.555555 | talk_time_3 | q02       | Agent/2  | ENTERQUEUE       |        |              |         |       |        |
          | 2012-01-01 09:03:06.666666 | talk_time_3 | q02       | Agent/2  | CONNECT          | 6      | 2222456.435  |         |       |        |
          | 2012-01-01 09:03:10.777777 | talk_time_3 | q02       | Agent/2  | TRANSFER         | 1001   | default      | 0       | 10    |        |
          | 2012-01-01 09:04:06.555555 | talk_time_4 | q02       | Agent/2  | ENTERQUEUE       |        |              |         |       |        |
          | 2012-01-01 09:04:06.666666 | talk_time_4 | q02       | Agent/2  | CONNECT          | 6      | 3222456.435  |         |       |        |
          | 2012-01-01 09:04:10.777777 | talk_time_4 | q02       | Agent/2  | BLINDTRANSFER    | 1001   | default      | 0       | 10    |        |
          | 2012-01-01 09:05:06.555555 | talk_time_5 | q02       | Agent/2  | ENTERQUEUE       |        |              |         |       |        |
          | 2012-01-01 09:05:06.666666 | talk_time_5 | q02       | Agent/2  | CONNECT          | 6      | 3222456.435  |         |       |        |
          | 2012-01-01 09:05:10.777777 | talk_time_5 | q02       | Agent/2  | ATTENDEDTRANSFER | BRIDGE | foobar       | 0       | 10    |        |
          | 2012-01-01 09:06:06.555555 | talk_time_6 | q02       | Agent/2  | ENTERQUEUE       |        |              |         |       |        |
          | 2012-01-01 09:06:06.666666 | talk_time_6 | q02       | Agent/2  | CONNECT          | 6      | 3222456.435  |         |       |        |
          | 2012-01-01 09:06:10.777777 | talk_time_6 | q02       | Agent/2  | ATTENDEDTRANSFER | LINK   | SIP/a-1      | SIP/b-2 | 0     | 10\|1  |

        Given I clear and generate the statistics cache
        Then I should have the following statistics on agent "2" on "2012-01-01" on configuration "test_talktime":
          |         | Answered | Conversation |
          | 8h-9h   |        0 |     00:00:00 |
          | 9h-10h  |        6 |     00:01:00 |
          | 10h-11h |        0 |     00:00:00 |
          | 11h-12h |        0 |     00:00:00 |
          | Total   |        6 |     00:01:00 |


    Scenario: Generate stats for total login time
        Given there is no entries in queue_log between "2012-01-01 08:00:00" and "2012-01-01 11:59:59"
        Given there is a agent "Agent" "3" with number "3"
        Given there is a statistic configuration "test_login_time_1" from "8:00" to "12:00" with agent "3"
        Given I have the following queue_log entries:
          | time                       | callid       | queuename | agent   | event               | data1            | data2 | data3         | data4 | data5 |
          | 2012-01-01 09:10:10.777777 | login_time_1 | NONE      | Agent/3 | AGENTCALLBACKLOGIN  | 1001@statscenter |       |               |       |       |
          | 2012-01-01 09:25:10.777777 | login_time_2 | NONE      | Agent/3 | AGENTCALLBACKLOGOFF | 1001@statscenter |   900 | CommandLogoff |       |       |
          | 2012-01-01 09:25:11.555555 | login_time_3 | NONE      | Agent/3 | UNPAUSEALL          |                  |       |               |       |       |

        Given I clear and generate the statistics cache
        Then I should have the following statistics on agent "3" on "2012-01-01" on configuration "test_login_time_1":
          |         | Login    |
          | 8h-9h   | 00:00:00 |
          | 9h-10h  | 00:15:00 |
          | 10h-11h | 00:00:00 |
          | 11h-12h | 00:00:00 |
          | Total   | 00:15:00 |


    Scenario: Two login session during the same hour
        Given there is no entries in queue_log between "2012-01-01 08:00:00" and "2012-01-01 11:59:59"
        Given there is a agent "Agent" "4" with number "4"
        Given there is a statistic configuration "test_login_time_2" from "8:00" to "12:00" with agent "4"
        Given I have the following queue_log entries:
          | time                       | callid       | queuename | agent   | event               | data1              | data2 | data3         | data4 | data5 |
          | 2012-01-01 09:01:00.000000 | login_time_1 | NONE      | Agent/4 | AGENTCALLBACKLOGIN  | 1003@default       |       |               |       |       |
          | 2012-01-01 09:01:06.000000 | login_time_2 | NONE      | Agent/4 | AGENTCALLBACKLOGOFF | 1003@default       |     6 | CommandLogoff |       |       |
          | 2012-01-01 09:02:00.000000 | login_time_3 | NONE      | Agent/4 | AGENTLOGIN          | SIP/aaaaa-00000001 |       |               |       |       |
          | 2012-01-01 09:02:30.000000 | login_time_3 | NONE      | Agent/4 | AGENTLOGOFF         | SIP/aaaaa-00000001 |    30 | CommandLogoff |       |       |
          | 2012-01-01 09:50:00.000000 | login_time_4 | NONE      | Agent/4 | AGENTCALLBACKLOGIN  | 1003@default       |       |               |       |       |

        Given I clear and generate the statistics cache
        Then I should have the following statistics on agent "4" on "2012-01-01" on configuration "test_login_time_2":
          |         |    Login |
          | 8h-9h   | 00:00:00 |
          | 9h-10h  | 00:10:36 |
          | 10h-11h | 01:00:00 |
          | 11h-12h | 01:00:00 |
          | Total   | 02:10:36 |


    Scenario: Login before the hour logout during the hour
        Given there is no entries in queue_log between "2012-01-01 08:00:00" and "2012-01-01 11:59:59"
        Given there is a agent "Agent" "5" with number "5"
        Given there is a statistic configuration "test_login_time_3" from "8:00" to "12:00" with agent "5"
        Given I have the following queue_log entries:
          | time                       | callid       | queuename | agent   | event               | data1              | data2 | data3         | data4 | data5 |
          | 2012-01-01 08:50:00.999999 | login_time_1 | NONE      | Agent/5 | AGENTCALLBACKLOGIN  | 1003@default       |       |               |       |       |
          | 2012-01-01 09:01:06.000000 | login_time_2 | NONE      | Agent/5 | AGENTCALLBACKLOGOFF | 1003@default       |   665 | CommandLogoff |       |       |
          | 2012-01-01 09:02:00.000000 | login_time_3 | NONE      | Agent/5 | AGENTLOGIN          | SIP/aaaaa-00000001 |       |               |       |       |
          | 2012-01-01 09:02:30.000000 | login_time_3 | NONE      | Agent/5 | AGENTLOGOFF         | SIP/aaaaa-00000001 |    30 | CommandLogoff |       |       |

        Given I clear and generate the statistics cache
        Then I should have the following statistics on agent "5" on "2012-01-01" on configuration "test_login_time_3":
          |         |    Login |
          | 8h-9h   | 00:09:59 |
          | 9h-10h  | 00:01:36 |
          | 10h-11h | 00:00:00 |
          | 11h-12h | 00:00:00 |
          | Total   | 00:11:35 |

    Scenario: Implicit login before the hour then logout exactly at the hour
        Given there is no entries in queue_log between "2012-01-02 07:00:00" and "2012-01-02 09:00:00"
        Given there is a agent "Agent" "5" with number "5"
        Given there is a statistic configuration "test_logout_time" from "08:00" to "09:00" with agent "5"
        Given I have the following queue_log entries:
          | time                       | callid       | queuename | agent   | event               | data1              | data2 | data3         | data4 | data5 |
          | 2012-01-02 08:00:00.000000 | login_time_1 | NONE      | Agent/5 | AGENTCALLBACKLOGOFF | 1003@default       | 300   | CommandLogoff |       |       |
          | 2012-01-02 08:00:00.000000 | login_time_2 | NONE      | Agent/5 | AGENTLOGOFF         | SIP/aaaaa-00000001 | 30    | CommandLogoff |       |       |
        Given I generate the statistics cache from start time "2012-01-02T08:00:00" to end time "2012-01-02T09:00:00"
        Then I should have the following statistics on agent "5" on "2012-01-02" on configuration "test_logout_time":
          |         |    Login |
          | 8h-9h   | 00:00:00 |
          | Total   | 00:00:00 |

    Scenario: Implicit login then logoff after the hour
        Given there is no entries in queue_log between "2012-01-02 07:00:00" and "2012-01-02 10:00:00"
        Given there is a agent "Agent" "5" with number "5"
        Given there is a statistic configuration "test_logout_time" from "08:00" to "09:00" with agent "5"
        Given I have the following queue_log entries:
        | time                       | callid       | queuename | agent   | event               | data1              | data2 | data3         | data4 | data5 |
        | 2012-01-02 10:00:00.000000 | login_time_1 | NONE      | Agent/5 | AGENTCALLBACKLOGOFF | 1003@default       | 300   | CommandLogoff |       |       |
        | 2012-01-02 10:00:00.000000 | login_time_2 | NONE      | Agent/5 | AGENTLOGOFF         | SIP/aaaaa-00000001 | 30    | CommandLogoff |       |       |
        Given I generate the statistics cache from start time "2012-01-02T08:00:00" to end time "2012-01-02T09:00:00"
        Then I should have the following statistics on agent "5" on "2012-01-02" on configuration "test_logout_time":
          |         |    Login |
          | 8h-9h   | 00:00:00 |
          | Total   | 00:00:00 |

    Scenario: Login after the hour with no logout
        Given there is no entries in queue_log between "2012-01-02 07:00:00" and "2012-01-02 10:00:00"
        Given there is a agent "Agent" "5" with number "5"
        Given there is a statistic configuration "test_logout_time" from "08:00" to "09:00" with agent "5"
        Given I have the following queue_log entries:
          | time                       | callid       | queuename | agent   | event               | data1              | data2  | data3         | data4 | data5 |
          | 2012-01-02 09:50:00.999999 | login_time_1 | NONE      | Agent/5 | AGENTCALLBACKLOGIN  | 1003@default       |        |               |       |       |
          | 2012-01-02 09:51:00.000000 | login_time_3 | NONE      | Agent/5 | AGENTLOGIN          | SIP/aaaaa-00000001 |        |               |       |       |
        Given I generate the statistics cache from start time "2012-01-02T08:00:00" to end time "2012-01-02T09:00:00"
        Then I should have the following statistics on agent "5" on "2012-01-02" on configuration "test_logout_time":
          |         |    Login |
          | 8h-9h   | 00:00:00 |
          | Total   | 00:00:00 |

    Scenario: Login and logoff during the hour and login after the hour
        Given there is no entries in queue_log between "2012-01-02 07:00:00" and "2012-01-02 10:00:00"
        Given there is a agent "Agent" "5" with number "5"
        Given there is a statistic configuration "test_logout_time" from "08:00" to "09:00" with agent "5"
        Given I have the following queue_log entries:
          | time                       | callid       | queuename | agent   | event               | data1              | data2 | data3         | data4 | data5 |
          | 2012-01-02 08:30:00.000000 | login_time_1 | NONE      | Agent/5 | AGENTCALLBACKLOGIN  | 1003@default       |       |               |       |       |
          | 2012-01-02 08:35:00.000000 | login_time_2 | NONE      | Agent/5 | AGENTCALLBACKLOGOFF | 1003@default       | 300   | CommandLogoff |       |       |
          | 2012-01-02 08:40:00.000000 | login_time_3 | NONE      | Agent/5 | AGENTLOGIN          | SIP/aaaaa-00000001 |       |               |       |       |
          | 2012-01-02 08:45:00.000000 | login_time_3 | NONE      | Agent/5 | AGENTLOGOFF         | SIP/aaaaa-00000001 | 300   | CommandLogoff |       |       |
          | 2012-01-02 09:30:00.000000 | login_time_1 | NONE      | Agent/5 | AGENTCALLBACKLOGIN  | 1003@default       |       |               |       |       |
          | 2012-01-02 09:40:00.000000 | login_time_3 | NONE      | Agent/5 | AGENTLOGIN          | SIP/aaaaa-00000001 |       |               |       |       |
        Given I generate the statistics cache from start time "2012-01-02T08:00:00" to end time "2012-01-02T09:00:00"
        Then I should have the following statistics on agent "5" on "2012-01-02" on configuration "test_logout_time":
          |         |    Login |
          | 8h-9h   | 00:10:00 |
          | Total   | 00:10:00 |

    Scenario: Login before the day logout after the day
        Given there is no entries in queue_log between "2012-01-01 08:00:00" and "2012-01-03 23:59:59"
        Given there is a agent "Agent" "6" with number "6"
        Given there is a statistic configuration "test_login_time_4" from "8:00" to "12:00" with agent "6"
        Given I have the following queue_log entries:
          | time                       | callid       | queuename | agent   | event               | data1              |  data2 | data3         | data4 | data5 |
          | 2012-01-01 08:50:00.999999 | login_time_1 | NONE      | Agent/6 | AGENTCALLBACKLOGIN  | 1003@default       |        |               |       |       |
          | 2012-01-03 09:01:06.000000 | login_time_2 | NONE      | Agent/6 | AGENTCALLBACKLOGOFF | 1003@default       | 173941 | CommandLogoff |       |       |
          | 2012-01-03 09:02:00.000000 | login_time_3 | NONE      | Agent/6 | AGENTLOGIN          | SIP/aaaaa-00000001 |        |               |       |       |
          | 2012-01-03 09:02:30.000000 | login_time_3 | NONE      | Agent/6 | AGENTLOGOFF         | SIP/aaaaa-00000001 |     30 | CommandLogoff |       |       |

        Given I clear and generate the statistics cache
        Then I should have the following statistics on agent "6" on "2012-01-02" on configuration "test_login_time_4":
          |         |    Login |
          | 8h-9h   | 01:00:00 |
          | 9h-10h  | 01:00:00 |
          | 10h-11h | 01:00:00 |
          | 11h-12h | 01:00:00 |
          | Total   | 04:00:00 |


    Scenario: Generate stats twice
        Given there is no entries in queue_log in the last hour
        Given there is a agent "Agent" "8" with number "8"
        Given there is a statistic configuration "test_login_time_6" from "00:00" to "24:00" with agent "8"
        Given I have the following queue_log entries in the last hour:
          | time         | callid       | queuename | agent   | event               | data1            | data2 | data3         | data4 | data5 |
          | 10:10.777777 | login_time_1 | NONE      | Agent/8 | AGENTCALLBACKLOGIN  | 1002@statscenter |       |               |       |       |
          | 25:10.777777 | login_time_2 | NONE      | Agent/8 | AGENTCALLBACKLOGOFF | 1002@statscenter |   900 | CommandLogoff |       |       |
          | 25:11.555555 | login_time_3 | NONE      | Agent/8 | UNPAUSEALL          |                  |       |               |       |       |

        Given I clear and generate the statistics cache twice
        Then I should have "00:15:00" minutes login in the last hour on agent "8" on configuration "test_login_time_6":


    Scenario: Login during the hour logout after the hour
        Given there is no entries in queue_log between "2012-01-01 08:00:00" and "2012-01-01 11:59:59"
        Given there is a agent "Agent" "9" with number "9"
        Given there is a statistic configuration "test_login_time_9" from "8:00" to "12:00" with agent "9"
        Given I have the following queue_log entries:
          | time                       | callid       | queuename | agent   | event               | data1              | data2 | data3         | data4 | data5 |
          | 2012-01-01 09:07:00.999999 | login_time_1 | NONE      | Agent/9 | AGENTCALLBACKLOGIN  | 1003@default       |       |               |       |       |
          | 2012-01-01 09:12:06.000000 | login_time_2 | NONE      | Agent/9 | AGENTCALLBACKLOGOFF | 1003@default       |   305 | CommandLogoff |       |       |
          | 2012-01-01 09:45:00.000000 | login_time_3 | NONE      | Agent/9 | AGENTLOGIN          | SIP/aaaaa-00000001 |       |               |       |       |
          | 2012-01-01 10:02:30.000000 | login_time_3 | NONE      | Agent/9 | AGENTLOGOFF         | SIP/aaaaa-00000001 |  1050 | CommandLogoff |       |       |

        Given I clear and generate the statistics cache
        Then I should have the following statistics on agent "9" on "2012-01-01" on configuration "test_login_time_9":
          |         |    Login |
          | 8h-9h   | 00:00:00 |
          | 9h-10h  | 00:20:05 |
          | 10h-11h | 00:02:30 |
          | 11h-12h | 00:00:00 |
          | Total   | 00:22:35 |


    Scenario: Generate stats for total pause time
        Given there is no entries in queue_log between "2012-01-01 08:00:00" and "2012-01-01 11:59:59"
        Given there is a agent "Agent" "10" with number "10"
        Given there is a statistic configuration "test_pause_time_1" from "8:00" to "12:00" with agent "10"
        Given I have the following queue_log entries:
          | time                       | callid | queuename | agent    | event      | data1 | data2 | data3 | data4 | data5 |
          | 2012-01-01 10:46:00.000000 | NONE   | NONE      | Agent/10 | UNPAUSEALL |       |       |       |       |       |
          | 2012-01-01 09:41:10.000000 | NONE   | NONE      | Agent/10 | PAUSEALL   |       |       |       |       |       |
          | 2012-01-01 08:54:09.000000 | NONE   | NONE      | Agent/10 | UNPAUSEALL |       |       |       |       |       |
          | 2012-01-01 08:50:59.000000 | NONE   | NONE      | Agent/10 | UNPAUSEALL |       |       |       |       |       |
          | 2012-01-01 08:50:46.000000 | NONE   | NONE      | Agent/10 | UNPAUSEALL |       |       |       |       |       |
          | 2012-01-01 08:48:45.000000 | NONE   | NONE      | Agent/10 | PAUSEALL   |       |       |       |       |       |
          | 2012-01-01 08:47:18.000000 | NONE   | NONE      | Agent/10 | PAUSEALL   |       |       |       |       |       |
          | 2012-01-01 08:47:17.000000 | NONE   | NONE      | Agent/10 | PAUSEALL   |       |       |       |       |       |
          | 2012-01-01 08:47:16.000000 | NONE   | NONE      | Agent/10 | PAUSEALL   |       |       |       |       |       |
          | 2012-01-01 08:46:38.000000 | NONE   | NONE      | Agent/10 | UNPAUSEALL |       |       |       |       |       |
          | 2012-01-01 08:41:30.000000 | NONE   | NONE      | Agent/10 | PAUSEALL   |       |       |       |       |       |
          | 2012-01-01 08:41:09.000000 | NONE   | NONE      | Agent/10 | UNPAUSEALL |       |       |       |       |       |

        Given I clear and generate the statistics cache
        Then I should have the following statistics on agent "10" on "2012-01-01" on configuration "test_pause_time_1":
          |         | Pause    |
          | 8h-9h   | 00:08:38 |
          | 9h-10h  | 00:18:50 |
          | 10h-11h | 00:46:00 |
          | 11h-12h | 00:00:00 |
          | Total   | 01:13:28 |


    Scenario: last Pause in QueueLog without Unpause
        Given there is no entries in queue_log between "2012-01-01 08:00:00" and "2012-01-01 11:59:59"
        Given there is a agent "Agent" "10" with number "10"
        Given there is a statistic configuration "test_pause_time_2" from "8:00" to "12:00" with agent "10"
        Given I have the following queue_log entries:
          | time                       | callid | queuename | agent    | event      | data1 | data2 | data3 | data4 | data5 |
          | 2012-01-01 09:41:10.000000 | NONE   | NONE      | Agent/10 | PAUSEALL   |       |       |       |       |       |
          | 2012-01-01 08:54:09.000000 | NONE   | NONE      | Agent/10 | UNPAUSEALL |       |       |       |       |       |
          | 2012-01-01 08:50:59.000000 | NONE   | NONE      | Agent/10 | UNPAUSEALL |       |       |       |       |       |
          | 2012-01-01 08:50:46.000000 | NONE   | NONE      | Agent/10 | UNPAUSEALL |       |       |       |       |       |
          | 2012-01-01 08:48:45.000000 | NONE   | NONE      | Agent/10 | PAUSEALL   |       |       |       |       |       |
          | 2012-01-01 08:47:18.000000 | NONE   | NONE      | Agent/10 | PAUSEALL   |       |       |       |       |       |
          | 2012-01-01 08:47:17.000000 | NONE   | NONE      | Agent/10 | PAUSEALL   |       |       |       |       |       |
          | 2012-01-01 08:47:16.000000 | NONE   | NONE      | Agent/10 | PAUSEALL   |       |       |       |       |       |
          | 2012-01-01 08:46:38.000000 | NONE   | NONE      | Agent/10 | UNPAUSEALL |       |       |       |       |       |
          | 2012-01-01 08:41:30.000000 | NONE   | NONE      | Agent/10 | PAUSEALL   |       |       |       |       |       |
          | 2012-01-01 08:41:09.000000 | NONE   | NONE      | Agent/10 | UNPAUSEALL |       |       |       |       |       |

        Given I clear and generate the statistics cache
        Then I should have the following statistics on agent "10" on "2012-01-01" on configuration "test_pause_time_2":
          |         | Pause    |
          | 8h-9h   | 00:08:38 |
          | 9h-10h  | 00:18:50 |
          | 10h-11h | 01:00:00 |
          | 11h-12h | 01:00:00 |
          | Total   | 02:27:28 |


    Scenario: Generate stats for total wrapup time
        Given there is no entries in queue_log between "2012-01-01 08:00:00" and "2012-01-01 11:59:59"
        Given there are queues with infos:
           | name | number | context     |
           | q11  | 5011   | statscenter |
        Given there is a agent "Agent" "11" with number "11"
        Given there is a statistic configuration "test_wrapup_time" from "8:00" to "12:00" with queue "q11" and agent "11"
        Given I have the following queue_log entries:
          | time                       | callid        | queuename | agent    | event         | data1 | data2         | data3 | data4 | data5 |
          | 2012-01-01 09:43:07.216260 | NONE          | NONE      | Agent/11 | WRAPUPSTART   | 15    |               |       |       |       |
          | 2012-01-01 09:43:07.213910 | wrapup_time_1 | q11       | Agent/11 | COMPLETEAGENT | 18    | 2             | 1     |       |       |
          | 2012-01-01 09:43:05.121034 | wrapup_time_1 | q11       | Agent/11 | CONNECT       | 18    | 1351078982.15 | 2     |       |       |
          | 2012-01-01 09:42:47.009661 | wrapup_time_1 | q11       | NONE     | ENTERQUEUE    |       | 1003          | 1     |       |       |
        Given I clear and generate the statistics cache
        Then I should have the following statistics on agent "11" on "2012-01-01" on configuration "test_wrapup_time":
          |         | Answered | Wrapup   |
          | 8h-9h   |        0 | 00:00:00 |
          | 9h-10h  |        1 | 00:00:15 |
          | 10h-11h |        0 | 00:00:00 |
          | 11h-12h |        0 | 00:00:00 |
          | Total   |        1 | 00:00:15 |


    Scenario: Generate stats for answered calls transfered by an agent to an another queue
        Given there is no entries in queue_log between "2013-11-08 08:00:00" and "2013-11-08 11:59:59"
        Given I clear the statistics cache
        Given there are queues with infos:
            | name | number | context     |
            | q12  | 5012   | statscenter |
            | q13  | 5013   | statscenter |
        Given there is a agent "Agent" "12" with number "12"
        Given there is a agent "Agent" "13" with number "13"
        Given there is a statistic configuration "test_agent_transfer_to_queue" from "8:00" to "12:00" with the following parameters:
            | queues  | agents |
            | q12,q13 | 12,13  |
        Given I have the following queue_log entries:
            |               time         |      callid       | queuename |   agent  |     event      | data1 |       data2       | data3 | data4 | data5 |
            | 2013-11-08 09:53:09.948070 | 1383900788.167039 | q12       | NONE     | ENTERQUEUE     |       | ##########        | 1     |       |       |
            | 2013-11-08 09:53:12.684547 | 1383900788.167039 | q12       | Agent/12 | CONNECT        | 3     | 1383900789.167040 | 2     |       |       |
            | 2013-11-08 10:02:30.219402 | 1383900788.167039 | q12       | Agent/12 | COMPLETECALLER | 3     | 558               | 1     |       |       |
            | 2013-11-08 10:02:30.569451 | 1383900788.167039 | q13       | NONE     | ENTERQUEUE     |       | ##########        | 1     |       |       |
            | 2013-11-08 10:02:32.770339 | 1383900788.167039 | q13       | Agent/13 | CONNECT        | 2     | 1383901350.167967 | 2     |       |       |
            | 2013-11-08 10:04:19.485883 | 1383900788.167039 | q13       | Agent/13 | COMPLETECALLER | 2     | 107               | 1     |       |       |
        Given I generate the statistics cache from start time "2013-11-08T10:00:00"

        Then I should have the following statistics on agent "12" on "2013-11-08" on configuration "test_agent_transfer_to_queue":
            |         | Answered |
            | 8h-9h   |        0 |
            | 9h-10h  |        1 |
            | 10h-11h |        0 |
            | 11h-12h |        0 |
            | Total   |        1 |

        Then I should have the following statistics on agent "13" on "2013-11-08" on configuration "test_agent_transfer_to_queue":
            |         | Answered |
            | 8h-9h   |        0 |
            | 9h-10h  |        0 |
            | 10h-11h |        1 |
            | 11h-12h |        0 |
            | Total   |        1 |

    Scenario: Agent login time in queue_log
        Given there is no agents logged
        Given there are users with infos:
        | firstname | lastname | number | context     | agent_number | protocol |
        | User      |      003 |   1003 | statscenter |         1003 | sip      |
        When I log agent "1003"
        When I wait 1 seconds
        When I unlog agent "1003"
        Then the queue_log table shows that agent "1003" has been logged for 1 seconds
