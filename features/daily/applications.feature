Feature: Application

  Scenario: Base application creation
    Given there are telephony users with infos:
      | firstname | exten | context | with_phone |
      | Alice     |  1001 | default | yes        |
    Given there are applications with infos:
      | name  | destination | destination_type |
      | zeapp | node        | holding          |
    Given there is an incall "1700@from-extern" to the application "zeapp"
    When chan_test calls "1700@from-extern"
    When "Alice" picks up the call from the application "zeapp"
    Then "zeapp" contains a node with "2" calls

  Scenario: Line application
    Given there are applications with infos:
      | name  | destination | destination_type |
      | MyApp | node        | holding          |
    Given there are telephony users with infos:
      | firstname | exten | context | application | with_phone |
      | Alice     |  1001 | default |             | yes        |
      | Bob       |  1002 | default | MyApp       | yes        |
    When "Bob" calls "123"
    When "Alice" picks up the call from the application "MyApp"
    Then "MyApp" contains a node with "2" calls
