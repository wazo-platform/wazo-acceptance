Feature: Do Not Disturb
  Scenario: Test
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | ring_seconds |
      | Alice     | 1100     | 1100  | default |      5       |
      | Bob       | 1101     | 1101  | default |      10      |
    Given "Bob 1101" has enabled "dnd" service
    When "Alice 1100" calls "1101"
    Then "Alice 1100" is hungup immediately

  Scenario: Direct call to user in DND status
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | ring_seconds | voicemail_name | voicemail_number | voicemail_context |
      | Alice     | 1100     | 1100  | default |      5       |                |                  |                   |
      | Bob       | 1101     | 1101  | default |      5       | Bob            |  1101            | default           |
    Given "Bob 1101" has enabled "dnd" service
    Given I listen on the bus for "MessageWaiting" messages
    When "Alice 1100" calls "1101" and waits for "30" seconds
    When "Alice 1100" hangs up
    Then I receive a "MessageWaiting" event with data:
      | Mailbox      | Waiting |
      | 1101@default | 1       |

  Scenario: call to user in DND status with no-answer forwarding enabled
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | ring_seconds | voicemail_name | voicemail_number | voicemail_context |
      | Alice     | 1100     | 1100  | default |      5       |                |                  |                   |
      | Bob       | 1101     | 1101  | default |      5       | Bob            |  1101            | default           |
      | Charlie   | 1102     | 1102  | default |      5       | Charlie        |  1102            | default           |
    Given "Bob 1101" has enabled "dnd" service
    Given I listen on the bus for "MessageWaiting" messages
    When "Bob 1101" enable forwarding on no-answer to "1102"
    When "Alice 1100" calls "1101" and waits for "30" seconds
    When "Alice 1100" hangs up
    Then I receive a "MessageWaiting" event with data:
      | Mailbox      | Waiting |
      | 1101@default | 1       |

  Scenario: call to user with no-answer forwarding enabled with forwarded callee in DND status
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | ring_seconds | voicemail_name | voicemail_number | voicemail_context |
      | Alice     | 1100     | 1100  | default |      5       |                |                  |                   |
      | Bob       | 1101     | 1101  | default |      5       | Bob            |  1101            | default           |
      | Charlie   | 1102     | 1102  | default |      5       | Charlie        |  1102            | default           |
    Given "Charlie 1102" has enabled "dnd" service
    Given I listen on the bus for "MessageWaiting" messages
    When "Bob 1101" enable forwarding on no-answer to "1102"
    When "Alice 1100" calls "1101" and waits for "30" seconds
    When "Alice 1100" hangs up
    Then I receive a "MessageWaiting" event with data:
      | Mailbox      | Waiting |
      | 1101@default | 1       |
