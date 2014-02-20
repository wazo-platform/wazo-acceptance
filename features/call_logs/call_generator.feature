Feature: Call Log Generation

    Scenario: Generation of answered internal call
        Given there are no call logs
        Given I have only the following CEL entries:
            | eventtype    | eventtime                  | cid_name      | cid_num | exten | context | channame            |     uniqueid |     linkedid | userfield |
            | CHAN_START   | 2013-01-01 08:46:20.118025 | Bob Marley    |    1002 | 1001  | default | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |
            | APP_START    | 2013-01-01 08:46:20.156126 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |
            | CHAN_START   | 2013-01-01 08:46:20.156385 | Alice Aglisse |    1001 | s     | default | SIP/hg63xv-00000013 | 1375994780.2 | 1375994780.1 |           |
            | ANSWER       | 2013-01-01 08:46:23.005457 | Alice Aglisse |    1001 | s     | default | SIP/hg63xv-00000013 | 1375994780.2 | 1375994780.1 |           |
            | ANSWER       | 2013-01-01 08:46:23.005613 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |
            | BRIDGE_START | 2013-01-01 08:46:23.005632 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |
            | BRIDGE_END   | 2013-01-01 08:46:26.848705 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |
            | HANGUP       | 2013-01-01 08:46:26.849811 | Alice Aglisse |    1001 |       | user    | SIP/hg63xv-00000013 | 1375994780.2 | 1375994780.1 |           |
            | CHAN_END     | 2013-01-01 08:46:26.84983  | Alice Aglisse |    1001 |       | user    | SIP/hg63xv-00000013 | 1375994780.2 | 1375994780.1 |           |
            | HANGUP       | 2013-01-01 08:46:26.860098 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |
            | CHAN_END     | 2013-01-01 08:46:26.860247 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |
            | LINKEDID_END | 2013-01-01 08:46:26.860254 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994780.1 | 1375994780.1 |           |
        When I generate call logs
        Then I should have the following call logs:
            | date                       | source_name | source_exten | destination_exten |       duration | user_field | answered | source_line_identity | destination_line_identity |
            | 2013-01-01 08:46:20.118025 | Bob Marley  |         1002 |              1001 | 0:00:03.854485 |            | True     | sip/z77kvm           | sip/hg63xv                |

    Scenario: Generation of non-answered internal call
        Given there are no call logs
        Given I have only the following CEL entries:
            | eventtype    | eventtime                  | cid_name      | cid_num | exten | context | channame            |     uniqueid |     linkedid | userfield |
            | CHAN_START   | 2013-01-01 08:46:31.981    | Bob Marley    |    1002 | 1001  | default | SIP/z77kvm-00000028 | 1375994791.3 | 1375994791.3 |           |
            | APP_START    | 2013-01-01 08:46:32.016612 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994791.3 | 1375994791.3 |           |
            | CHAN_START   | 2013-01-01 08:46:32.016872 | Alice Aglisse |    1001 | s     | default | SIP/hg63xv-00000013 | 1375994792.4 | 1375994791.3 |           |
            | HANGUP       | 2013-01-01 08:46:36.327564 | Alice Aglisse |    1001 | s     | default | SIP/hg63xv-00000013 | 1375994792.4 | 1375994791.3 |           |
            | CHAN_END     | 2013-01-01 08:46:36.32762  | Alice Aglisse |    1001 | s     | default | SIP/hg63xv-00000013 | 1375994792.4 | 1375994791.3 |           |
            | HANGUP       | 2013-01-01 08:46:36.327692 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994791.3 | 1375994791.3 |           |
            | CHAN_END     | 2013-01-01 08:46:36.327704 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994791.3 | 1375994791.3 |           |
            | LINKEDID_END | 2013-01-01 08:46:36.327708 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1375994791.3 | 1375994791.3 |           |
        When I generate call logs
        Then I should have the following call logs:
            | date                    | source_name | source_exten | destination_exten | duration | user_field | answered | source_line_identity | destination_line_identity |
            | 2013-01-01 08:46:31.981 | Bob Marley  |         1002 |              1001 |        0 |            | False    | sip/z77kvm           | sip/hg63xv                |

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
            | date                  | source_name | source_exten | destination_exten |  duration | user_field | answered | source_line_identity | destination_line_identity |
            | 2013-01-01 11:02:38.0 |   612345678 |    612345678 |              1002 | 0:00:03.0 |            | True     | sip/trunk            | sip/hg63xv                |

    Scenario: Generation of answered outgoing call
        Given there are no call logs
        Given I have only the following CEL entries:
            | eventtype    | eventtime             | cid_name   | cid_num | exten      | context     | channame            |      uniqueid |      linkedid | userfield |
            | CHAN_START   | 2013-01-01 11:03:47.0 | Bob Marley |    1002 | 4185550155 | default     | SIP/z77kvm-00000028 | 1376060627.21 | 1376060627.21 |           |
            | APP_START    | 2013-01-01 11:03:47.1 | Bob Marley |    1002 | dial       | outcall     | SIP/z77kvm-00000028 | 1376060627.21 | 1376060627.21 |           |
            | CHAN_START   | 2013-01-01 11:03:47.2 |            |         | s          | from-extern | SIP/trunk-00000013  | 1376060627.22 | 1376060627.21 |           |
            | ANSWER       | 2013-01-01 11:03:51.0 |            |    dial | dial       | from-extern | SIP/trunk-00000013  | 1376060627.22 | 1376060627.21 |           |
            | ANSWER       | 2013-01-01 11:03:51.1 | Bob Marley |    1002 | dial       | outcall     | SIP/z77kvm-00000028 | 1376060627.21 | 1376060627.21 |           |
            | BRIDGE_START | 2013-01-01 11:03:51.2 | Bob Marley |    1002 | dial       | outcall     | SIP/z77kvm-00000028 | 1376060627.21 | 1376060627.21 |           |
            | BRIDGE_END   | 2013-01-01 11:03:54.0 | Bob Marley |    1002 | dial       | outcall     | SIP/z77kvm-00000028 | 1376060627.21 | 1376060627.21 |           |
            | HANGUP       | 2013-01-01 11:03:54.1 |            |    dial |            | outcall     | SIP/trunk-00000013  | 1376060627.22 | 1376060627.21 |           |
            | CHAN_END     | 2013-01-01 11:03:54.2 |            |    dial |            | outcall     | SIP/trunk-00000013  | 1376060627.22 | 1376060627.21 |           |
            | HANGUP       | 2013-01-01 11:03:54.3 | Bob Marley |    1002 | dial       | outcall     | SIP/z77kvm-00000028 | 1376060627.21 | 1376060627.21 |           |
            | CHAN_END     | 2013-01-01 11:03:54.4 | Bob Marley |    1002 | dial       | outcall     | SIP/z77kvm-00000028 | 1376060627.21 | 1376060627.21 |           |
            | LINKEDID_END | 2013-01-01 11:03:54.5 | Bob Marley |    1002 | dial       | outcall     | SIP/z77kvm-00000028 | 1376060627.21 | 1376060627.21 |           |
            | CHAN_START   | 2013-01-01 11:20:08.0 | Bob Marley |    1002 | 4185550155 | default     | SIP/z77kvm-00000028 | 1376068808.35 | 1376068808.35 |           |
            | APP_START    | 2013-01-01 11:20:08.1 | Bob Marley |    1002 | dial       | outcall     | SIP/z77kvm-00000028 | 1376068808.35 | 1376068808.35 | Père Noël |
            | CHAN_START   | 2013-01-01 11:20:08.2 |            |         | s          | from-extern | SIP/trunk-00000013  | 1376068808.36 | 1376068808.35 |           |
            | ANSWER       | 2013-01-01 11:20:10.0 |            |    dial | dial       | from-extern | SIP/trunk-00000013  | 1376068808.36 | 1376068808.35 |           |
            | ANSWER       | 2013-01-01 11:20:10.1 | Bob Marley |    1002 | dial       | outcall     | SIP/z77kvm-00000028 | 1376068808.35 | 1376068808.35 | Père Noël |
            | BRIDGE_START | 2013-01-01 11:20:10.2 | Bob Marley |    1002 | dial       | outcall     | SIP/z77kvm-00000028 | 1376068808.35 | 1376068808.35 | Père Noël |
            | BRIDGE_END   | 2013-01-01 11:20:13.0 | Bob Marley |    1002 | dial       | outcall     | SIP/z77kvm-00000028 | 1376068808.35 | 1376068808.35 | Père Noël |
            | HANGUP       | 2013-01-01 11:20:13.1 |            |    dial |            | outcall     | SIP/trunk-00000013  | 1376068808.36 | 1376068808.35 |           |
            | CHAN_END     | 2013-01-01 11:20:13.2 |            |    dial |            | outcall     | SIP/trunk-00000013  | 1376068808.36 | 1376068808.35 |           |
            | HANGUP       | 2013-01-01 11:20:13.3 | Bob Marley |    1002 | dial       | outcall     | SIP/z77kvm-00000028 | 1376068808.35 | 1376068808.35 | Père Noël |
            | CHAN_END     | 2013-01-01 11:20:13.4 | Bob Marley |    1002 | dial       | outcall     | SIP/z77kvm-00000028 | 1376068808.35 | 1376068808.35 | Père Noël |
            | LINKEDID_END | 2013-01-01 11:20:13.5 | Bob Marley |    1002 | dial       | outcall     | SIP/z77kvm-00000028 | 1376068808.35 | 1376068808.35 | Père Noël |
        When I generate call logs
        Then I should have the following call logs:
            | date                  | source_name | source_exten | destination_exten |  duration | user_field | answered | source_line_identity | destination_line_identity |
            | 2013-01-01 11:03:47.0 | Bob Marley  |         1002 |        4185550155 | 0:00:03.0 |            | True     | sip/z77kvm           | sip/trunk                 |
            | 2013-01-01 11:20:08.0 | Bob Marley  |         1002 |        4185550155 | 0:00:03.0 | Père Noël  | True     | sip/z77kvm           | sip/trunk                 |

    Scenario: Generation of originate call
        Given there are no call logs
        Given I have only the following CEL entries:
            | eventtype    | eventtime             | cid_name      | cid_num | exten | context | channame            |       uniqueid |       linkedid | userfield |
            | CHAN_START   | 2013-01-01 15:47:39.0 | Bob Marley    |    1002 | s     | default | SIP/z77kvm-00000028 | 1379101659.670 | 1379101659.670 |           |
            | ANSWER       | 2013-01-01 15:47:40.0 | 1001          |    1001 |       | default | SIP/z77kvm-00000028 | 1379101659.670 | 1379101659.670 |           |
            | APP_START    | 2013-01-01 15:47:41.0 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1379101659.670 | 1379101659.670 |           |
            | CHAN_START   | 2013-01-01 15:47:41.1 | Alice Aglisse |    1001 | s     | default | SIP/hg63xv-00000013 | 1379101661.671 | 1379101659.670 |           |
            | ANSWER       | 2013-01-01 15:47:42.0 | Alice Aglisse |    1001 | s     | default | SIP/hg63xv-00000013 | 1379101661.671 | 1379101659.670 |           |
            | BRIDGE_START | 2013-01-01 15:47:42.1 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1379101659.670 | 1379101659.670 |           |
            | BRIDGE_END   | 2013-01-01 15:47:44.0 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1379101659.670 | 1379101659.670 |           |
            | HANGUP       | 2013-01-01 15:47:44.1 | Alice Aglisse |    1001 |       | user    | SIP/hg63xv-00000013 | 1379101661.671 | 1379101659.670 |           |
            | CHAN_END     | 2013-01-01 15:47:44.2 | Alice Aglisse |    1001 |       | user    | SIP/hg63xv-00000013 | 1379101661.671 | 1379101659.670 |           |
            | HANGUP       | 2013-01-01 15:47:44.3 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1379101659.670 | 1379101659.670 |           |
            | CHAN_END     | 2013-01-01 15:47:44.4 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1379101659.670 | 1379101659.670 |           |
            | LINKEDID_END | 2013-01-01 15:47:44.5 | Bob Marley    |    1002 | s     | user    | SIP/z77kvm-00000028 | 1379101659.670 | 1379101659.670 |           |
        When I generate call logs
        Then I should have the following call logs:
            | date                  | source_name | source_exten | destination_exten |  duration | user_field | answered | source_line_identity | destination_line_identity |
            | 2013-01-01 15:47:39.0 | Bob Marley  |         1002 |              1001 | 0:00:02.1 |            | True     | sip/z77kvm           | sip/hg63xv                |

    Scenario: Generation of unanswered originate call
        Given there are no call logs
        Given I have only the following CEL entries:
            | eventtype    | eventtime                  | cid_name | cid_num | exten | context | channame            |     uniqueid |     linkedid | userfield |
            | CHAN_START   | 2014-02-20 08:53:12.914145 | Carlos   |    1003 | s     | pcmdev  | SIP/d49t0y-00000001 | 1392904392.1 | 1392904392.1 |           |
            | ANSWER       | 2014-02-20 08:53:13.394103 | 1002     |    1002 |       | pcmdev  | SIP/d49t0y-00000001 | 1392904392.1 | 1392904392.1 |           |
            | APP_START    | 2014-02-20 08:53:13.510263 | Carlos   |    1003 | s     | user    | SIP/d49t0y-00000001 | 1392904392.1 | 1392904392.1 |           |
            | CHAN_START   | 2014-02-20 08:53:13.510397 | Bõb      |    1002 | s     | pcmdev  | SCCP/1002-00000000  | 1392904393.2 | 1392904392.1 |           |
            | HANGUP       | 2014-02-20 08:53:20.196726 | Bõb      |    1002 | s     | pcmdev  | SCCP/1002-00000000  | 1392904393.2 | 1392904392.1 |           |
            | CHAN_END     | 2014-02-20 08:53:20.1975   | Bõb      |    1002 | s     | pcmdev  | SCCP/1002-00000000  | 1392904393.2 | 1392904392.1 |           |
            | HANGUP       | 2014-02-20 08:53:20.197711 | Carlos   |    1003 | s     | user    | SIP/d49t0y-00000001 | 1392904392.1 | 1392904392.1 |           |
            | CHAN_END     | 2014-02-20 08:53:20.19851  | Carlos   |    1003 | s     | user    | SIP/d49t0y-00000001 | 1392904392.1 | 1392904392.1 |           |
            | LINKEDID_END | 2014-02-20 08:53:20.198528 | Carlos   |    1003 | s     | user    | SIP/d49t0y-00000001 | 1392904392.1 | 1392904392.1 |           |
        When I generate call logs
        Then I should have the following call logs:
            | date                       | source_name | source_exten | destination_exten | duration | user_field | answered | source_line_identity | destination_line_identity |
            | 2014-02-20 08:53:12.914145 | Carlos      |         1003 |              1002 |        0 |            | False    | sip/d49t0y           | sccp/1002                 |

     Scenario: Generation for a specified latest CEL count with no processed calls
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
        Then I should have the following call logs:
            | date                | source_name | source_exten | destination_exten | duration | user_field | answered | source_line_identity | destination_line_identity |
            | 2013-01-01 10:00:00 | Bob Marley  |         1002 |              1001 |  0:00:05 |            | True     | sip/z77kvm           | sip/hg63xv                |
        Then I should not have the following call logs:
            | date                | source_name | source_exten | destination_exten | duration | user_field | answered | source_line_identity | destination_line_identity |
            | 2013-01-01 08:00:00 | Bob Marley  |         1002 |              1001 |  0:00:05 |            | True     | sip/z77kvm           | sip/hg63xv                |
            | 2013-01-01 09:00:00 | Bob Marley  |         1002 |              1001 |  0:00:05 |            | True     | sip/z77kvm           | sip/hg63xv                |

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
            | date                | source_name | source_exten | destination_exten | duration | user_field | answered | source_line_identity | destination_line_identity |
            | 2013-01-01 09:00:00 | Bob Marley  |         1002 |              1001 |  0:00:05 |            | True     | sip/z77kvm           | sip/hg63xv                |
            | 2013-01-01 10:00:00 | Bob Marley  |         1002 |              1001 |  0:00:05 |            | True     | sip/z77kvm           | sip/hg63xv                |
        Then I should not have the following call logs:
            | date                | source_name | source_exten | destination_exten | duration | user_field | answered | source_line_identity | destination_line_identity |
            | 2013-01-01 08:00:00 | Bob Marley  |         1002 |              1001 |  0:00:05 |            | True     | sip/z77kvm           | sip/hg63xv                |

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
            | date                | source_name | source_exten | destination_exten | duration | user_field | answered | source_line_identity | destination_line_identity |
            | 2013-01-01 08:00:00 | Bob Marley  |         1002 |              1001 |  0:00:05 |            | True     | sip/z77kvm           | sip/hg63xv                |

     Scenario: Generation of partially processed calls
        Given there are only the following call logs:
            | id | date                | source_name | source_exten | destination_exten | duration | user_field | answered | source_line_identity | destination_line_identity |
            | 42 | 2013-01-01 08:00:00 | Bob Marley  |         1002 |              1001 |  0:00:00 |            | True     | sip/z77kvm           | sip/hg63xv                |
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
            | date                | source_name | source_exten | destination_exten | duration | user_field | answered | source_line_identity | destination_line_identity |
            | 2013-01-01 08:00:00 | Bob Marley  |         1002 |              1001 |  0:00:05 |            | True     | sip/z77kvm           | sip/hg63xv                |

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
            | date                  | source_name     | source_exten | destination_exten | duration  | user_field | answered | source_line_identity | destination_line_identity |
            | 2013-12-04 14:20:58.0 | Neelix Talaxian | 1066         | 1624              | 0:00:01.5 |            | True     | sip/2dvtpb           | sip/zsp7wv                |
