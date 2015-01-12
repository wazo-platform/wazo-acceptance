Feature: Status notifications

    Scenario: Bus notification on presence change
        Given there are users with infos:
         | firstname | lastname  | cti_profile | cti_login | cti_passwd |
         | Donald    | MacRonald | Client      | donald    | macronald  |
        Given I start the XiVO Client
        Given I log in the XiVO client as "donald", pass "macronald"
        Given I listen on the bus for messages:
        | exchange | routing_key |
        | xivo     | status.user |
        When I change my presence to "away"
        Then I receive a "user_status_update" on the bus exchange "xivo" with data:
        | user_id | firstname | lastname  | status | xivo_uuid |
        | yes     | Donald    | MacRonald | away   | yes       |

    Scenario: Bus notification on phone status change
        Given I listen on the bus for messages:
        | exchange | routing_key     |
        | xivo     | status.endpoint |
        Given there are users with infos:
        | firstname | lastname | number | context | protocol |
        | Alice     |          |   1100 | default | sip      |
        | Bob       |          |   1101 | default | sip      |
        When a call is started:
        | caller | dial | callee | talk_time | hangup |
        | Alice  | 1101 | Bob    |         3 | callee |
        Then I receive a "endpoint_status_update" on the bus exchange "xivo" with data:
        | endpoint_id | number | context | status | xivo_uuid |
        | yes         |   1101 | default |      8 | yes       |
