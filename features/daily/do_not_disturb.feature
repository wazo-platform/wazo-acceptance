Feature: Do Not Disturb
  Scenario: Call to user in DND status hangs up quickly
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | ring_seconds |
      | Alice     | 1100     | 1100  | default |      5       |
      | Bob       | 1101     | 1101  | default |      10      |
    Given "Bob 1101" has enabled "dnd" service
    When "Alice 1100" calls "1101"
    Then "Alice 1100" is hungup immediately

  Scenario: Direct call to user in DND status with voicemail
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | ring_seconds | voicemail_name | voicemail_number | voicemail_context |
      | Alice     | 1100     | 1100  | default |      5       |                |                  |                   |
      | Bob       | 1101     | 1101  | default |      5       | Bob            |  1101            | default           |
    Given "Bob 1101" has enabled "dnd" service
    Given I listen on the bus for "MessageWaiting" messages
    When "Alice 1100" calls "1101"
    When I wait 5 seconds for the timeout to expire
    When I wait 2 seconds for the call processing
    When I wait 20 seconds to play message
    When "Alice 1100" hangs up
    Then I receive a MessageWaiting event with "1" messages for mailbox "1101@default"

  Scenario: call to user in DND status with no-answer forwarding redirects to correct voicemail
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | ring_seconds | voicemail_name | voicemail_number | voicemail_context |
      | Alice     | 1100     | 1100  | default |      5       |                |                  |                   |
      | Bob       | 1101     | 1101  | default |      5       | Bob            |  1101            | default           |
      | Charlie   | 1102     | 1102  | default |      5       | Charlie        |  1102            | default           |
    Given "Bob 1101" has enabled "dnd" service
    Given I listen on the bus for "MessageWaiting" messages
    Given "Bob 1101" enable forwarding on no-answer to "1102"
    When "Alice 1100" calls "1101"
    When I wait 5 seconds for the timeout to expire
    When I wait 2 seconds for the call processing
    When I wait 20 seconds to play message
    When "Alice 1100" hangs up
    Then I receive a MessageWaiting event with "1" messages for mailbox "1101@default"

  Scenario: call to user with no-answer forwarding to user in DND status redirects to correct voicemail
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | ring_seconds | voicemail_name | voicemail_number | voicemail_context |
      | Alice     | 1100     | 1100  | default |      5       |                |                  |                   |
      | Bob       | 1101     | 1101  | default |      5       | Bob            |  1101            | default           |
      | Charlie   | 1102     | 1102  | default |      5       | Charlie        |  1102            | default           |
    Given "Charlie 1102" has enabled "dnd" service
    Given I listen on the bus for "MessageWaiting" messages
    Given "Bob 1101" enable forwarding on no-answer to "1102"
    When "Alice 1100" calls "1101"
    When I wait 5 seconds for the timeout to expire
    When I wait 2 seconds for the call processing
    When I wait 20 seconds to play message
    When "Alice 1100" hangs up
    Then I receive a MessageWaiting event with "1" messages for mailbox "1101@default"
