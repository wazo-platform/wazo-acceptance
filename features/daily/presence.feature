Feature: Presence updated

  Scenario: Presence sessions are updated
    Given there are telephony users with infos:
      | firstname | lastname | username | password |
      | James     | Bond     | jbond    | secret   |
    Given I listen on the bus for "chatd_presence_updated" messages
    When I create a session with username "jbond" password "secret"
    Then I receive a "chatd_presence_updated" event
    Then "James Bond" has "1" session in his presence

  Scenario: Presence line state is updated
    Given there are telephony users with infos:
      | firstname | lastname | exten  | context |
      | James     | Bond     | 1801   | default |
    Given I listen on the bus for "chatd_presence_updated" messages
    When "James Bond" calls "*10"
    Then I receive a "chatd_presence_updated" event with data:
      | line_state |
      | talking    |
    Then "James Bond" has his line state to "talking"
