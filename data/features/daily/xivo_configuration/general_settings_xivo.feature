Feature: General Settings

    Scenario: Disable live reload
        Given live reload is enabled
        When I disable the live reload
        When I wait 10 seconds
        When I create users with the following parameters:
            | firstname | lastname |
            | Joe       |      Doe |
        Then i see no live reload request in sysconfd log file

    Scenario: Enable live reload
        Given live reload is disabled
        When I enable the live reload
        Then the CTI is notified for a configuration change
        When I create users with the following parameters:
            | firstname | lastname |
            | Joe       |      Doe |
        Then i see live reload request in sysconfd log file
