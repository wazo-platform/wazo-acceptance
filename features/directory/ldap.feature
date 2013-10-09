Feature: LDAP

    Scenario: Add LDAP Server
        Given there is no LDAP server "test-ldap-server"
        When I create an LDAP server with name "test-ldap-server" and host "test-ldap-server"
        Then LDAP server "test-ldap-server" is displayed in the list

    Scenario: Add LDAP Filter
        Given there is a LDAP server with name "test-ldap-server" and with host "test-ldap-server"
        Given there is no LDAP filter "test-ldap-filter"
        When I create an LDAP filter with name "test-ldap-filter" and server "test-ldap-server (test-ldap-server)"
        Then LDAP filter "test-ldap-filter" is displayed in the list
