Feature: SCCP General

    Scenario: Enable directmedia
        Given the directmedia option is disabled
        Given I am on the SCCP General Settings page
        When I click the directmedia checkbox
        When I submit the form
        Then the option "directmedia" is at "1" in sccp.conf

    Scenario: Disable directmedia
        Given the directmedia option is enabled
        Given I am on the SCCP General Settings page
        When I click the directmedia checkbox
        When I submit the form
        Then the option "directmedia" is at "0" in sccp.conf

    Scenario: Change dial timeout
        Given the dial timeout is at 1 seconds
        Given I am on the SCCP General Settings page
        When I change the dial timeout to "6"
        When I submit the form
        Then the option "dialtimeout" is at "6" in sccp.conf

    Scenario: Change language
        Given the language option is at "en_US"
        Given I am on the SCCP General Settings page
        When I select the language "fr_FR"
        When I submit the form
        Then the option "language" is at "fr_FR" in sccp.conf

