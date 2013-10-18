Feature: CEL webservice

    Scenario: Access to the webservice
        Given I have only the following CEL entries:
            | eventtype    | eventtime                  | cid_name      | cid_num | exten | context | uniqueid     | linkedid     | userfield |
            | CHAN_START   | 2013-01-01 08:46:20.118025 | Bob Marley    | 1002    | 1001  | default | 1375994780.1 | 1375994780.1 |           |
            | APP_START    | 2013-01-01 08:46:20.156126 | Bob Marley    | 1002    | s     | user    | 1375994780.1 | 1375994780.1 |           |
            | CHAN_START   | 2013-01-01 08:46:20.156385 | Alice Aglisse | 1001    | s     | default | 1375994780.2 | 1375994780.1 |           |
            | ANSWER       | 2013-01-01 08:46:23.005457 | Alice Aglisse | 1001    | s     | default | 1375994780.2 | 1375994780.1 |           |
            | ANSWER       | 2013-01-01 08:46:23.005613 | Bob Marley    | 1002    | s     | user    | 1375994780.1 | 1375994780.1 |           |
            | BRIDGE_START | 2013-01-01 08:46:23.005632 | Bob Marley    | 1002    | s     | user    | 1375994780.1 | 1375994780.1 |           |
            | BRIDGE_END   | 2013-01-01 08:46:26.848705 | Bob Marley    | 1002    | s     | user    | 1375994780.1 | 1375994780.1 |           |
            | HANGUP       | 2013-01-01 08:46:26.849811 | Alice Aglisse | 1001    |       | user    | 1375994780.2 | 1375994780.1 |           |
            | CHAN_END     | 2013-01-01 08:46:26.84983  | Alice Aglisse | 1001    |       | user    | 1375994780.2 | 1375994780.1 |           |
            | HANGUP       | 2013-01-01 08:46:26.860098 | Bob Marley    | 1002    | s     | user    | 1375994780.1 | 1375994780.1 |           |
            | CHAN_END     | 2013-01-01 08:46:26.860247 | Bob Marley    | 1002    | s     | user    | 1375994780.1 | 1375994780.1 |           |
            | LINKEDID_END | 2013-01-01 08:46:26.860254 | Bob Marley    | 1002    | s     | user    | 1375994780.1 | 1375994780.1 |           |
        When I ask for the list of CEL via WebService:
            | start date |   end date |
            | 2013-01-01 | 2013-01-01 |
        Then I get a list with the following CEL:
            | eventtype    | eventtime                  | cid_name      | cid_num | exten | context |     uniqueid |     linkedid | userfield |
            | CHAN_START   | 2013-01-01 08:46:20.118025 | Bob Marley    |    1002 | 1001  | default | 1375994780.1 | 1375994780.1 |           |
            | APP_START    | 2013-01-01 08:46:20.156126 | Bob Marley    |    1002 | s     | user    | 1375994780.1 | 1375994780.1 |           |
            | CHAN_START   | 2013-01-01 08:46:20.156385 | Alice Aglisse |    1001 | s     | default | 1375994780.2 | 1375994780.1 |           |
            | ANSWER       | 2013-01-01 08:46:23.005457 | Alice Aglisse |    1001 | s     | default | 1375994780.2 | 1375994780.1 |           |
            | ANSWER       | 2013-01-01 08:46:23.005613 | Bob Marley    |    1002 | s     | user    | 1375994780.1 | 1375994780.1 |           |
            | BRIDGE_START | 2013-01-01 08:46:23.005632 | Bob Marley    |    1002 | s     | user    | 1375994780.1 | 1375994780.1 |           |
            | BRIDGE_END   | 2013-01-01 08:46:26.848705 | Bob Marley    |    1002 | s     | user    | 1375994780.1 | 1375994780.1 |           |
            | HANGUP       | 2013-01-01 08:46:26.849811 | Alice Aglisse |    1001 |       | user    | 1375994780.2 | 1375994780.1 |           |
            | CHAN_END     | 2013-01-01 08:46:26.84983  | Alice Aglisse |    1001 |       | user    | 1375994780.2 | 1375994780.1 |           |
            | HANGUP       | 2013-01-01 08:46:26.860098 | Bob Marley    |    1002 | s     | user    | 1375994780.1 | 1375994780.1 |           |
            | CHAN_END     | 2013-01-01 08:46:26.860247 | Bob Marley    |    1002 | s     | user    | 1375994780.1 | 1375994780.1 |           |
            | LINKEDID_END | 2013-01-01 08:46:26.860254 | Bob Marley    |    1002 | s     | user    | 1375994780.1 | 1375994780.1 |           |
