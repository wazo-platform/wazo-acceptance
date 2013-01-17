Feature: SCCP General

    Scenario: Enable directmedia
        Given the SCCP directmedia is disabled
        When I enable the SCCP directmedia
        Then the option "directmedia" is at "1" in sccp.conf

    Scenario: Disable directmedia
        Given the SCCP directmedia is enabled
        When I disable the SCCP directmedia
        Then the option "directmedia" is at "0" in sccp.conf

    Scenario: Change dial timeout
        Given the SCCP dial timeout is at "1" seconds
        When I change the SCCP dial timeout to "6" seconds
        Then the option "dialtimeout" is at "6" in sccp.conf

    Scenario: Change language
        Given the SCCP language is "en_US"
        When I select the SCCP language "fr_FR"
        Then the option "language" is at "fr_FR" in sccp.conf
