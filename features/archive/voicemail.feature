Feature: Voicemail

    Scenario: Leave voicemail message
        Given there are users with infos:
         | firstname | lastname | number | context | protocol | voicemail_name | voicemail_number | voicemail_context |
         | Geroge    | Hanson   | 1801   | default | sip      | George Hanson  | 1801             | default           |
        Given I listen on the bus for messages:
         | queue           | routing_key                 |
         | test_vm_create  | voicemails.messages.created |
        When a message is left on voicemail "1801@default" by "Billy"
        Then I receive a voicemail message event "user_voicemail_message_created" on the queue "test_vm_create" with data:
         | caller_id_name | folder_name | folder_type |
         | Billy          | inbox       | new         |
        Then there's the following messages in voicemail "1801@default"
         | caller_id_name | folder_name | folder_type |
         | Billy          | inbox       | new         |

    Scenario: Check voicemail message
        Given there are users with infos:
         | firstname | lastname | number | context | protocol | voicemail_name | voicemail_number | voicemail_context |
         | Geroge    | Hanson   | 1801   | default | sip      | George Hanson  | 1801             | default           |
        Given I listen on the bus for messages:
         | queue           | routing_key                 |
         | test_vm_update  | voicemails.messages.updated |
        When a message is left on voicemail "1801@default" by "Billy"
        When a message is checked and kept on voicemail "1801@default"
        Then I receive a voicemail message event "user_voicemail_message_updated" on the queue "test_vm_update" with data:
         | caller_id_name | folder_name | folder_type |
         | Billy          | old         | old         |
        Then there's the following messages in voicemail "1801@default"
         | caller_id_name | folder_name | folder_type |
         | Billy          | old         | old         |

    Scenario: Delete voicemail message
        Given there are users with infos:
         | firstname | lastname | number | context | protocol | voicemail_name | voicemail_number | voicemail_context |
         | Geroge    | Hanson   | 1801   | default | sip      | George Hanson  | 1801             | default           |
        Given I listen on the bus for messages:
         | queue           | routing_key                 |
         | test_vm_delete  | voicemails.messages.deleted |
        When a message is left on voicemail "1801@default" by "Billy"
        When a message is checked and deleted on voicemail "1801@default"
        Then I receive a voicemail message event "user_voicemail_message_deleted" on the queue "test_vm_delete" with data:
         | caller_id_name | folder_name | folder_type |
         | Billy          | inbox       | new         |
        Then there's no message in voicemail "1801@default"
