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

    Scenario: Reverse lookup with LDAP
        Given a reverse lookup test configuration
        Given there are users with infos:
         | firstname | lastname | number | context | cti_profile | protocol |
         | Sam       | Well     |   1767 | default | Client      | sip      |
        Given there's an LDAP server configured for reverse lookup with entries:
         | first name | last name |      phone |
         | Peter      | Pan       | 5551236666 |
        Given I restart xivo-dird
        Given there is an incall "1767" in context "from-extern" to the "User" "Sam Well"
        When I start the XiVO Client
        When I enable screen pop-up
        When I log in the XiVO Client as "sam", pass "well"
        When chan_test calls "1767@from-extern" with id "1767-1" and calleridname "5551236666" and calleridnum "5551236666"
        When "Sam Well" answers
        Then I should see the following caller id:
         | Name  |     Number |
         | Peter | 5551236666 |
