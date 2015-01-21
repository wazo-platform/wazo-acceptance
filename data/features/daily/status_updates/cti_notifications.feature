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
         "  "data": {"user_id": 42,
         "           "xivo_id": "my-uuid",
         "           "status": "some-new-status"}}
         """
         Then I should receive the following cti command:
         """
         " {"class": "user_status_update",
         "  "timenow": "%(xivo_cti_timenow)s",
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
         "  "data": {"user_id": 42,
         "           "xivo_id": "my-uuid",
         "           "status": "some-new-status"}}
         """
         Then I should NOT receive the following cti command:
         """
         " {"class": "user_status_update",
         "  "timenow": "%(xivo_cti_timenow)s",
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
         "  "data": {"endpoint_id": 42,
         "           "xivo_id": "my-uuid",
         "           "status": 12}}
         """
         Then I should receive the following cti command:
         """
         " {"class": "endpoint_status_update",
         "  "timenow": "%(xivo_cti_timenow)s",
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
         "  "data": {"endpoint_id": 42,
         "           "xivo_id": "my-uuid",
         "           "status": 13}}
         """
         Then I should NOT receive the following cti command:
         """
         " {"class": "endpoint_status_update",
         "  "timenow": "%(xivo_cti_timenow)s",
         "  "data": {"status": 13,
         "           "endpoint_id": 42,
         "           "xivo_uuid": "my-uuid"}}
         """
