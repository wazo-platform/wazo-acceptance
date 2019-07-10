Feature: Agent

  Scenario: Login and logout an agent from the phone
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | agent_number | with_phone |
      | User      | 003      | 1003  | default | 1003         | yes        |
    When I log agent "1003" from phone
    When I wait "3" seconds for the call processing
    Then the agent "1003" is logged
    When I unlog agent "1003" from phone
    When I wait "3" seconds for the call processing
    Then the agent "1003" is not logged
