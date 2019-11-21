Feature: Schedule call distribution

  Scenario: Call distribution when the schedule is opened:
    Given I have a schedule "open" in "America/Montreal" with the following schedules:
    | periods | months | month_days | week_days | hours_start | hours_end |
    | open    |   1-12 |       1-31 |       1-7 |       00:00 |     23:59 |
    Given there are telephony users with infos:
    | firstname | lastname | exten | context |
    | Peter     | Parker   |  1001 | default |
    | Clark     | Kent     |  1002 | default |
    Given "Clark Kent" has schedule "open"
    When "Peter Parker" calls "1002"
    Then "Clark Kent" is ringing

  Scenario: Call distribution when the schedule is closed:
    Given there are telephony users with infos:
    | firstname | lastname | exten | context |
    | Peter     | Parker   |  1001 | default |
    | Clark     | Kent     |  1002 | default |
    | Bruce     | Wayne    |  1003 | default |
    Given I have a schedule "closed" in "America/Montreal" with the following schedules towards user "Bruce Wayne":
    | periods | months | month_days | week_days | hours_start | hours_end |
    | open    |      1 |          1 |         1 |       00:00 |     00:01 |
    Given "Clark Kent" has schedule "closed"
    When "Peter Parker" calls "1002"
    When I wait "4" seconds for the call to be forwarded
    Then "Bruce Wayne" is ringing

  Scenario: Call distribution when the schedule is closed during open period:
    Given there are telephony users with infos:
    | firstname | lastname | exten | context |
    | Peter     | Parker   |  1001 | default |
    | Clark     | Kent     |  1002 | default |
    | Bruce     | Wayne    |  1003 | default |
    Given I have a schedule "closed_in_open" in "America/Montreal" with the following schedules:
    | periods     | months | month_days | week_days | hours_start | hours_end | destination_user |
    | open        |   1-12 |       1-31 |       1-7 |       00:00 |     23:59 |                  |
    | exceptional |   1-12 |       1-31 |       1-7 |       00:01 |     23:58 | Bruce Wayne      |
    Given "Clark Kent" has schedule "closed_in_open"
    When "Peter Parker" calls "1002"
    When I wait "4" seconds for the call to be forwarded
    Then "Bruce Wayne" is ringing

  Scenario: Call distribution on group schedule
    Given there are telephony users with infos:
    | firstname | lastname | exten | context |
    | Peter     | Parker   |  1001 | default |
    | Clark     | Kent     |  1002 | default |
    | Bruce     | Wayne    |  1003 | default |
    Given I have a schedule "group-closed" in "America/Montreal" with the following schedules towards user "Bruce Wayne":
    | periods | months | month_days | week_days | hours_start | hours_end |
    | open    |      1 |          1 |         1 |       00:00 |     00:01 |
    Given there are telephony groups with infos:
    | name   | exten | context | schedule     |
    | league |  2666 | default | group-closed |
    Given the telephony group "league" has users:
    | firstname | lastname |
    | Peter     | Parker   |

    When "Peter Parker" calls "2666"
    When I wait "4" seconds for the call to be forwarded
    Then "Bruce Wayne" is ringing

  Scenario: Call distribution on incall schedule
    Given there are telephony users with infos:
    | firstname | lastname | exten | context |
    | Clark     | Kent     |  1002 | default |
    | Bruce     | Wayne    |  1003 | default |
    Given I have a schedule "incall-closed" in "America/Montreal" with the following schedules towards user "Bruce Wayne":
    | periods | months | month_days | week_days | hours_start | hours_end |
    | open    |      1 |          1 |         1 |       00:00 |     00:01 |
    Given there is an incall "1002@from-extern" to the user "Clark Kent"
    Given I have a schedule "incall-closed" associated to incall "1002@from-extern"
    When chan_test calls "1002@from-extern"
    When I wait "4" seconds for the call to be forwarded
    Then "Bruce Wayne" is ringing
