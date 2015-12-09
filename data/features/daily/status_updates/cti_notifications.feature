Feature: Status notifications to cti client
    status events that are sent on the bus should be forwarded to
    registered xivo clients

    Scenario: Registered xivo clients receive the updated user statuses
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd |
         | Donny     | Brasco   | Client      | joseph    | pistone    |
         Given I connect to xivo-ctid:
         | username | password |
         | joseph   | pistone  |
         Given I send a cti message:
         """
         " {"class": "register_user_status_update",
         "  "user_ids": [["my-uuid", 42]]}
         """
         When I publish the following message on "status.user":
         """
         " {"name": "user_status_update",
         "  "origin_uuid": "my-uuid",
         "  "data": {"user_id": 42,
         "           "status": "some-new-status"}}
         """
         Then I should receive the following cti command:
         """
         " {"class": "user_status_update",
         "  "data": {"status": "some-new-status",
         "           "user_id": 42,
         "           "xivo_uuid": "my-uuid"}}
         """
         Given I send a cti message:
         """
         " {"class": "unregister_user_status_update",
         "  "user_ids": [["my-uuid", 42]]}
         """
         When I publish the following message on "status.user":
         """
         " {"name": "user_status_update",
         "  "origin_uuid": "my-uuid",
         "  "data": {"user_id": 42,
         "           "status": "some-new-status"}}
         """
         Then I should NOT receive the following cti command:
         """
         " {"class": "user_status_update",
         "  "data": {"status": "some-new-status",
         "           "user_id": 42,
         "           "xivo_uuid": "my-uuid"}}
         """

    Scenario: Registered xivo clients receive the updated endpoint statuses
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd |
         | Donny     | Brasco   | Client      | joseph    | pistone    |
         Given I connect to xivo-ctid:
         | username | password |
         | joseph   | pistone  |
         Given I send a cti message:
         """
         " {"class": "register_endpoint_status_update",
         "  "endpoint_ids": [["my-uuid", 42]]}
         """
         When I publish the following message on "status.endpoint":
         """
         " {"name": "endpoint_status_update",
         "  "origin_uuid": "my-uuid",
         "  "data": {"endpoint_id": 42,
         "           "status": 12}}
         """
         Then I should receive the following cti command:
         """
         " {"class": "endpoint_status_update",
         "  "data": {"status": 12,
         "           "endpoint_id": 42,
         "           "xivo_uuid": "my-uuid"}}
         """
         Given I send a cti message:
         """
         " {"class": "unregister_endpoint_status_update",
         "  "endpoint_ids": [["my-uuid", 42]]}
         """
         When I publish the following message on "status.endpoint":
         """
         " {"name": "endpoint_status_update",
         "  "origin_uuid": "my-uuid",
         "  "data": {"endpoint_id": 42,
         "           "status": 13}}
         """
         Then I should NOT receive the following cti command:
         """
         " {"class": "endpoint_status_update",
         "  "data": {"status": 13,
         "           "endpoint_id": 42,
         "           "xivo_uuid": "my-uuid"}}
         """

    Scenario: Registered xivo clients receive the updated agent statuses
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd |
         | Donny     | Brasco   | Client      | joseph    | pistone    |
         Given I connect to xivo-ctid:
         | username | password |
         | joseph   | pistone  |
         Given I send a cti message:
         """
         " {"class": "register_agent_status_update",
         "  "agent_ids": [["my-uuid", 42]]}
         """
         When I publish the following message on "status.agent":
         """
         " {"name": "agent_status_update",
         "  "origin_uuid": "my-uuid",
         "  "data": {"agent_id": 42,
         "           "status": "gone fishing"}}
         """
         Then I should receive the following cti command:
         """
         " {"class": "agent_status_update",
         "  "data": {"status": "gone fishing",
         "           "agent_id": 42,
         "           "xivo_uuid": "my-uuid"}}
         """
         Given I send a cti message:
         """
         " {"class": "unregister_agent_status_update",
         "  "agent_ids": [["my-uuid", 42]]}
         """
         When I publish the following message on "status.agent":
         """
         " {"name": "agent_status_update",
         "  "origin_uuid": "my-uuid",
         "  "data": {"agent_id": 42,
         "           "status": "gone fishing"}}
         """
         Then I should NOT receive the following cti command:
         """
         " {"class": "agent_status_update",
         "  "data": {"status": "gone fishing",
         "           "agent_id": 42,
         "           "xivo_uuid": "my-uuid"}}
         """

     Scenario: Chat messages published to the bus are forwarded to the appropriate client
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd |
         | Timothy   | Dalton   | Client      | jamesbond | bond007    |
         Given I connect to xivo-ctid:
         | username  | password |
         | jamesbond | bond007  |
         When I publish a chat message:
         | firstname | lastname | alias       | msg                     | from                  |
         | Timothy   | Dalton   | Pam Bouvier | Sweet dreams, Mr. Bond. | ["some-uuid-007", 42] |
         Then I should receive the following chat message:
         | firstname | lastname | alias       | msg                     | from                  |
         | Timothy   | Dalton   | Pam Bouvier | Sweet dreams, Mr. Bond. | ["some-uuid-007", 42] |
