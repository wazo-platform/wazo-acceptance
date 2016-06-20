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
        When I log agent "042"
        Then I receive a "agent_status_update" on the queue "test_status_agent" with data:
        | agent_id | agent_number | status    |
        | yes      |          042 | logged_in |

    Scenario: Bus notification on presence change
        Given I listen on the bus for messages:
        | queue            | routing_key |
        | test_status_user | status.user |
        Given there are users with infos:
         | firstname | lastname  | cti_profile | cti_login | cti_passwd |
         | Donald    | MacRonald | Client      | donald    | macronald  |
        Given I start the XiVO Client
        Given I log in the XiVO client as "donald", pass "macronald"
        When I change my presence to "away"
        Then I receive a "user_status_update" on the queue "test_status_user" with data:
        | user_uuid | firstname | lastname  | status |
        | yes       | Donald    | MacRonald | away   |

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
        | endpoint_id | number | context | status |
        | yes         |   1101 | default |      8 |
