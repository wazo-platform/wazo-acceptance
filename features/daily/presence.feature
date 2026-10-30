Feature: Presence updated

  Scenario: Presence connected are updated
    Given there are telephony users with infos:
      | firstname | lastname | username | password |
      | James     | Bond     | jbond    | secret   |
    Given I listen on the bus for "chatd_presence_updated" messages
    When I create a session with username "jbond" password "secret"
    Then I receive a "chatd_presence_updated" event
    Then "James Bond" has their presence connected

  Scenario: Presence line state is updated
    Given there are telephony users with infos:
      | firstname | lastname | exten | context |
      | James     | Bond     | 1801  | default |
    Given I listen on the bus for "chatd_presence_updated" messages
    When "James Bond" calls "*10"
    Then I receive a "chatd_presence_updated" event with data:
      | line_state |
      | talking    |
    Then "James Bond" has their line state to "talking"

  Scenario: Presence line holding state
    Given there are telephony users with infos:
      | firstname | lastname | exten | context |
      | James     | Bond     | 1801  | default |
      | Ti-Me     | Pare     | 1802  | default |
    Given "James Bond" calls "1802"
    Given "Ti-Me Pare" answers
    Given I listen on the bus for "chatd_presence_updated" messages
    When "Ti-Me Pare" puts their call on hold
    Then I receive a "chatd_presence_updated" event with data:
      | line_state |
      | holding    |
    Then "Ti-Me Pare" has their line state to "holding"
    Then "James Bond" has their line state to "talking"
    When "Ti-Me Pare" resumes their call
    Then I receive a "chatd_presence_updated" event with data:
      | line_state |
      | talking    |
    Then "Ti-Me Pare" has their line state to "talking"
    Then "James Bond" has their line state to "talking"
