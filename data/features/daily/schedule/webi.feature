Feature: Schedule

  Scenario: Remove closed hour
    Given I have a schedule "Test" in "America/Montreal" with the following schedules:
    | Status | Months | Days of month | Days of week | Start hour | End hour |
    | Opened |   1-12 |          1-31 |          1-5 |      09:00 |    17:00 |
    | Closed |     12 |            25 |          1-5 |      09:00 |    17:00 |
    | Closed |     12 |            31 |          1-5 |      09:00 |    17:00 |
    | Closed |      1 |             1 |          1-5 |      09:00 |    17:00 |
    When I delete the "Second" "Closed" schedule from "Test"
    Then I should have a schedule "Test" in "America/Montreal" with the following schedules:
    | Status | Months | Days of month | Days of week | Start hour | End hour |
    | Opened |   1-12 |          1-31 |          1-5 |      09:00 |    17:00 |
    | Closed |     12 |            25 |          1-5 |      09:00 |    17:00 |
    | Closed |      1 |             1 |          1-5 |      09:00 |    17:00 |

  Scenario: Remove opened hour
    Given I have a schedule "Test" in "America/Montreal" with the following schedules:
    | Status | Months | Days of month | Days of week | Start hour | End hour |
    | Opened |   1-12 |          1-31 |          1-3 |      09:00 |    17:00 |
    | Opened |   1-12 |          1-31 |          4-5 |      09:00 |    21:00 |
    | Opened |   1-12 |          1-31 |          6-7 |      10:00 |    18:00 |
    When I delete the "Second" "Opened" schedule from "Test"
    Then I should have a schedule "Test" in "America/Montreal" with the following schedules:
    | Status | Months | Days of month | Days of week | Start hour | End hour |
    | Opened |   1-12 |          1-31 |          1-3 |      09:00 |    17:00 |
    | Opened |   1-12 |          1-31 |          6-7 |      10:00 |    18:00 |

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
