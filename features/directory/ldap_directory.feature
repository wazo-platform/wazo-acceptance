Feature: LDAP Directory

    Scenario: Search for a contact in a SSL LDAP directory
        # If this test fails on May 24th 2014 or after, generate a new server certificate on the ldap server
        Given there are users with infos:
         | firstname | lastname   | number | context | cti_profile |
         | GreatLord | MacDonnell | 1043   | default | Client      |
        Given the LDAP server is configured for SSL connections
        Given there are entries in the ldap server:
          | first name | last name | phone      |
          | Milan      | Gélinas   | 0133123456 |
        Given the CTI directory definition is configured for LDAP searches using the ldap filter "openldap-dev"
        When I start the XiVO Client
        When I log in the XiVO Client as "greatlord", pass "macdonnell"
        When I search for "gélinas" in the directory xlet
        Then the following results show up in the directory xlet:
          | Nom           | Numéro      |
          | Milan Gélinas | 0133123456  |

    Scenario: Search for a contact in a LDAP server with a custom filter
        Given there are users with infos:
         | firstname | lastname   | number | context | cti_profile |
         | GreatLord | MacDonnell | 1043   | default | Client      |
        Given the LDAP server is configured and active
        Given there are entries in the ldap server:
          | first name | last name              | email             | city   | state  | phone      |
          | explicite  | mail avencall no state | user@avencall.com | Québec |        | 3698521478 |
          | explicite  | no mail state quebec   |                   |        | Québec | 123123123  |
          | explicite  | mail example no state  | qqch@example.com  |        |        | 4445556666 |
        Given there are the following ldap filters:
          | name              | server       | username                                  | password  | base dn                          | filter                                         | display name | phone number    |
          | openldap-explicit | openldap-dev | cn=admin,dc=lan-quebec,dc=avencall,dc=com | superpass | dc=lan-quebec,dc=avencall,dc=com | &(cn=*%Q*)(\|(mail=*@avencall.com)(st=Québec)) | cn           | telephoneNumber |
        Given the CTI directory definition is configured for LDAP searches using the ldap filter "openldap-explicit"
        When I start the XiVO Client
        When I log in the XiVO Client as "greatlord", pass "macdonnell"
        When I search for "explicite" in the directory xlet
        Then the following results show up in the directory xlet:
          | Nom                              | Numéro     |
          | explicite mail avencall no state | 3698521478 |
          | explicite no mail state quebec   | 123123123  |
        Then the following results does not show up in the directory xlet:
          | Nom                             | Numéro     |
          | explicite mail example no state | 4445556666 |

    Scenario: Search for a contact in a LDAP server with special characters
        Given there are users with infos:
         | firstname | lastname   | number | context | cti_profile |
         | GreatLord | MacDonnell | 1043   | default | Client      |
        Given the LDAP server is configured and active
        Given there are entries in the ldap server:
          | first name | last name | email               | phone |
          | Vwé        | Xyzà      | vwexyza@example.org | 987   |
        Given there are the following ldap filters:
          | name              | server       | username                                  | password  | base dn                          | display name | phone number    |
          | openldap-chars    | openldap-dev | cn=admin,dc=lan-quebec,dc=avencall,dc=com | superpass | dc=lan-quebec,dc=avencall,dc=com | cn           | telephoneNumber |
        Given the CTI directory definition is configured for LDAP searches using the ldap filter "openldap-chars"
        When I start the XiVO Client
        When I log in the XiVO Client as "greatlord", pass "macdonnell"
        When I search for "Vw" in the directory xlet
        Then the following results show up in the directory xlet:
          | Nom      | Numéro |
          | Vwé Xyzà | 987    |
        When I search for "é" in the directory xlet
        Then the following results show up in the directory xlet:
          | Nom      | Numéro |
          | Vwé Xyzà | 987    |

    Scenario: Search for a contact in a LDAP server with special characters in credentials
        Given there are users with infos:
         | firstname | lastname   | number | context | cti_profile |
         | GreatLord | MacDonnell | 1043   | default | Client      |
        Given the LDAP server is configured and active
        Given there is a user with common name "specialpass" and password "!@#$%^&*()_-+=[]{}/\<>" on the ldap server
        Given there are entries in the ldap server:
          | first name | last name | email                        | phone |
          | Bélaïne    | Alogé     | belaine.aloge@example.org    | 988   |
        Given there are the following ldap filters:
          | name           | server       | username                                                  | password               | base dn                          | display name | phone number    |
          | openldap-creds | openldap-dev | cn=specialpass,ou=people,dc=lan-quebec,dc=avencall,dc=com | !@#$%^&*()_-+=[]{}/\<> | dc=lan-quebec,dc=avencall,dc=com | cn           | telephoneNumber |
        Given the CTI directory definition is configured for LDAP searches using the ldap filter "openldap-creds"
        When I start the XiVO Client
        When I log in the XiVO Client as "greatlord", pass "macdonnell"
        When I search for "bél" in the directory xlet
        Then the following results show up in the directory xlet:
          | Nom           | Numéro |
          | Bélaïne Alogé | 988    |

    Scenario: Search for a contact in a LDAP server with an active directory username
        Given there are users with infos:
         | firstname | lastname   | number | context | cti_profile |
         | GreatLord | MacDonnell | 1043   | default | Client      |
        Given the LDAP server is configured and active
        Given there are entries in the ldap server:
            | first name | last name | phone |
            | active     | directory | 990   |
        Given there is a user with common name "ACTIVE\Directory" and password "superpass" on the ldap server
        Given there are the following ldap filters:
          | name            | server       | username                                             | password  | base dn                          | display name | phone number    |
          | openldap-aduser | openldap-dev | cn=ACTIVE\Directory,dc=lan-quebec,dc=avencall,dc=com | superpass | dc=lan-quebec,dc=avencall,dc=com | cn           | telephoneNumber |
        Given the CTI directory definition is configured for LDAP searches using the ldap filter "openldap-aduser"
        When I start the XiVO Client
        When I log in the XiVO Client as "greatlord", pass "macdonnell"
        When I search for "active" in the directory xlet
        Then the following results show up in the directory xlet:
          | Nom              | Numéro |
          | active directory | 990    |
        Then there are no errors in the CTI logs

    Scenario: Search for a contact in a LDAP server with invalid credentials
        Given there are users with infos:
         | firstname | lastname   | number | context | cti_profile |
         | GreatLord | MacDonnell | 1043   | default | Client      |
        Given the LDAP server is configured and active
        Given there are the following ldap filters:
          | name             | server       | username                                  | password        | base dn                          | display name | phone number    |
          | openldap-invalid | openldap-dev | cn=admin,dc=lan-quebec,dc=avencall,dc=com | invalidpassword | dc=lan-quebec,dc=avencall,dc=com | cn           | telephoneNumber |
        Given the internal directory exists
        Given the CTI server searches both the internal directory and the LDAP filter "openldap-invalid"
        When I start the XiVO Client
        When I log in the XiVO Client as "greatlord", pass "macdonnell"
        When I search for "greatlord" in the directory xlet
        Then the following results show up in the directory xlet:
          | Nom                  | Numéro |
          | GreatLord MacDonnell | 1043   |
        Then there are no errors in the CTI logs
        When I log out of the XiVO Client
        When I log in the XiVO Client as "greatlord", pass "macdonnell"
        When I search for "greatlord" in the directory xlet
        Then the following results show up in the directory xlet:
          | Nom                  | Numéro |
          | GreatLord MacDonnell | 1043   |
        Then there are no errors in the CTI logs

    Scenario: Search for a contact with an inactive LDAP server
        Given there are users with infos:
         | firstname | lastname   | number | context | cti_profile |
         | GreatLord | MacDonnell | 1043   | default | Client      |
        Given the LDAP server is configured and active
        Given there are entries in the ldap server:
          | first name | last name | email          | phone |
          | James      | Bond      | james@bond.com | 007   |
        Given there are the following ldap filters:
          | name              | server       | username                                  | password  | base dn                          | display name | phone number    |
          | openldap-inactive | openldap-dev | cn=admin,dc=lan-quebec,dc=avencall,dc=com | superpass | dc=lan-quebec,dc=avencall,dc=com | cn           | telephoneNumber |
        Given the CTI server searches both the internal directory and the LDAP filter "openldap-inactive"
        When the LDAP service is stopped
        When I start the XiVO Client
        When I log in the XiVO Client as "greatlord", pass "macdonnell"
        When I search for "james" in the directory xlet
        Then the following results does not show up in the directory xlet:
          | Nom        | Numéro |
          | James Bond | 007    |
        When I search for "greatlord" in the directory xlet
        Then the following results show up in the directory xlet:
          | Nom                  | Numéro |
          | GreatLord MacDonnell | 1043   |

    Scenario: Search for a contact with a LDAP server shut down
        Given there are users with infos:
         | firstname | lastname   | number | context | cti_profile |
         | GreatLord | MacDonnell | 1043   | default | Client      |
        Given the LDAP server is configured and active
        Given there are entries in the ldap server:
          | first name | last name | email          | phone |
          | James      | Bond      | james@bond.com | 007   |
        Given there are the following ldap filters:
          | name              | server       | username                                  | password  | base dn                          | display name | phone number    |
          | openldap-inactive | openldap-dev | cn=admin,dc=lan-quebec,dc=avencall,dc=com | superpass | dc=lan-quebec,dc=avencall,dc=com | cn           | telephoneNumber |
        Given the CTI server searches both the internal directory and the LDAP filter "openldap-inactive"
        When I shut down the LDAP server
        When I start the XiVO Client
        When I log in the XiVO Client as "greatlord", pass "macdonnell"
        When I search for "james" in the directory xlet
        Then the following results does not show up in the directory xlet:
          | Nom        | Numéro |
          | James Bond | 007    |
        When I search for "greatlord" in the directory xlet
        Then the following results show up in the directory xlet:
          | Nom                  | Numéro |
          | GreatLord MacDonnell | 1043   |
