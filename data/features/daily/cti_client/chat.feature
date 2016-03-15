Feature: Chat

    Scenario: Bus notification on chat message
        Given I listen on the bus for messages:
        | queue              | routing_key                  |
        | test_chat_messages | chat.message.d0e36147-49f6-40b0-ac78-1af2048bed55.# |
        Given there are users with infos:
        | firstname | lastname | cti_profile | cti_login | cti_passwd |
        | Alice     | A        | Client      | alicea    | alicea     |
        Given I connect to xivo-ctid:
        | username | password |
        | alicea   | alicea   |
        Given I send a cti message:
        """
        " {"class": "chitchat",
        "  "alias": "Alice",
        "  "to": ["d0e36147-49f6-40b0-ac78-1af2048bed55", "7f49ae32-24ab-478a-8b98-cd4ea01d7584"],
        "  "text": "Yo yo yo"}
        """
        Then I receive a "chat_message_event" on the queue "test_chat_messages" with data:
        | alias | msg      | to                                                                               | from | firstname | lastname | origin_uuid |
        | Alice | Yo yo yo | ["d0e36147-49f6-40b0-ac78-1af2048bed55", "7f49ae32-24ab-478a-8b98-cd4ea01d7584"] | yes  | Alice     | A        | yes         |

     Scenario: Chat messages published to the bus are forwarded to the appropriate client
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd |
         | Timothy   | Dalton   | Client      | jamesbond | bond007    |
         Given I connect to xivo-ctid:
         | username  | password |
         | jamesbond | bond007  |
         When I publish a chat message:
         | firstname | lastname | alias       | msg                     | from                                                      |
         | Timothy   | Dalton   | Pam Bouvier | Sweet dreams, Mr. Bond. | ["some-uuid-007", "7f49ae32-24ab-478a-8b98-cd4ea01d7584"] |
         Then I should receive the following chat message:
         | firstname | lastname | alias       | msg                     | from                                                      |
         | Timothy   | Dalton   | Pam Bouvier | Sweet dreams, Mr. Bond. | ["some-uuid-007", "7f49ae32-24ab-478a-8b98-cd4ea01d7584"] |
