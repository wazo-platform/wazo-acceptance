Feature: General Settings

    Scenario: Enable/Disable live reload configuration
        Given a live reload configuration is enable
        When i edit extenfeatures page
        Then i see messages in daemon log file
        When i disable live reload configuration
        When i edit extenfeatures page
        Then i see no messages in daemon log file
