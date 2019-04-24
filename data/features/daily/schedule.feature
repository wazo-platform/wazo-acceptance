Feature: Schedule call distribution

  Scenario: Call distribution when the schedule is opened:
    Given I have a schedule "open" in "America/Montreal" with the following schedules:
    | Status | Months | Days of month | Days of week | Start hour | End hour |
    | Opened |   1-12 |          1-31 |          1-7 |      00:00 |    23:59 |
    Given there are users with infos:
    | firstname | lastname | number | context | protocol | schedule |
    | Peter     | Parker   |   1001 | default | sip      |          |
    | Clark     | Kent     |   1002 | default | sip      | open     |
    When "Peter Parker" calls "1002"
    Then "Clark Kent" is ringing

  Scenario: Call distribution when the schedule is closed:
    Given there are users with infos:
    | firstname | lastname | number | context | protocol |
    | Peter     | Parker   |   1001 | default | sip      |
    | Clark     | Kent     |   1002 | default | sip      |
    | Bruce     | Wayne    |   1003 | default | sip      |
    Given I have a schedule "closed" in "America/Montreal" towards user "Bruce" "Wayne" with the following schedules:
    | Status | Months | Days of month | Days of week | Start hour | End hour |
    | Opened |      1 |             1 |            1 |      00:00 |    00:01 |
    Given user "Clark" "Kent" has schedule "closed"
    When "Peter Parker" calls "1002"
    When I wait 3 seconds
    Then "Bruce Wayne" is ringing

  Scenario: Call distribution when the schedule is closed during open period:
    Given there are users with infos:
    | firstname | lastname | number | context | protocol |
    | Peter     | Parker   |   1001 | default | sip      |
    | Clark     | Kent     |   1002 | default | sip      |
    | Bruce     | Wayne    |   1003 | default | sip      |
    Given I have a schedule "closed_in_open" in "America/Montreal" with the following schedules:
    | Status | Months | Days of month | Days of week | Start hour | End hour | Destination firstname | Destination lastname |
    | Opened |   1-12 |          1-31 |          1-7 |      00:00 |    23:59 |                       |                      |
    | Closed |   1-12 |          1-31 |          1-7 |      00:01 |    23:58 | Bruce                 | Wayne                |
    Given user "Clark" "Kent" has schedule "closed_in_open"
    When "Peter Parker" calls "1002"
    When I wait 3 seconds
    Then "Bruce Wayne" is ringing

  Scenario: Call distribution on group schedule
    Given there are users with infos:
    | firstname | lastname | number | context | protocol |
    | Peter     | Parker   |   1001 | default | sip      |
    | Clark     | Kent     |   1002 | default | sip      |
    | Bruce     | Wayne    |   1003 | default | sip      |
    Given I have a schedule "group-closed" in "America/Montreal" towards user "Bruce" "Wayne" with the following schedules:
    | Status | Months | Days of month | Days of week | Start hour | End hour |
    | Opened |      1 |             1 |            1 |      00:00 |    00:01 |
    Given there are groups:
    | name   | exten | context | users      | schedule     |
    | league |  2666 | default | Clark Kent | group-closed |
    When "Peter Parker" calls "2666"
    When I wait 3 seconds
    Then "Bruce Wayne" is ringing

  Scenario: Call distribution on incall schedule
    Given there are users with infos:
    | firstname | lastname | number | context | protocol |
    | Clark     | Kent     |   1002 | default | sip      |
    | Bruce     | Wayne    |   1003 | default | sip      |
    Given I have a schedule "incall-closed" in "America/Montreal" towards user "Bruce" "Wayne" with the following schedules:
    | Status | Months | Days of month | Days of week | Start hour | End hour |
    | Opened |      1 |             1 |            1 |      00:00 |    00:01 |
    Given there are incalls with infos in the webi:
    | extension | context     | destination_type | destination | schedule      |
    |      1002 | from-extern | User             | Clark Kent  | incall-closed |
    When chan_test calls "1002@from-extern"
    When I wait 3 seconds
    Then "Bruce Wayne" is ringing
