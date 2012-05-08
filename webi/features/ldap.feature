Feature: ldap

    Test X-238

    Scenario: Add LDAP Server
        Given I am logged in
        Given there is no LDAP server "ldap-server"
        When I create an LDAP server with name "ldap-server" and host "ldap-server"
        Then LDAP server "ldap-server" is displayed in the list
