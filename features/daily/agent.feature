Feature: Agent

  Scenario: Login and logout an agent from the phone
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | agent_number |
      | User      | 003      | 1003  | default | 1003         |
    When I log agent "1003" from phone
    When I wait "3" seconds for the call processing
    Then the agent "1003" is logged
    When I unlog agent "1003" from phone
    When I wait "3" seconds for the call processing
    Then the agent "1003" is not logged

  Scenario: Toggle agent status from the phone
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | agent_number |
      | User      | 003      | 1003  | default | 1003         |
    When I toggle agent "1003" status from phone
    When I wait "3" seconds for the call processing
    Then the agent "1003" is logged
    When I toggle agent "1003" status from phone
    When I wait "3" seconds for the call processing
    Then the agent "1003" is not logged

  Scenario: Assign agent penalty
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | agent_number |
      | James     | Bond     | 1801  | default |              |
      | Ti-Me     | Pare     | 1802  | default | 1802         |
      | Moman     | Pare     | 1803  | default | 1803         |
    Given there are queues with infos:
      | name | label | exten | context |
      | Pare | House | 3801  | default |
    Given queue "Pare" has agent "1802" with penalty "1"
    Given queue "Pare" has agent "1803" with penalty "5"
    Given agent "1802" is logged
    Given agent "1803" is logged
    When "James Bond" calls "3801"
    When I wait "1" seconds for the call processing
    Then "Ti-Me Pare" is ringing
    Then "Moman Pare" is hungup
    When "Ti-Me Pare" hangs up
    Then "Moman Pare" is ringing
    Given "James Bond" hangs up
    When "James Bond" calls "3801"
    When I wait "1" seconds for the call processing
    When "Ti-Me Pare" answers
    When "James Bond" calls "3801"
    When I wait "1" seconds for the call processing
    Then "Ti-Me Pare" is talking
    Then "Moman Pare" is ringing
