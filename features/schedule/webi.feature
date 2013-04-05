Feature: Schedule

  Scenario: Remove closed hour
    Given I have a schedule "Test" in "America/Montreal" with the following schedules:
    | Status | Months | Days of month | Days of week | Start hour | End hour |
    | Opened |   1-12 |          1-31 |          1-5 |      09:00 |    17:00 |
    | Closed |     12 |            25 |          1-5 |      09:00 |    17:00 |
    | Closed |     12 |            31 |          1-5 |      09:00 |    17:00 |
    | Closed |      1 |             1 |          1-5 |      09:00 |    17:00 |
    When I delete the "Second" "Closed" schedule from "Test"
    Then I should have a schdule "Test" in "America/Montreal" with the following schedules:
    | Status | Months | Days of month | Days of week | Start hour | End hour |
    | Opened |   1-12 |          1-31 |          1-5 |      09:00 |    17:00 |
    | Closed |     12 |            25 |          1-5 |      09:00 |    17:00 |
    | Closed |      1 |             1 |          1-5 |      09:00 |    17:00 |
