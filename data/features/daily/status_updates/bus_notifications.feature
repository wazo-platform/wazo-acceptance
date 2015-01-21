Feature: Status notifications


    Scenario: Agent login status update events
        Given there is no agents logged
        Given there are users with infos:
        | firstname | lastname | number | context     | agent_number | protocol |
        | User      |      003 |   1003 | statscenter |          042 | sip      |
        Given there are queues with infos:
        | name     | number | context     | agents_number |
        | thequeue |   5010 | statscenter |           042 |
        Given I listen on the bus for messages:
        | queue             | routing_key  |
        | test_status_agent | status.agent |
        When "User 003" calls "*31042" and waits until the end
        Then I receive a "agent_status_update" on the queue "test_status_agent" with data:
        | agent_id | agent_number | status    | xivo_uuid |
        | yes      |          042 | logged_in | yes       |

    Scenario: Bus notification on presence change
        Given there are users with infos:
         | firstname | lastname  | cti_profile | cti_login | cti_passwd |
         | Donald    | MacRonald | Client      | donald    | macronald  |
        Given I start the XiVO Client
        Given I log in the XiVO client as "donald", pass "macronald"
        Given I listen on the bus for messages:
        | queue            | routing_key |
        | test_status_user | status.user |
        When I change my presence to "away"
        Then I receive a "user_status_update" on the queue "test_status_user" with data:
        | user_id | firstname | lastname  | status | xivo_uuid |
        | yes     | Donald    | MacRonald | away   | yes       |

    Scenario: Bus notification on phone status change
        Given I listen on the bus for messages:
        | queue | routing_key     |
        | test_status_endpoint       | status.endpoint |
        Given there are users with infos:
        | firstname | lastname | number | context | protocol |
        | Alice     |          |   1100 | default | sip      |
        | Bob       |          |   1101 | default | sip      |
        When a call is started:
        | caller | dial | callee | talk_time | hangup |
        | Alice  | 1101 | Bob    |         3 | callee |
        Then I receive a "endpoint_status_update" on the queue "test_status_endpoint" with data:
        | endpoint_id | number | context | status | xivo_uuid |
        | yes         |   1101 | default |      8 | yes       |

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
