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

    Scenario: Client doesn't crash after disconnecting
        Given there is a profile "full" with no services and xlets:
        | xlet                    |
        | Identity                |
        | Dialer                  |
        | History                 |
        | Search                  |
        | Directory               |
        | Fax                     |
        | Features                |
        | Conference rooms        |
        | Datetime                |
        | Tabber                  |
        | MyDirectory             |
        | Customer info           |
        | Agents (list)           |
        | Agents (detail)         |
        | Queues (list)           |
        | Queue members           |
        | Queues (entries detail) |
        | Switchboard             |
        | Remote directory        |
        | Agent status dashboard  |
        Given there are users with infos:
         | firstname | lastname | number | context | cti_profile |
         | Bernard   | Derome   | 1044   | default | full        |
        When I start the XiVO Client
        When I log in and log out of the XiVO Client as "bernard", pass "derome" 10 times
        Then the XiVO Client did not crash
