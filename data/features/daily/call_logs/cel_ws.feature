Feature: CEL webservice

    @skip_old_webi_step
    Scenario: Access to the webservice
        Given I have only the following CEL entries:
            | id | eventtype    | eventtime                  | cid_name      | cid_num | exten | context | uniqueid     | linkedid     | userfield |
            | 1  | CHAN_START   | 2013-01-01 08:46:20.118025 | Bob Marley    | 1002    | 1001  | default | 1375994780.1 | 1375994780.1 |           |
            | 2  | APP_START    | 2013-01-01 08:46:20.156126 | Bob Marley    | 1002    | s     | user    | 1375994780.1 | 1375994780.1 |           |
            | 3  | CHAN_START   | 2013-01-01 08:46:20.156385 | Alice Aglisse | 1001    | s     | default | 1375994780.2 | 1375994780.1 |           |
            | 4  | ANSWER       | 2013-01-01 08:46:23.005457 | Alice Aglisse | 1001    | s     | default | 1375994780.2 | 1375994780.1 |           |
        When I ask for the list of CEL via WebService:
            | id beg |
            | 2      |
        Then I get a list with the following CEL:
            | id | eventtype    | eventtime                  | cid_name      | cid_num | exten | context |     uniqueid |     linkedid | userfield |
            | 3  | CHAN_START   | 2013-01-01 08:46:20.156385 | Alice Aglisse | 1001    | s     | default | 1375994780.2 | 1375994780.1 |           |
            | 4  | ANSWER       | 2013-01-01 08:46:23.005457 | Alice Aglisse | 1001    | s     | default | 1375994780.2 | 1375994780.1 |           |
