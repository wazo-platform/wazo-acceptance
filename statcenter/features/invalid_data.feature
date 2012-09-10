Feature: QueueLog Invalid Data

    Scenario: Generate corrupt stats with EXITWITHTIMEOUT event
        Given there are a corrupt entry in queue_log
        When execute xivo-stat
        Then I don't should not have an error
