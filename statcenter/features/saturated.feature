Feature: Saturated calls

    Scenario: Generate stats for saturated calls
        Given there is no queue with name "q1"
        Given there is no "FULL" entry in queue "q1" between "2012-07-01 08:00:00" and "2012-07-01 11:59:59"
        Given there is no "DIVERT_CA_RATIO" entry in queue "q1" between "2012-07-01 08:00:00" and "2012-07-01 11:59:59"
        Given there is no "DIVERT_HOLTIME" entry in queue "q1" between "2012-07-01 08:00:00" and "2012-07-01 11:59:59"
        Given there is a queue "q1" in context "statscenter" with number "5502"
        Given there is a statistic configuration "test" from "8" to "12" with queue "q1"
        Given I have to following queue_log entries:
        ...
        Then I should have the following statististic on "q1" on "2012-07-01" on configuration "test":
        ...
