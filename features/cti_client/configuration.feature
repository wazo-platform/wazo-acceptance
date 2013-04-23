Feature: CtiClient Configuration

    Scenario: Bad server address
        When I start the XiVO Client
        When I log in the XiVO Client with bad server address
        Then I see a error message on CtiClient

    Scenario: Bad server port
        When I start the XiVO Client
        When I log in the XiVO Client with bad server port
        Then I see a error message on CtiClient

    Scenario: Show/Hide agent option on login screen
        When I start the XiVO Client
        When I hide agent option on login screen
        Then I not see agent option on login screen
        When I show agent option on login screen
        Then I see agent option on login screen
        