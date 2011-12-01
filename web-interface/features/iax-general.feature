Feature: IAX general parameters

    Scenario: Enable shrink Caller ID
        Given I am logged in
        Given I go on the General Settings > IAX Protocol page, tab "Advanced"
        Given the option "Shrink CallerID" is not checked
        When I go on the General Settings > IAX Protocol page, tab "Advanced"
        When I check this option
        When I submit
        When I go on the General Settings > IAX Protocol page, tab "Advanced"
        Then this option is checked

    Scenario: Disable shrink Caller ID
        Given I am logged in
        Given I go on the General Settings > IAX Protocol page, tab "Advanced"
        Given the option "Shrink CallerID" is checked
        When I go on the General Settings > IAX Protocol page, tab "Advanced"
        When I uncheck this option
        When I submit
        When I go on the General Settings > IAX Protocol page, tab "Advanced"
        Then this option is not checked

    Scenario: Enable SRV lookup
        Given I am logged in
        Given I go on the General Settings > IAX Protocol page, tab "Default"
        Given the option "SRV lookup" is checked
        When I go on the General Settings > IAX Protocol page, tab "Default"
        When I check this option
        When I submit
        When I go on the General Settings > IAX Protocol page, tab "Default"
        Then this option is checked

    Scenario: Disable SRV lookup
        Given I am logged in
        Given I go on the General Settings > IAX Protocol page, tab "Default"
        Given the option "SRV lookup" is checked
        When I go on the General Settings > IAX Protocol page, tab "Default"
        When I uncheck this option
        When I submit
        When I go on the General Settings > IAX Protocol page, tab "Default"
        Then this option is not checked