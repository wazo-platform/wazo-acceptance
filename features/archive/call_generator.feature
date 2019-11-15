# Should be in xivo-call-logd integration tests
Feature: Call Log Generation

     Scenario: Generation for a specified latest CEL count with no processed calls
         Given there are no call logs
         Given I have only the following CEL entries:
            | eventtype    | eventtime                  | cid_name | cid_num | exten | context | channame            |      uniqueid |      linkedid | userfield |
            | CHAN_START   | 2015-06-18 14:17:15.314919 | Elès 45  | 1045    | 1001  | default | SIP/as2mkq-0000002f | 1434651435.47 | 1434651435.47 |           |
            | APP_START    | 2015-06-18 14:17:15.418728 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-0000002f | 1434651435.47 | 1434651435.47 |           |
            | CHAN_START   | 2015-06-18 14:17:15.42325  | Elès 01  | 1001    | s     | default | SIP/je5qtq-00000030 | 1434651435.48 | 1434651435.47 |           |
            | ANSWER       | 2015-06-18 14:17:17.632403 | Elès 01  | 1001    | s     | default | SIP/je5qtq-00000030 | 1434651435.48 | 1434651435.47 |           |
            | ANSWER       | 2015-06-18 14:17:17.641401 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-0000002f | 1434651435.47 | 1434651435.47 |           |
            | BRIDGE_ENTER | 2015-06-18 14:17:17.642693 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-0000002f | 1434651435.47 | 1434651435.47 |           |
            | BRIDGE_ENTER | 2015-06-18 14:17:17.644112 | Elès 01  | 1001    |       | default | SIP/je5qtq-00000030 | 1434651435.48 | 1434651435.47 |           |
            | BRIDGE_EXIT  | 2015-06-18 14:17:22.249479 | Elès 01  | 1001    |       | default | SIP/je5qtq-00000030 | 1434651435.48 | 1434651435.47 |           |
            | HANGUP       | 2015-06-18 14:17:22.259363 | Elès 01  | 1001    |       | default | SIP/je5qtq-00000030 | 1434651435.48 | 1434651435.47 |           |
            | CHAN_END     | 2015-06-18 14:17:22.260562 | Elès 01  | 1001    |       | default | SIP/je5qtq-00000030 | 1434651435.48 | 1434651435.47 |           |
            | BRIDGE_EXIT  | 2015-06-18 14:17:22.261986 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-0000002f | 1434651435.47 | 1434651435.47 |           |
            | HANGUP       | 2015-06-18 14:17:22.263564 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-0000002f | 1434651435.47 | 1434651435.47 |           |
            | CHAN_END     | 2015-06-18 14:17:22.264727 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-0000002f | 1434651435.47 | 1434651435.47 |           |
            | LINKEDID_END | 2015-06-18 14:17:22.266043 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-0000002f | 1434651435.47 | 1434651435.47 |           |
            | CHAN_START   | 2015-06-18 14:17:24.135378 | Elès 45  | 1045    | 1001  | default | SIP/as2mkq-00000031 | 1434651444.49 | 1434651444.49 |           |
            | APP_START    | 2015-06-18 14:17:24.938839 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-00000031 | 1434651444.49 | 1434651444.49 |           |
            | CHAN_START   | 2015-06-18 14:17:24.943746 | Elès 01  | 1001    | s     | default | SIP/je5qtq-00000032 | 1434651444.50 | 1434651444.49 |           |
            | ANSWER       | 2015-06-18 14:17:27.124748 | Elès 01  | 1001    | s     | default | SIP/je5qtq-00000032 | 1434651444.50 | 1434651444.49 |           |
            | ANSWER       | 2015-06-18 14:17:27.134133 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-00000031 | 1434651444.49 | 1434651444.49 |           |
            | BRIDGE_ENTER | 2015-06-18 14:17:27.135653 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-00000031 | 1434651444.49 | 1434651444.49 |           |
            | BRIDGE_ENTER | 2015-06-18 14:17:27.136997 | Elès 01  | 1001    |       | default | SIP/je5qtq-00000032 | 1434651444.50 | 1434651444.49 |           |
            | BRIDGE_EXIT  | 2015-06-18 14:17:30.54609  | Elès 45  | 1045    | s     | user    | SIP/as2mkq-00000031 | 1434651444.49 | 1434651444.49 |           |
            | HANGUP       | 2015-06-18 14:17:30.556918 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-00000031 | 1434651444.49 | 1434651444.49 |           |
            | CHAN_END     | 2015-06-18 14:17:30.558334 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-00000031 | 1434651444.49 | 1434651444.49 |           |
            | BRIDGE_EXIT  | 2015-06-18 14:17:30.559702 | Elès 01  | 1001    |       | default | SIP/je5qtq-00000032 | 1434651444.50 | 1434651444.49 |           |
            | HANGUP       | 2015-06-18 14:17:30.561057 | Elès 01  | 1001    |       | default | SIP/je5qtq-00000032 | 1434651444.50 | 1434651444.49 |           |
            | CHAN_END     | 2015-06-18 14:17:30.562551 | Elès 01  | 1001    |       | default | SIP/je5qtq-00000032 | 1434651444.50 | 1434651444.49 |           |
            | LINKEDID_END | 2015-06-18 14:17:30.563808 | Elès 01  | 1001    |       | default | SIP/je5qtq-00000032 | 1434651444.50 | 1434651444.49 |           |
            | CHAN_START   | 2015-06-18 14:17:32.195429 | Elès 45  | 1045    | 1001  | default | SIP/as2mkq-00000033 | 1434651452.51 | 1434651452.51 |           |
            | APP_START    | 2015-06-18 14:17:32.296484 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-00000033 | 1434651452.51 | 1434651452.51 |           |
            | CHAN_START   | 2015-06-18 14:17:32.301413 | Elès 01  | 1001    | s     | default | SIP/je5qtq-00000034 | 1434651452.52 | 1434651452.51 |           |
            | ANSWER       | 2015-06-18 14:17:34.066573 | Elès 01  | 1001    | s     | default | SIP/je5qtq-00000034 | 1434651452.52 | 1434651452.51 |           |
            | ANSWER       | 2015-06-18 14:17:34.079356 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-00000033 | 1434651452.51 | 1434651452.51 |           |
            | BRIDGE_ENTER | 2015-06-18 14:17:34.080717 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-00000033 | 1434651452.51 | 1434651452.51 |           |
            | BRIDGE_ENTER | 2015-06-18 14:17:34.082069 | Elès 01  | 1001    |       | default | SIP/je5qtq-00000034 | 1434651452.52 | 1434651452.51 |           |
            | BRIDGE_EXIT  | 2015-06-18 14:17:37.528919 | Elès 01  | 1001    |       | default | SIP/je5qtq-00000034 | 1434651452.52 | 1434651452.51 |           |
            | HANGUP       | 2015-06-18 14:17:37.538345 | Elès 01  | 1001    |       | default | SIP/je5qtq-00000034 | 1434651452.52 | 1434651452.51 |           |
            | CHAN_END     | 2015-06-18 14:17:37.539689 | Elès 01  | 1001    |       | default | SIP/je5qtq-00000034 | 1434651452.52 | 1434651452.51 |           |
            | BRIDGE_EXIT  | 2015-06-18 14:17:37.54106  | Elès 45  | 1045    | s     | user    | SIP/as2mkq-00000033 | 1434651452.51 | 1434651452.51 |           |
            | HANGUP       | 2015-06-18 14:17:37.542328 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-00000033 | 1434651452.51 | 1434651452.51 |           |
            | CHAN_END     | 2015-06-18 14:17:37.544217 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-00000033 | 1434651452.51 | 1434651452.51 |           |
            | LINKEDID_END | 2015-06-18 14:17:37.545342 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-00000033 | 1434651452.51 | 1434651452.51 |           |
        When I generate call logs using the last 12 unprocessed CEL entries
        Then I should have the following call logs:
            | date                       | date_answer                | date_end                   |
            | 2015-06-18 14:17:32.195429 | 2015-06-18 14:17:34.080717 | 2015-06-18 14:17:37.544217 |
        Then I should not have the following call logs:
            | date                       | date_answer                | date_end                   |
            | 2015-06-18 14:17:15.314919 | 2015-06-18 14:17:17.642693 | 2015-06-18 14:17:22.264727 |
            | 2015-06-18 14:17:24.135378 | 2015-06-18 14:17:27.135653 | 2015-06-18 14:17:30.558334 |

     Scenario: Generation for a specified latest CEL count with processed calls
         Given there are no call logs
         Given I have only the following CEL entries:
            | eventtype    | eventtime           | cid_name      | cid_num | exten | context | channame            |     uniqueid |     linkedid | userfield |
            | CHAN_START   | 2013-01-01 08:00:00 | Bob Marley    |    1002 | 1001  | default | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |
            | APP_START    | 2013-01-01 08:00:01 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |
            | CHAN_START   | 2013-01-01 08:00:02 | Alice Aglisse |    1001 | s     | default | SIP/hg63xv-00000013 | 1375994780.2 | 1375994780.1 |           |
            | ANSWER       | 2013-01-01 08:00:03 | Alice Aglisse |    1001 | s     | default | SIP/hg63xv-00000013 | 1375994780.2 | 1375994780.1 |           |
            | ANSWER       | 2013-01-01 08:00:04 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |
            | BRIDGE_START | 2013-01-01 08:00:05 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |
            | BRIDGE_END   | 2013-01-01 08:00:06 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |
            | HANGUP       | 2013-01-01 08:00:07 | Alice Aglisse |    1001 |       | user    | SIP/hg63xv-00000013 | 1375994780.2 | 1375994780.1 |           |
            | CHAN_END     | 2013-01-01 08:00:08 | Alice Aglisse |    1001 |       | user    | SIP/hg63xv-00000013 | 1375994780.2 | 1375994780.1 |           |
            | HANGUP       | 2013-01-01 08:00:09 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |
            | CHAN_END     | 2013-01-01 08:00:10 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |
            | LINKEDID_END | 2013-01-01 08:00:11 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |
            | CHAN_START   | 2013-01-01 09:00:00 | Bob Marley    |    1002 | 1001  | default | SIP/z77kvm-00000028 | 1375994781.1 | 1375994781.1 |           |
            | APP_START    | 2013-01-01 09:00:01 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994781.1 | 1375994781.1 |           |
            | CHAN_START   | 2013-01-01 09:00:02 | Alice Aglisse |    1001 | s     | default | SIP/hg63xv-00000013 | 1375994781.2 | 1375994781.1 |           |
            | ANSWER       | 2013-01-01 09:00:03 | Alice Aglisse |    1001 | s     | default | SIP/hg63xv-00000013 | 1375994781.2 | 1375994781.1 |           |
            | ANSWER       | 2013-01-01 09:00:04 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994781.1 | 1375994781.1 |           |
            | BRIDGE_START | 2013-01-01 09:00:05 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994781.1 | 1375994781.1 |           |
            | BRIDGE_END   | 2013-01-01 09:00:06 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994781.1 | 1375994781.1 |           |
            | HANGUP       | 2013-01-01 09:00:07 | Alice Aglisse |    1001 |       | user    | SIP/hg63xv-00000013 | 1375994781.2 | 1375994781.1 |           |
            | CHAN_END     | 2013-01-01 09:00:08 | Alice Aglisse |    1001 |       | user    | SIP/hg63xv-00000013 | 1375994781.2 | 1375994781.1 |           |
            | HANGUP       | 2013-01-01 09:00:09 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994781.1 | 1375994781.1 |           |
            | CHAN_END     | 2013-01-01 09:00:10 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994781.1 | 1375994781.1 |           |
            | LINKEDID_END | 2013-01-01 09:00:11 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994781.1 | 1375994781.1 |           |
            | CHAN_START   | 2013-01-01 10:00:00 | Bob Marley    |    1002 | 1001  | default | SIP/z77kvm-00000028 | 1375994782.1 | 1375994782.1 |           |
            | APP_START    | 2013-01-01 10:00:01 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994782.1 | 1375994782.1 |           |
            | CHAN_START   | 2013-01-01 10:00:02 | Alice Aglisse |    1001 | s     | default | SIP/hg63xv-00000013 | 1375994782.2 | 1375994782.1 |           |
            | ANSWER       | 2013-01-01 10:00:03 | Alice Aglisse |    1001 | s     | default | SIP/hg63xv-00000013 | 1375994782.2 | 1375994782.1 |           |
            | ANSWER       | 2013-01-01 10:00:04 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994782.1 | 1375994782.1 |           |
            | BRIDGE_START | 2013-01-01 10:00:05 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994782.1 | 1375994782.1 |           |
            | BRIDGE_END   | 2013-01-01 10:00:06 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994782.1 | 1375994782.1 |           |
            | HANGUP       | 2013-01-01 10:00:07 | Alice Aglisse |    1001 |       | user    | SIP/hg63xv-00000013 | 1375994782.2 | 1375994782.1 |           |
            | CHAN_END     | 2013-01-01 10:00:08 | Alice Aglisse |    1001 |       | user    | SIP/hg63xv-00000013 | 1375994782.2 | 1375994782.1 |           |
            | HANGUP       | 2013-01-01 10:00:09 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994782.1 | 1375994782.1 |           |
            | CHAN_END     | 2013-01-01 10:00:10 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994782.1 | 1375994782.1 |           |
            | LINKEDID_END | 2013-01-01 10:00:11 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994782.1 | 1375994782.1 |           |
        When I generate call logs using the last 12 unprocessed CEL entries
        When I generate call logs using the last 12 unprocessed CEL entries
        Then I should have the following call logs:
            | date                | date_answer         | date_end            |
            | 2013-01-01 09:00:00 | 2013-01-01 09:00:05 | 2013-01-01 09:00:10 |
            | 2013-01-01 10:00:00 | 2013-01-01 10:00:05 | 2013-01-01 10:00:10 |
        Then I should not have the following call logs:
            | date                | date_answer         | date_end            |
            | 2013-01-01 08:00:00 | 2013-01-01 08:00:05 | 2013-01-01 08:00:10 |

     Scenario: Running call log generation in parallel should fail
         Given there are no call logs
         Given there are a lot of unprocessed calls
         When I generate call logs twice in parallel
         Then I see that call log generation is already running

     Scenario: Generation of complete calls only
         Given there are no call logs
         Given I have only the following CEL entries:
            | eventtype    | eventtime           | cid_name      | cid_num | exten | context | channame            |     uniqueid |     linkedid | userfield |
            | CHAN_START   | 2013-01-01 08:00:00 | Bob Marley    |    1002 | 1001  | default | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |
            | APP_START    | 2013-01-01 08:00:01 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |
            | CHAN_START   | 2013-01-01 08:00:02 | Alice Aglisse |    1001 | s     | default | SIP/hg63xv-00000013 | 1375994780.2 | 1375994780.1 |           |
            | ANSWER       | 2013-01-01 08:00:03 | Alice Aglisse |    1001 | s     | default | SIP/hg63xv-00000013 | 1375994780.2 | 1375994780.1 |           |
            | ANSWER       | 2013-01-01 08:00:04 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |
            | BRIDGE_START | 2013-01-01 08:00:05 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |
            | BRIDGE_END   | 2013-01-01 08:00:06 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |
            | HANGUP       | 2013-01-01 08:00:07 | Alice Aglisse |    1001 |       | user    | SIP/hg63xv-00000013 | 1375994780.2 | 1375994780.1 |           |
            | CHAN_END     | 2013-01-01 08:00:08 | Alice Aglisse |    1001 |       | user    | SIP/hg63xv-00000013 | 1375994780.2 | 1375994780.1 |           |
            | HANGUP       | 2013-01-01 08:00:09 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |
            | CHAN_END     | 2013-01-01 08:00:10 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |
         When I generate call logs using the last 1 unprocessed CEL entries
         Then I should have the following call logs:
            | date                | date_answer         | date_end            |
            | 2013-01-01 08:00:00 | 2013-01-01 08:00:05 | 2013-01-01 08:00:10 |

     Scenario: Generation of partially processed calls
        Given there are only the following call logs:
            | id | date                | date_answer         | date_end            | source_name | source_exten | destination_exten | user_field | source_line_identity | destination_line_identity |
            | 42 | 2013-01-01 08:00:00 | 2013-01-01 08:00:05 | 2013-01-01 08:00:10 | Bob Marley  |         1002 |              1001 |            | sip/z77kvm           | sip/hg63xv                |
         Given I have only the following CEL entries:
            | eventtype    | eventtime           | cid_name      | cid_num | exten | context | channame            |     uniqueid |     linkedid | userfield | call_log_id |
            | CHAN_START   | 2013-01-01 08:00:00 | Bob Marley    |    1002 | 1001  | default | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |          42 |
            | APP_START    | 2013-01-01 08:00:01 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |          42 |
            | CHAN_START   | 2013-01-01 08:00:02 | Alice Aglisse |    1001 | s     | default | SIP/hg63xv-00000013 | 1375994780.2 | 1375994780.1 |           |          42 |
            | ANSWER       | 2013-01-01 08:00:03 | Alice Aglisse |    1001 | s     | default | SIP/hg63xv-00000013 | 1375994780.2 | 1375994780.1 |           |          42 |
            | ANSWER       | 2013-01-01 08:00:04 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |          42 |
            | BRIDGE_START | 2013-01-01 08:00:05 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |          42 |
            | BRIDGE_END   | 2013-01-01 08:00:06 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |             |
            | HANGUP       | 2013-01-01 08:00:07 | Alice Aglisse |    1001 |       | user    | SIP/hg63xv-00000013 | 1375994780.2 | 1375994780.1 |           |             |
            | CHAN_END     | 2013-01-01 08:00:08 | Alice Aglisse |    1001 |       | user    | SIP/hg63xv-00000013 | 1375994780.2 | 1375994780.1 |           |             |
            | HANGUP       | 2013-01-01 08:00:09 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |             |
            | CHAN_END     | 2013-01-01 08:00:10 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |             |
         When I generate call logs using the last 20 unprocessed CEL entries
         Then I should have the following call logs:
            | date                | date_answer         | date_end            | source_name | source_exten | destination_exten | user_field | source_line_identity | destination_line_identity |
            | 2013-01-01 08:00:00 | 2013-01-01 08:00:05 | 2013-01-01 08:00:10 | Bob Marley  |         1002 |              1001 |            | sip/z77kvm           | sip/hg63xv                |
