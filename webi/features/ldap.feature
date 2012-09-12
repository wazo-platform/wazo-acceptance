Feature: ldap

    Scenario: Add LDAP Server
        Given there is no LDAP server "test-ldap-server"
        When I create an LDAP server with name "test-ldap-server" and host "test-ldap-server"
        Then LDAP server "test-ldap-server" is displayed in the list

    Scenario: Add LDAP Filter
        Given there is no LDAP filter "test-ldap-filter"
        Given there is a LDAP server with name "test-ldap-server" and with host "test-ldap-server"
        When I go on the add LDAP filter page
        When I set the text field "Name" to "test-ldap-filter"
        When I set the text field "Base DN" to "dc=lan-quebec,dc=avencall,dc=com"
        When I set the select field "LDAP Server" to "test-ldap-server (test-ldap-server)"
        When I go to the "Attributes" tab
        When I set the display name to "sn" 
        When I set the phone number to "telephoneNumber" 
        When I submit
        Then LDAP filter "test-ldap-filter" is displayed in the list
