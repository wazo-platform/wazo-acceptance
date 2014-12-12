Feature: User

    Scenario: Enable XiVO Client
        Given there are users with infos:
        | firstname | lastname | cti_profile | cti_login | cti_passwd |
        | Charles   | Magne    |   Client    | charles   | magne      |

        When I start the XiVO Client
        When I disable auto-reconnect
        When I disable access to XiVO Client to user "Charles" "Magne"
        Then I can't connect the CTI client of "Charles" "Magne"
        When I enable access to XiVO Client to user "Charles" "Magne"
        Then I can connect the CTI client of "Charles" "Magne"

    Scenario: Bus notification on presence change
        Given there are users with infos:
         | firstname | lastname  | cti_profile | cti_login | cti_passwd |
         | Donald    | MacRonald | Client      | donald    | macronald  |
        Given I start the XiVO Client
        Given I log in the XiVO client as "donald", pass "macronald"
        Given I listen on the bus for messages:
        | exchange            | routing_key |
        | xivo-status-updates | status.user |
        When I change my presence to "away"
        Then I receive a "user_status_update" on the bus with data on exchange "xivo-status-updates":
        | user_id | firstname | lastname  | status | xivo_uuid |
        | yes     | Donald    | MacRonald | away   | yes       |
