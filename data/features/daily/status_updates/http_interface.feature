Feature: Status related HTTP interfaces

  Scenario: User status
    Given there are users with infos:
    | firstname | lastname  | cti_profile | cti_login | cti_passwd |
    | Tyrion    | Lannister | Client      | tyrion    | tyrion     |
    Given I start the XiVO Client
    Given I log in the XiVO client as "tyrion", pass "tyrion"
    When I change my presence to "away"
    Then I should have have the following user status when I query the cti:
    | user_id | origin_uuid | firstname | lastname  | presence |
    | yes     | yes         | Tyrion    | Lannister | away     |
