Feature: Call Log Generation

    Scenario: Generation of answered internal call
        Given there are no call logs
        Given I have only the following CEL entries:
            | eventtype    | eventtime                  | cid_name | cid_num | exten | context | channame            |      uniqueid |     linkedid  | userfield |
            | CHAN_START   | 2015-06-18 14:08:56.910686 | Elès 45  | 1045    | 1001  | default | SIP/as2mkq-0000001f | 1434650936.31 | 1434650936.31 |           |
            | APP_START    | 2015-06-18 14:08:57.014249 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-0000001f | 1434650936.31 | 1434650936.31 |           |
            | CHAN_START   | 2015-06-18 14:08:57.019202 | Elès 01  | 1001    | s     | default | SIP/je5qtq-00000020 | 1434650937.32 | 1434650936.31 |           |
            | ANSWER       | 2015-06-18 14:08:59.864053 | Elès 01  | 1001    | s     | default | SIP/je5qtq-00000020 | 1434650937.32 | 1434650936.31 |           |
            | ANSWER       | 2015-06-18 14:08:59.877155 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-0000001f | 1434650936.31 | 1434650936.31 |           |
            | BRIDGE_ENTER | 2015-06-18 14:08:59.878    | Elès 45  | 1045    | s     | user    | SIP/as2mkq-0000001f | 1434650936.31 | 1434650936.31 |           |
            | BRIDGE_ENTER | 2015-06-18 14:08:59.87976  | Elès 01  | 1001    |       | default | SIP/je5qtq-00000020 | 1434650937.32 | 1434650936.31 |           |
            | BRIDGE_EXIT  | 2015-06-18 14:09:02.250446 | Elès 01  | 1001    |       | default | SIP/je5qtq-00000020 | 1434650937.32 | 1434650936.31 |           |
            | HANGUP       | 2015-06-18 14:09:02.26592  | Elès 01  | 1001    |       | default | SIP/je5qtq-00000020 | 1434650937.32 | 1434650936.31 |           |
            | CHAN_END     | 2015-06-18 14:09:02.267146 | Elès 01  | 1001    |       | default | SIP/je5qtq-00000020 | 1434650937.32 | 1434650936.31 |           |
            | BRIDGE_EXIT  | 2015-06-18 14:09:02.268    | Elès 45  | 1045    | s     | user    | SIP/as2mkq-0000001f | 1434650936.31 | 1434650936.31 |           |
            | HANGUP       | 2015-06-18 14:09:02.269498 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-0000001f | 1434650936.31 | 1434650936.31 |           |
            | CHAN_END     | 2015-06-18 14:09:02.271033 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-0000001f | 1434650936.31 | 1434650936.31 |           |
            | LINKEDID_END | 2015-06-18 14:09:02.272325 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-0000001f | 1434650936.31 | 1434650936.31 |           |
        When I generate call logs
        Then I should have the following call logs:
            | date                       | date_answer             | date_end                   | source_name | source_exten | destination_exten | user_field | source_line_identity | destination_line_identity |
            | 2015-06-18 14:08:56.910686 | 2015-06-18 14:08:59.878 | 2015-06-18 14:09:02.271033 | Elès 45     | 1045         | 1001              |            | sip/as2mkq           | sip/je5qtq                |

    Scenario: Generation of non-answered internal call
        Given there are no call logs
        Given I have only the following CEL entries:
            | eventtype    | eventtime                  | cid_name | cid_num | exten | context | channame            |      uniqueid |     linkedid  | userfield |
            | CHAN_START   | 2015-06-18 14:10:24.586638 | Elès 45  | 1045    | 1001  | default | SIP/as2mkq-00000021 | 1434651024.33 | 1434651024.33 |           |
            | APP_START    | 2015-06-18 14:10:24.6893   | Elès 45  | 1045    | s     | user    | SIP/as2mkq-00000021 | 1434651024.33 | 1434651024.33 |           |
            | CHAN_START   | 2015-06-18 14:10:24.694166 | Elès 01  | 1001    | s     | default | SIP/je5qtq-00000022 | 1434651024.34 | 1434651024.33 |           |
            | HANGUP       | 2015-06-18 14:10:28.280456 | Elès 01  | 1001    | s     | default | SIP/je5qtq-00000022 | 1434651024.34 | 1434651024.33 |           |
            | CHAN_END     | 2015-06-18 14:10:28.28819  | Elès 01  | 1001    | s     | default | SIP/je5qtq-00000022 | 1434651024.34 | 1434651024.33 |           |
            | HANGUP       | 2015-06-18 14:10:28.289431 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-00000021 | 1434651024.33 | 1434651024.33 |           |
            | CHAN_END     | 2015-06-18 14:10:28.290746 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-00000021 | 1434651024.33 | 1434651024.33 |           |
            | LINKEDID_END | 2015-06-18 14:10:28.292243 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-00000021 | 1434651024.33 | 1434651024.33 |           |
        When I generate call logs
        Then I should have the following call logs:
            | date                       | date_answer | date_end                   | source_name | source_exten | destination_exten | user_field | source_line_identity | destination_line_identity |
            | 2015-06-18 14:10:24.586638 | NULL        | 2015-06-18 14:10:28.290746 | Elès 45     | 1045         | 1001              |            | sip/as2mkq           | sip/je5qtq                |

    Scenario: Generation of answered incoming call
        Given there are no call logs
        Given I have only the following CEL entries:
            | eventtype    | eventtime             | cid_name   |    cid_num | exten | context     | channame            |      uniqueid |      linkedid | userfield |
            | CHAN_START   | 2013-01-01 11:02:38.0 | 612345678  |  612345678 | 1002  | from-extern | SIP/trunk-00000028  | 1376060558.17 | 1376060558.17 |           |
            | APP_START    | 2013-01-01 11:02:38.1 |            | 0612345678 | s     | user        | SIP/trunk-00000028  | 1376060558.17 | 1376060558.17 |           |
            | CHAN_START   | 2013-01-01 11:02:38.2 | Bob Marley |       1002 | s     | default     | SIP/hg63xv-00000013 | 1376060558.18 | 1376060558.17 |           |
            | ANSWER       | 2013-01-01 11:02:42.0 | Bob Marley |       1002 | s     | default     | SIP/hg63xv-00000013 | 1376060558.18 | 1376060558.17 |           |
            | ANSWER       | 2013-01-01 11:02:42.1 |            | 0612345678 | s     | user        | SIP/trunk-00000028  | 1376060558.17 | 1376060558.17 |           |
            | BRIDGE_START | 2013-01-01 11:02:42.2 |            | 0612345678 | s     | user        | SIP/trunk-00000028  | 1376060558.17 | 1376060558.17 |           |
            | BRIDGE_END   | 2013-01-01 11:02:45.0 |            | 0612345678 | s     | user        | SIP/trunk-00000028  | 1376060558.17 | 1376060558.17 |           |
            | HANGUP       | 2013-01-01 11:02:45.1 | Bob Marley |       1002 |       | user        | SIP/hg63xv-00000013 | 1376060558.18 | 1376060558.17 |           |
            | CHAN_END     | 2013-01-01 11:02:45.2 | Bob Marley |       1002 |       | user        | SIP/hg63xv-00000013 | 1376060558.18 | 1376060558.17 |           |
            | HANGUP       | 2013-01-01 11:02:45.3 |            | 0612345678 | s     | user        | SIP/trunk-00000028  | 1376060558.17 | 1376060558.17 |           |
            | CHAN_END     | 2013-01-01 11:02:45.4 |            | 0612345678 | s     | user        | SIP/trunk-00000028  | 1376060558.17 | 1376060558.17 |           |
            | LINKEDID_END | 2013-01-01 11:02:45.5 |            | 0612345678 | s     | user        | SIP/trunk-00000028  | 1376060558.17 | 1376060558.17 |           |
        When I generate call logs
        Then I should have the following call logs:
            | date                  | date_answer           | date_end              | source_name | source_exten | destination_exten | user_field | source_line_identity | destination_line_identity |
            | 2013-01-01 11:02:38.0 | 2013-01-01 11:02:42.2 | 2013-01-01 11:02:45.4 |   612345678 |    612345678 |              1002 |            | sip/trunk            | sip/hg63xv                |

	Scenario: Generation of answered incoming call on s extension
        Given there are no call logs
        Given I have only the following CEL entries:
            | eventtype    | eventtime             | cid_name   |    cid_num | exten | context     | channame            |      uniqueid |      linkedid | userfield |
            | CHAN_START   | 2013-01-01 11:02:38.0 | 612345678  |  612345678 | s     | from-extern | SIP/trunk-00000028  | 1376060558.17 | 1376060558.17 |           |
            | XIVO_FROM_S  | 2013-01-01 11:02:38.1 | 612345678  |  612345678 | 1002  | from-extern | SIP/trunk-00000028  | 1376060558.17 | 1376060558.17 |           |
            | APP_START    | 2013-01-01 11:02:38.1 |            | 0612345678 | s     | user        | SIP/trunk-00000028  | 1376060558.17 | 1376060558.17 |           |
            | CHAN_START   | 2013-01-01 11:02:38.2 | Bob Marley |       1002 | s     | default     | SIP/hg63xv-00000013 | 1376060558.18 | 1376060558.17 |           |
            | ANSWER       | 2013-01-01 11:02:42.0 | Bob Marley |       1002 | s     | default     | SIP/hg63xv-00000013 | 1376060558.18 | 1376060558.17 |           |
            | ANSWER       | 2013-01-01 11:02:42.1 |            | 0612345678 | s     | user        | SIP/trunk-00000028  | 1376060558.17 | 1376060558.17 |           |
            | BRIDGE_START | 2013-01-01 11:02:42.2 |            | 0612345678 | s     | user        | SIP/trunk-00000028  | 1376060558.17 | 1376060558.17 |           |
            | BRIDGE_END   | 2013-01-01 11:02:45.0 |            | 0612345678 | s     | user        | SIP/trunk-00000028  | 1376060558.17 | 1376060558.17 |           |
            | HANGUP       | 2013-01-01 11:02:45.1 | Bob Marley |       1002 |       | user        | SIP/hg63xv-00000013 | 1376060558.18 | 1376060558.17 |           |
            | CHAN_END     | 2013-01-01 11:02:45.2 | Bob Marley |       1002 |       | user        | SIP/hg63xv-00000013 | 1376060558.18 | 1376060558.17 |           |
            | HANGUP       | 2013-01-01 11:02:45.3 |            | 0612345678 | s     | user        | SIP/trunk-00000028  | 1376060558.17 | 1376060558.17 |           |
            | CHAN_END     | 2013-01-01 11:02:45.4 |            | 0612345678 | s     | user        | SIP/trunk-00000028  | 1376060558.17 | 1376060558.17 |           |
            | LINKEDID_END | 2013-01-01 11:02:45.5 |            | 0612345678 | s     | user        | SIP/trunk-00000028  | 1376060558.17 | 1376060558.17 |           |
        When I generate call logs
        Then I should have the following call logs:
            | date                  | date_answer           | date_end              | source_name | source_exten | destination_exten | user_field | source_line_identity | destination_line_identity |
            | 2013-01-01 11:02:38.0 | 2013-01-01 11:02:42.2 | 2013-01-01 11:02:45.4 |   612345678 |    612345678 |              1002 |            | sip/trunk            | sip/hg63xv                |

    Scenario: Generation of answered outgoing call
        Given there are no call logs
        Given I have only the following CEL entries:
            | eventtype    | eventtime                  | cid_name | cid_num   | exten     | context     | channame              |      uniqueid |     linkedid  | userfield |
            | CHAN_START   | 2015-06-18 14:12:05.935283 | Elès 01  | 1001      | **9642301 | default     | SIP/je5qtq-00000025   | 1434651125.37 | 1434651125.37 |           |
            | XIVO_OUTCALL | 2015-06-18 14:12:06.118509 | Elès 01  | 1001      | dial      | outcall     | SIP/je5qtq-00000025   | 1434651125.37 | 1434651125.37 |           |
            | APP_START    | 2015-06-18 14:12:06.123695 | Elès 01  | 1001      | dial      | outcall     | SIP/je5qtq-00000025   | 1434651125.37 | 1434651125.37 |           |
            | CHAN_START   | 2015-06-18 14:12:06.124957 |          |           | s         | from-extern | SIP/dev_34-1-00000026 | 1434651126.38 | 1434651125.37 |           |
            | ANSWER       | 2015-06-18 14:12:12.500153 |          | **9642301 | dial      | from-extern | SIP/dev_34-1-00000026 | 1434651126.38 | 1434651125.37 |           |
            | ANSWER       | 2015-06-18 14:12:12.514389 | Elès 01  | 1001      | dial      | outcall     | SIP/je5qtq-00000025   | 1434651125.37 | 1434651125.37 |           |
            | BRIDGE_ENTER | 2015-06-18 14:12:12.515753 | Elès 01  | 1001      | dial      | outcall     | SIP/je5qtq-00000025   | 1434651125.37 | 1434651125.37 |           |
            | BRIDGE_ENTER | 2015-06-18 14:12:12.517027 |          | **9642301 |           | from-extern | SIP/dev_34-1-00000026 | 1434651126.38 | 1434651125.37 |           |
            | BRIDGE_EXIT  | 2015-06-18 14:12:16.85455  | Elès 01  | 1001      | dial      | outcall     | SIP/je5qtq-00000025   | 1434651125.37 | 1434651125.37 |           |
            | HANGUP       | 2015-06-18 14:12:16.861414 | Elès 01  | 1001      | dial      | outcall     | SIP/je5qtq-00000025   | 1434651125.37 | 1434651125.37 |           |
            | CHAN_END     | 2015-06-18 14:12:16.862638 | Elès 01  | 1001      | dial      | outcall     | SIP/je5qtq-00000025   | 1434651125.37 | 1434651125.37 |           |
            | BRIDGE_EXIT  | 2015-06-18 14:12:16.863979 |          | **9642301 |           | from-extern | SIP/dev_34-1-00000026 | 1434651126.38 | 1434651125.37 |           |
            | HANGUP       | 2015-06-18 14:12:16.865316 |          | **9642301 |           | from-extern | SIP/dev_34-1-00000026 | 1434651126.38 | 1434651125.37 |           |
            | CHAN_END     | 2015-06-18 14:12:16.866615 |          | **9642301 |           | from-extern | SIP/dev_34-1-00000026 | 1434651126.38 | 1434651125.37 |           |
            | LINKEDID_END | 2015-06-18 14:12:16.867848 |          | **9642301 |           | from-extern | SIP/dev_34-1-00000026 | 1434651126.38 | 1434651125.37 |           |
            | CHAN_START   | 2015-06-18 14:13:18.176182 | Elès 01  | 1001      | **9642301 | default     | SIP/je5qtq-00000027   | 1434651198.39 | 1434651198.39 |           |
            | XIVO_OUTCALL | 2015-06-18 14:13:18.250067 | Elès 01  | 1001      | dial      | outcall     | SIP/je5qtq-00000027   | 1434651198.39 | 1434651198.39 | foo       |
            | APP_START    | 2015-06-18 14:13:18.254452 | Elès 01  | 1001      | dial      | outcall     | SIP/je5qtq-00000027   | 1434651198.39 | 1434651198.39 | foo       |
            | CHAN_START   | 2015-06-18 14:13:18.255915 |          |           | s         | from-extern | SIP/dev_34-1-00000028 | 1434651198.40 | 1434651198.39 |           |
            | ANSWER       | 2015-06-18 14:13:20.98612  |          | **9642301 | dial      | from-extern | SIP/dev_34-1-00000028 | 1434651198.40 | 1434651198.39 |           |
            | ANSWER       | 2015-06-18 14:13:20.998113 | Elès 01  | 1001      | dial      | outcall     | SIP/je5qtq-00000027   | 1434651198.39 | 1434651198.39 | foo       |
            | BRIDGE_ENTER | 2015-06-18 14:13:21.190246 | Elès 01  | 1001      | dial      | outcall     | SIP/je5qtq-00000027   | 1434651198.39 | 1434651198.39 | foo       |
            | BRIDGE_ENTER | 2015-06-18 14:13:21.192798 |          | **9642301 |           | from-extern | SIP/dev_34-1-00000028 | 1434651198.40 | 1434651198.39 |           |
            | BRIDGE_EXIT  | 2015-06-18 14:13:24.137056 | Elès 01  | 1001      | dial      | outcall     | SIP/je5qtq-00000027   | 1434651198.39 | 1434651198.39 | foo       |
            | HANGUP       | 2015-06-18 14:13:24.146256 | Elès 01  | 1001      | dial      | outcall     | SIP/je5qtq-00000027   | 1434651198.39 | 1434651198.39 | foo       |
            | CHAN_END     | 2015-06-18 14:13:24.14759  | Elès 01  | 1001      | dial      | outcall     | SIP/je5qtq-00000027   | 1434651198.39 | 1434651198.39 | foo       |
            | BRIDGE_EXIT  | 2015-06-18 14:13:24.148734 |          | **9642301 |           | from-extern | SIP/dev_34-1-00000028 | 1434651198.40 | 1434651198.39 |           |
            | HANGUP       | 2015-06-18 14:13:24.149943 |          | **9642301 |           | from-extern | SIP/dev_34-1-00000028 | 1434651198.40 | 1434651198.39 |           |
            | CHAN_END     | 2015-06-18 14:13:24.151296 |          | **9642301 |           | from-extern | SIP/dev_34-1-00000028 | 1434651198.40 | 1434651198.39 |           |
            | LINKEDID_END | 2015-06-18 14:13:24.152458 |          | **9642301 |           | from-extern | SIP/dev_34-1-00000028 | 1434651198.40 | 1434651198.39 |           |
        When I generate call logs
        Then I should have the following call logs:
            | date                       | date_answer                | date_end                   | source_name | source_exten | destination_exten | user_field | source_line_identity | destination_line_identity |
            | 2015-06-18 14:12:05.935283 | 2015-06-18 14:12:12.515753 | 2015-06-18 14:12:16.862638 | Elès 01     | 1001         | **9642301         |            | sip/je5qtq           | sip/dev_34-1              |
            | 2015-06-18 14:13:18.176182 | 2015-06-18 14:13:21.190246 | 2015-06-18 14:13:24.14759  | Elès 01     | 1001         | **9642301         | foo        | sip/je5qtq           | sip/dev_34-1              |

    Scenario: Generation of originate call
        Given there are no call logs
        Given I have only the following CEL entries:
            | eventtype     | eventtime                  | cid_name | cid_num | exten | context | channame            |      uniqueid |     linkedid  | userfield |
            |  CHAN_START   | 2015-06-18 14:15:12.978338 | Elès 45  | 1045    | s     | default | SIP/as2mkq-0000002b | 1434651312.43 | 1434651312.43 |           |
            |  ANSWER       | 2015-06-18 14:15:14.587341 | 1001     | 1001    |       | default | SIP/as2mkq-0000002b | 1434651312.43 | 1434651312.43 |           |
            |  APP_START    | 2015-06-18 14:15:14.697414 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-0000002b | 1434651312.43 | 1434651312.43 |           |
            |  CHAN_START   | 2015-06-18 14:15:14.702394 | Elès 01  | 1001    | s     | default | SIP/je5qtq-0000002c | 1434651314.44 | 1434651312.43 |           |
            |  ANSWER       | 2015-06-18 14:15:16.389857 | Elès 01  | 1001    | s     | default | SIP/je5qtq-0000002c | 1434651314.44 | 1434651312.43 |           |
            |  BRIDGE_ENTER | 2015-06-18 14:15:16.396213 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-0000002b | 1434651312.43 | 1434651312.43 |           |
            |  BRIDGE_ENTER | 2015-06-18 14:15:16.397787 | Elès 01  | 1001    |       | default | SIP/je5qtq-0000002c | 1434651314.44 | 1434651312.43 |           |
            |  BRIDGE_EXIT  | 2015-06-18 14:15:19.192422 | Elès 01  | 1001    |       | default | SIP/je5qtq-0000002c | 1434651314.44 | 1434651312.43 |           |
            |  HANGUP       | 2015-06-18 14:15:19.206152 | Elès 01  | 1001    |       | default | SIP/je5qtq-0000002c | 1434651314.44 | 1434651312.43 |           |
            |  CHAN_END     | 2015-06-18 14:15:19.208217 | Elès 01  | 1001    |       | default | SIP/je5qtq-0000002c | 1434651314.44 | 1434651312.43 |           |
            |  BRIDGE_EXIT  | 2015-06-18 14:15:19.209432 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-0000002b | 1434651312.43 | 1434651312.43 |           |
            |  HANGUP       | 2015-06-18 14:15:19.211393 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-0000002b | 1434651312.43 | 1434651312.43 |           |
            |  CHAN_END     | 2015-06-18 14:15:19.212596 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-0000002b | 1434651312.43 | 1434651312.43 |           |
            |  LINKEDID_END | 2015-06-18 14:15:19.213763 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-0000002b | 1434651312.43 | 1434651312.43 |           |
        When I generate call logs
        Then I should have the following call logs:
            | date                       | date_answer                | date_end                   | source_name | source_exten | destination_exten | user_field | source_line_identity | destination_line_identity |
            | 2015-06-18 14:15:12.978338 | 2015-06-18 14:15:16.396213 | 2015-06-18 14:15:19.212596 | Elès 45     | 1045         | 1001              |            | sip/as2mkq           | sip/je5qtq                |

    Scenario: Generation of unanswered originate call
        Given there are no call logs
        Given I have only the following CEL entries:
            | eventtype    | eventtime                  | cid_name | cid_num | exten | context | channame            |      uniqueid |     linkedid  | userfield |
            | CHAN_START   | 2015-06-18 14:15:48.836632 | Elès 45  | 1045    | s     | default | SIP/as2mkq-0000002d | 1434651348.45 | 1434651348.45 |           |
            | ANSWER       | 2015-06-18 14:15:50.127815 | 1001     | 1001    |       | default | SIP/as2mkq-0000002d | 1434651348.45 | 1434651348.45 |           |
            | APP_START    | 2015-06-18 14:15:50.220755 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-0000002d | 1434651348.45 | 1434651348.45 |           |
            | CHAN_START   | 2015-06-18 14:15:50.22621  | Elès 01  | 1001    | s     | default | SIP/je5qtq-0000002e | 1434651350.46 | 1434651348.45 |           |
            | HANGUP       | 2015-06-18 14:15:54.936991 | Elès 01  | 1001    | s     | default | SIP/je5qtq-0000002e | 1434651350.46 | 1434651348.45 |           |
            | CHAN_END     | 2015-06-18 14:15:54.949784 | Elès 01  | 1001    | s     | default | SIP/je5qtq-0000002e | 1434651350.46 | 1434651348.45 |           |
            | HANGUP       | 2015-06-18 14:15:54.951351 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-0000002d | 1434651348.45 | 1434651348.45 |           |
            | CHAN_END     | 2015-06-18 14:15:54.952707 | Elès 45  | 1045    | s     | user    | SIP/as2mkq-0000002d | 1434651348.45 | 1434651348.45 |           |
            | LINKEDID_END | 2015-06-18 14:15:54.9539   | Elès 45  | 1045    | s     | user    | SIP/as2mkq-0000002d | 1434651348.45 | 1434651348.45 |           |
        When I generate call logs
        Then I should have the following call logs:
            | date                       | date_answer | date_end                   | source_name | source_exten | destination_exten | user_field | source_line_identity | destination_line_identity |
            | 2015-06-18 14:15:48.836632 | NULL        | 2015-06-18 14:15:54.952707 | Elès 45     | 1045         | 1001              |            | sip/as2mkq           | sip/je5qtq                |

    Scenario: Generation of originates hung up by the switchboard
        Given there are no call logs
        Given I have only the following CEL entries:
            | eventtype    | eventtime                  | cid_name | cid_num | exten                | context | channame            |     uniqueid |     linkedid | userfield |
            | CHAN_START   | 2014-02-20 09:28:46.683014 | Carlos   |    1003 | s                    | pcmdev  | SIP/d49t0y-00000003 | 1392906526.4 | 1392906526.4 |           |
            | ANSWER       | 2014-02-20 09:28:47.183651 | 1002     |    1002 |                      | pcmdev  | SIP/d49t0y-00000003 | 1392906526.4 | 1392906526.4 |           |
            | APP_START    | 2014-02-20 09:28:47.288346 | Carlos   |    1003 | s                    | user    | SIP/d49t0y-00000003 | 1392906526.4 | 1392906526.4 |           |
            | CHAN_START   | 2014-02-20 09:28:47.288466 | Bõb      |    1002 | s                    | pcmdev  | SCCP/1002-00000001  | 1392906527.5 | 1392906526.4 |           |
            | HANGUP       | 2014-02-20 09:29:00.306587 | Bõb      |    1002 | s                    | pcmdev  | SCCP/1002-00000001  | 1392906527.5 | 1392906526.4 |           |
            | CHAN_END     | 2014-02-20 09:29:00.307651 | Bõb      |    1002 | s                    | pcmdev  | SCCP/1002-00000001  | 1392906527.5 | 1392906526.4 |           |
            | HANGUP       | 2014-02-20 09:29:00.308165 | Carlos   |    1003 | endcall:hangupsilent | forward | SIP/d49t0y-00000003 | 1392906526.4 | 1392906526.4 |           |
            | CHAN_END     | 2014-02-20 09:29:00.309786 | Carlos   |    1003 | endcall:hangupsilent | forward | SIP/d49t0y-00000003 | 1392906526.4 | 1392906526.4 |           |
            | LINKEDID_END | 2014-02-20 09:29:00.309806 | Carlos   |    1003 | endcall:hangupsilent | forward | SIP/d49t0y-00000003 | 1392906526.4 | 1392906526.4 |           |
        When I generate call logs
        Then I should have the following call logs:
            | date                       | date_answer | date_end                   | source_name | source_exten | destination_exten | user_field | source_line_identity | destination_line_identity |
            | 2014-02-20 09:28:46.683014 | NULL        | 2014-02-20 09:29:00.309786 | Carlos      |         1003 |              1002 |            | sip/d49t0y           | sccp/1002                 |

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
            | date                       | date_answer                | date_end                   | source_name | source_exten | destination_exten | user_field | source_line_identity | destination_line_identity |
            | 2015-06-18 14:17:32.195429 | 2015-06-18 14:17:34.080717 | 2015-06-18 14:17:37.544217 | Elès 45     | 1045         | 1001              |            | sip/as2mkq           | sip/je5qtq                |
        Then I should not have the following call logs:
            | date                       | date_answer                | date_end                   | source_name | source_exten | destination_exten | user_field | source_line_identity | destination_line_identity |
            | 2015-06-18 14:17:15.314919 | 2015-06-18 14:17:17.642693 | 2015-06-18 14:17:22.264727 | Elès 45     | 1045         | 1001              |            | sip/as2mkq           | sip/je5qtq                |
            | 2015-06-18 14:17:24.135378 | 2015-06-18 14:17:27.135653 | 2015-06-18 14:17:30.558334 | Elès 45     | 1045         | 1001              |            | sip/as2mkq           | sip/je5qtq                |

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
            | date                | date_answer         | date_end            | source_name | source_exten | destination_exten | user_field | source_line_identity | destination_line_identity |
            | 2013-01-01 09:00:00 | 2013-01-01 09:00:05 | 2013-01-01 09:00:10 | Bob Marley  |         1002 |              1001 |            | sip/z77kvm           | sip/hg63xv                |
            | 2013-01-01 10:00:00 | 2013-01-01 10:00:05 | 2013-01-01 10:00:10 | Bob Marley  |         1002 |              1001 |            | sip/z77kvm           | sip/hg63xv                |
        Then I should not have the following call logs:
            | date                | date_answer         | date_end            | source_name | source_exten | destination_exten | user_field | source_line_identity | destination_line_identity |
            | 2013-01-01 08:00:00 | 2013-01-01 08:00:05 | 2013-01-01 08:00:10 | Bob Marley  |         1002 |              1001 |            | sip/z77kvm           | sip/hg63xv                |

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
            | date                | date_answer         | date_end            | source_name | source_exten | destination_exten | user_field | source_line_identity | destination_line_identity |
            | 2013-01-01 08:00:00 | 2013-01-01 08:00:05 | 2013-01-01 08:00:10 | Bob Marley  |         1002 |              1001 |            | sip/z77kvm           | sip/hg63xv                |

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

    Scenario: Generation of a call where uniqueid must be sorted chronologically, not alphabetically
        Given there are no call logs
        Given I have only the following CEL entries:
            | eventtype    | eventtime             | cid_name         | cid_num | exten | context | channame            | uniqueid      | linkedid     | userfield |
            | CHAN_START   | 2013-12-04 14:20:58.0 | Neelix Talaxian  | 1066    | 1624  | default | SIP/2dvtpb-00000009 | 1386184858.9  | 1386184858.9 |           |
            | APP_START    | 2013-12-04 14:20:58.1 | Neelix Talaxian  | 1066    | s     | user    | SIP/2dvtpb-00000009 | 1386184858.9  | 1386184858.9 |           |
            | CHAN_START   | 2013-12-04 14:20:58.2 | Donald MacRonald | 1624    | s     | default | SIP/zsp7wv-0000000a | 1386184858.10 | 1386184858.9 |           |
            | ANSWER       | 2013-12-04 14:21:05.3 | Donald MacRonald | 1624    | s     | default | SIP/zsp7wv-0000000a | 1386184858.10 | 1386184858.9 |           |
            | ANSWER       | 2013-12-04 14:21:05.4 | Neelix Talaxian  | 1066    | s     | user    | SIP/2dvtpb-00000009 | 1386184858.9  | 1386184858.9 |           |
            | BRIDGE_START | 2013-12-04 14:21:05.5 | Neelix Talaxian  | 1066    | s     | user    | SIP/2dvtpb-00000009 | 1386184858.9  | 1386184858.9 |           |
            | BRIDGE_END   | 2013-12-04 14:21:06.6 | Neelix Talaxian  | 1066    | s     | user    | SIP/2dvtpb-00000009 | 1386184858.9  | 1386184858.9 |           |
            | HANGUP       | 2013-12-04 14:21:06.7 | Donald MacRonald | 1624    |       | user    | SIP/zsp7wv-0000000a | 1386184858.10 | 1386184858.9 |           |
            | CHAN_END     | 2013-12-04 14:21:06.8 | Donald MacRonald | 1624    |       | user    | SIP/zsp7wv-0000000a | 1386184858.10 | 1386184858.9 |           |
            | HANGUP       | 2013-12-04 14:21:06.9 | Neelix Talaxian  | 1066    | s     | user    | SIP/2dvtpb-00000009 | 1386184858.9  | 1386184858.9 |           |
            | CHAN_END     | 2013-12-04 14:21:07.1 | Neelix Talaxian  | 1066    | s     | user    | SIP/2dvtpb-00000009 | 1386184858.9  | 1386184858.9 |           |
            | LINKEDID_END | 2013-12-04 14:21:07.2 | Neelix Talaxian  | 1066    | s     | user    | SIP/2dvtpb-00000009 | 1386184858.9  | 1386184858.9 |           |
        When I generate call logs
        Then I should have the following call logs:
            | date                  | date_answer           | date_end              | source_name     | source_exten | destination_exten | user_field | source_line_identity | destination_line_identity |
            | 2013-12-04 14:20:58.0 | 2013-12-04 14:21:05.5 | 2013-12-04 14:21:07.1 | Neelix Talaxian |         1066 |              1624 |            | sip/2dvtpb           | sip/zsp7wv                |
