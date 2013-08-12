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
        | xlet                    | position |
        | Identity                | dock     |
        | Dialer                  | dock     |
        | History                 | dock     |
        | Search                  | dock     |
        | Directory               | dock     |
        | Fax                     | dock     |
        | Features                | dock     |
        | Conference rooms        | dock     |
        | Datetime                | dock     |
        | Tabber                  | grid     |
        | MyDirectory             | dock     |
        | Customer info           | dock     |
        | Agents (list)           | dock     |
        | Agents (detail)         | dock     |
        | Queues (list)           | dock     |
        | Queue members           | dock     |
        | Queues (entries detail) | dock     |
        | Switchboard             | dock     |
        | Remote directory        | dock     |
        | Agent status dashboard  | dock     |
        Given there are users with infos:
         | firstname | lastname | number | context | cti_profile |
         | Bernard   | Derome   | 1044   | default | full        |
        When I start the XiVO Client
        When I log in and log out of the XiVO Client as "bernard", pass "derome" 10 times
        Then the XiVO Client did not crash

    Scenario: Enable/Disable menu availability
        Given there are users with infos:
         | firstname | lastname | number | context | cti_profile |
         | Gonzales  | DaCosta  | 1044   | default | Client      |
        When I start the XiVO Client
        When I enable menu availability
        Then I see menu availability are enabled
        When I disable menu availability
        Then I see menu availability are disabled
        When I enable menu availability
        Then I see menu availability are enabled

    Scenario: Enable/Disable start systrayed
        Given there are users with infos:
         | firstname | lastname | number | context | cti_profile |
         | Gonzales  | DaCosta  | 1044   | default | Client      |
        When I start the XiVO Client
        When I disable start systrayed
        When I stop the XiVO Client
        When I start the XiVO Client
        Then I see the window
        When I enable start systrayed
        When I stop the XiVO Client
        When I start the XiVO Client
        Then I not see the window
        When I disable start systrayed
        When I stop the XiVO Client
        When I start the XiVO Client
        Then I see the window

    Scenario: Enable/Disable auto reconnect
        Given there are users with infos:
         | firstname | lastname | number | context | cti_profile |
         | Gonzales  | DaCosta  | 1044   | default | Client      |
        When I start the XiVO Client
        When I set auto-reconnect interval to "5" seconds
        When I enable auto-reconnect
        When I log in the XiVO Client as "gonzales", pass "dacosta"
        When I restart the CTI server
        Then I logged after "5" seconds

    Scenario: Enable/Disable connect at startup
        Given there are users with infos:
         | firstname | lastname | number | context | cti_profile |
         | Gonzales  | DaCosta  | 1044   | default | Client      |
        When I start the XiVO Client
        When I enable keep password
        When I enable connect at startup
        When I log in the XiVO Client as "gonzales", pass "dacosta"
        When I stop the XiVO Client
        When I start the XiVO Client
        Then I logged after "2" seconds
        When I disable connect at startup
        When I stop the XiVO Client
        When I start the XiVO Client
        Then I not logged after "2" seconds

    Scenario: Enable/Disable multiple instances
        When I start the XiVO Client "default"
        When I enable multiple instances
        When I stop the XiVO Client "default"
        When I start the XiVO Client "default"
        When I start the XiVO Client "toto"
        Then I have "2" instances of the client
        When I disable multiple instances
        When I stop the XiVO Client "toto"
        When I stop the XiVO Client "default"
        When I start the XiVO Client "default"
        When I start the XiVO Client "toto"
        Then I have "1" instances of the client
