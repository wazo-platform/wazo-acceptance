Feature: Voicemail

  Scenario: Leave voicemail message
    Given there are telephony users with infos:
      | firstname | lastname | number | context | voicemail_name | voicemail_number | voicemail_context |
      | George    | Hanson   | 1801   | default | George Hanson  | 1801             | default           |
    Given I listen on the bus for "user_voicemail_message_created" messages
    When a message is left on voicemail "1801@default" by "Billy"
    Then I receive a voicemail message event "user_voicemail_message_created" with data:
      | caller_id_name | folder_name | folder_type |
      | Billy          | inbox       | new         |
    Then there's the following messages in voicemail "1801@default"
      | caller_id_name | folder_name | folder_type |
      | Billy          | inbox       | new         |

  Scenario: Check voicemail message
    Given there are telephony users with infos:
      | firstname | lastname | number | context | voicemail_name | voicemail_number | voicemail_context |
      | George    | Hanson   | 1801   | default | George Hanson  | 1801             | default           |
    Given I listen on the bus for "user_voicemail_message_updated" messages
    When a message is left on voicemail "1801@default" by "Billy"
    When a message is checked and kept on voicemail "1801@default"
    Then I receive a voicemail message event "user_voicemail_message_updated" with data:
      | caller_id_name | folder_name | folder_type |
      | Billy          | old         | old         |
    Then there's the following messages in voicemail "1801@default"
      | caller_id_name | folder_name | folder_type |
      | Billy          | old         | old         |

  Scenario: Delete voicemail message
    Given there are telephony users with infos:
      | firstname | lastname | number | context | voicemail_name | voicemail_number | voicemail_context |
      | George    | Hanson   | 1801   | default | George Hanson  | 1801             | default           |
    Given I listen on the bus for "user_voicemail_message_deleted" messages
    When a message is left on voicemail "1801@default" by "Billy"
    When a message is checked and deleted on voicemail "1801@default"
    Then I receive a voicemail message event "user_voicemail_message_deleted" with data:
      | caller_id_name | folder_name | folder_type |
      | Billy          | inbox       | new         |
    Then there's no message in voicemail "1801@default"
