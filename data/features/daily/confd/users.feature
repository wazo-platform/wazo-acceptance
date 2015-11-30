Feature: REST API Users

    Scenario: User list with directory view
        Given there are users with infos:
        | firstname | lastname  | mobile_number | number | context | protocol | agent_number |
        | Albert    | Montoya   |               |        |         |          |              |
        | Greg      | Sanderson |  +14184765458 |   1103 | default | sip      |              |
        | Bob       | Marley    |  +12345678910 |   1104 | default | sip      |        24002 |
        When I ask for the list of users with view "directory"
        Then I get a list containing the following users with view directory:
        | id  | firstname | lastname  | exten | mobile_phone_number | line_id | agent_id |
        | yes | Albert    | Montoya   |       |                     | no      | no       |
        | yes | Greg      | Sanderson |  1103 |        +14184765458 | yes     | no       |
        | yes | Bob       | Marley    |  1104 |        +12345678910 | yes     | yes      |
