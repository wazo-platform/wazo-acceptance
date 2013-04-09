Feature: CtiClient Configuration

    Scenario: Bad server address
        When I start the XiVO Client
        When I log in the XiVO Client with bad server address
        Then I see a error message on CtiClient
