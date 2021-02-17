Feature: User multi lines

  Scenario: Ring all lines of a user
    Given there are telephony users with infos:
      | firstname | lastname | exten  | context |
      | Multi     | Lines    |        |         |
      | Bob       | Field    | 1802   | default |
    Given "Multi Lines" has lines:
      | name  | exten | context | with_phone |
      | line1 | 1801  | default | yes        |
      | line2 | 1801  | default | yes        |
      | line3 |       | default | yes        |
    When "Bob Field" calls "1801"
    Then "Multi Lines" is ringing on its contact "1"
    Then "Multi Lines" is ringing on its contact "2"
    Then "Multi Lines" is hungup on its contact "3"

  Scenario: User multi lines multi extensions
    Given there are telephony users with infos:
      | firstname | lastname | exten | context |
      | Multi     | Lines    |       |         |
      | Bob       | Field    | 1803  | default |
    Given "Multi Lines" has lines:
      | name  | exten | context | with_phone |
      | line1 | 1801  | default | yes        |
      | line2 | 1802  | default | yes        |
    When "Bob Field" calls "1801"
    Then "Multi Lines" is ringing on its contact "1"
    Then "Multi Lines" is hungup on its contact "2"

  Scenario: Activate a forward on user multi lines
    Given there are telephony users with infos:
      | firstname | lastname | exten | context |
      | Multi     | Lines    |       |         |
      | Bob       | Field    | 1802  | default |
      | Forward   | Unc      | 1803  | default |
    Given "Multi Lines" has lines:
      | name  | exten | context | with_phone |
      | line1 | 1801  | default | yes        |
      | line2 | 1801  | default | yes        |
    Given "Multi Lines" has an "unconditional" forward set to "1803"
    When "Bob Field" calls "1801"
    When I wait 4 seconds for the call to be forwarded
    Then "Forward Unc" is ringing

  Scenario: Activate dnd on user multi lines
    Given there are telephony users with infos:
      | firstname | lastname | exten | context |
      | Multi     | Lines    |       |         |
      | Bob       | Field    | 1802  | default |
    Given "Multi Lines" has lines:
      | name  | exten | context | with_phone |
      | line1 | 1801  | default | yes        |
      | line2 | 1801  | default | yes        |
    Given "Multi Lines" has enabled "dnd" service
    When "Bob Field" calls "1801"
    When I wait 2 seconds for the call processing
    When I wait 5 seconds to play unreachable message
    Then "Bob Field" is hungup

  Scenario: Ringing time are respected on user multi lines
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | ring_seconds |
      | Multi     | Lines    |       |         | 5            |
      | Bob       | Field    | 1802  | default |              |
    Given "Multi Lines" has lines:
      | name  | exten | context | with_phone |
      | line1 | 1801  | default | yes        |
      | line2 | 1801  | default | yes        |
    When "Bob Field" calls "1801"
    Then "Multi Lines" is ringing on its contact "1"
    Then "Multi Lines" is ringing on its contact "2"
    When I wait 5 seconds for the end of ringing time
    Then "Multi Lines" is hungup on its contact "1"
    Then "Multi Lines" is hungup on its contact "2"
    When I wait 5 seconds for the call processing
    Then "Bob Field" is hungup

  Scenario: Incoming call rings all lines that have the same extension as the main line
    Given there are telephony users with infos:
      | firstname | lastname |
      | Multi     | Lines    |
    Given "Multi Lines" has lines:
      | name  | exten | context | with_phone |
      | line1 | 1801  | default | yes        |
      | line2 | 1801  | default | yes        |
      | line3 | 1802  | default | yes        |
    Given there is an incall "1801@from-extern" to the user "Multi Lines"
    When chan_test calls "1801@from-extern"
    Then "Multi Lines" is ringing on its contact "1"
    Then "Multi Lines" is ringing on its contact "2"
    Then "Multi Lines" is hungup on its contact "3"
