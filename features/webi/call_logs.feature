Feature: Call logs

    Scenario: No error message when the requested call logs are not too big
        When I request call_logs for today
        Then I see no errors

    Scenario: Error message is displayed when the requested call logs are too big
        Given there are a lot of calls on the date "2013-07-24"
        When I request call_logs for "2013-07-24"
        Then I see errors
