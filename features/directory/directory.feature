Feature: Directory

    Scenario: Create a directory from CSV file
        Given the CSV file "phonebook-x254.csv" is copied on the server into "/tmp"
        When I create the following directory configurations:
          | name           | type | URI                     |
          | phonebook-x254 | File | /tmp/phonebook-x254.csv |
        Then the directory configuration "phonebook-x254" has the URI "file:///tmp/phonebook-x254.csv"
        When I edit and save the directory configuration "phonebook-x254"
        Then the directory configuration "phonebook-x254" has the URI "file:///tmp/phonebook-x254.csv"

    Scenario: Create a CTI directory definition from CSV file
        Given there are users with infos:
         | firstname | lastname   | number | context | cti_profile |
         | GreatLord | MacDonnell | 1043   | default | Client      |
        Given the CSV file "phonebook-x254.csv" is copied on the server into "/tmp"
        Given the following directory configurations exist:
          | name           | type | URI                     |
          | phonebook-x254 | File | /tmp/phonebook-x254.csv |
        Given the directory definition "phonebookcsv" does not exist
        Given the display filter "Display" exists with the following fields:
          | Field title | Field type | Default value | Display format               |
          | Nom         |            |               | {db-firstname} {db-lastname} |
          | Numéro      | phone      |               | {db-phone}                   |
          | Entreprise  |            | Inconnue      | {db-company}                 |
          | E-mail      |            |               | {db-mail}                    |
          | Mobile      | phone      |               | {db-mobile}                  |
          | Source      |            |               | {db-directory}               |
        When I add the following CTI directory definition:
          | name         | URI                            | delimiter | direct match                    |
          | phonebookcsv | file:///tmp/phonebook-x254.csv | \|        | firstname,lastname,mobilenumber |
        When I map the following fields and save the directory definition:
          | field name | value        |
          | firstname  | firstname    |
          | lastname   | lastname     |
          | phone      | mobilenumber |
        When I include "phonebookcsv" in the default directory
        When I restart the CTI server
        When I start the XiVO Client
        When I log in the XiVO Client as "greatlord", pass "macdonnell"
        When I search for "emmet" in the directory xlet
        Then the following results show up in the directory xlet:
          | Nom          | Numéro     | Entreprise | E-mail | Mobile     | Source |
          | Emmett Brown | 0601020304 |            |        |            |        |
        When I search for "0601" in the directory xlet
        Then the following results show up in the directory xlet:
          | Nom          | Numéro     | Entreprise | E-mail | Mobile     | Source |
          | Emmett Brown | 0601020304 |            |        |            |        |

    Scenario: Create a CTI directory definition from UTF-8 CSV file
        Given there are users with infos:
         | firstname | lastname   | number | context | cti_profile |
         | GreatLord | MacDonnell | 1043   | default | Client      |
        Given the CSV file "phonebook-unicode.csv" is copied on the server into "/tmp"
        Given the following directory configurations exist:
          | name              | type | URI                        |
          | phonebook-unicode | File | /tmp/phonebook-unicode.csv |
        Given the directory definition "phonebookunicode" does not exist
        Given the display filter "Display" exists with the following fields:
          | Field title | Field type | Default value | Display format               |
          | Nom         |            |               | {db-firstname} {db-lastname} |
          | Numéro      | phone      |               | {db-phone}                   |
        When I add the following CTI directory definition:
          | name             | URI                               | delimiter | direct match   |
          | phonebookunicode | file:///tmp/phonebook-unicode.csv | ;         | nom,prenom,tel |
        When I map the following fields and save the directory definition:
          | field name | value  |
          | firstname  | prenom |
          | lastname   | nom    |
          | phone      | tel    |
        When I include "phonebookunicode" in the default directory
        When I restart the CTI server
        When I start the XiVO Client
        When I log in the XiVO Client as "greatlord", pass "macdonnell"
        When I search for "pier" in the directory xlet
        Then the following results show up in the directory xlet:
          | Nom              | Numéro |
          | Pierre DÉSPROGES | 12345  |
        When I search for "dés" in the directory xlet
        Then the following results show up in the directory xlet:
          | Nom              | Numéro |
          | Pierre DÉSPROGES | 12345  |

    Scenario: Search for a contact without a line
        Given there are users with infos:
         | firstname | lastname   | cti_profile |
         | GreatLord | MacDonnell | Client      |
        Given the CSV file "phonebook-x254.csv" is copied on the server into "/tmp"
        Given the directory definition "internal" is included in the default directory
        When I start the XiVO Client
        When I log in the Xivo Client as "greatlord", pass "macdonnell"
        When I search for "emmet" in the directory xlet
        Then nothing shows up in the directory xlet

    Scenario: Search for a contact with special characters in his name
        Given there are users with infos:
         | firstname | lastname    | number | context | cti_profile |
         | Lord      | Sanderson   | 1042   | default | Client      |
         | Lôrdé     | Sànndéêrsòn |        |         |             |
         | Làârd     | Témèlêtë    |        |         |             |
         | Lûùrd     | Tûrècôt     |        |         |             |
        Given the internal phonebook is configured
        When I restart the CTI server
        When I start the XiVO Client
        When I log in the Xivo Client as "lord", pass "sanderson"
        When I search for "lord" in the directory xlet
        Then the following results show up in the directory xlet:
          | Nom            |
          | Lord Sanderson |
        When I search for "ôrdé" in the directory xlet
        Then the following results show up in the directory xlet:
          | Nom               |
          | Lôrdé Sànndéêrsòn |
        When I search for "asdfasdfasdfasdf" in the directory xlet
        Then nothing shows up in the directory xlet

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

    Scenario: Search for a contact in a LDAP server with an active directory username
        Given there are users with infos:
         | firstname | lastname   | number | context | cti_profile |
         | GreatLord | MacDonnell | 1043   | default | Client      |
        Given the LDAP server is configured and active
        Given there is a user with common name "ACTIVE\Directory" on the ldap server
        Given there are the following ldap filters:
          | name            | server       | username                                             | password  | base dn                          | display name | phone number    |
          | openldap-aduser | openldap-dev | cn=ACTIVE\Directory,dc=lan-quebec,dc=avencall,dc=com | superpass | dc=lan-quebec,dc=avencall,dc=com | cn           | telephoneNumber |
        Given the CTI directory definition is configured for LDAP searches using the ldap filter "openldap-aduser"
        When I start the XiVO Client
        When I log in the XiVO Client as "greatlord", pass "macdonnell"
        When I search for "active" in the directory xlet
        Then the following results show up in the directory xlet:
          | Nom               | Numéro |
          | active\ directory |        |
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

    Scenario: Call a contact in the directory
        Given there are no calls running
        Given there are users with infos:
          | firstname | lastname   | number | context | cti_profile |
          | Lord      | Sanderson  | 1042   | default | Client      |
          | GreatLord | MacDonnell | 1043   | default | Client      |
        Given the internal phonebook is configured
        Given extension 1042 will answer a call and wait
        Given extension 1043 will answer a call, wait 5 seconds and hangup
        When I include "internal" in the default directory
        When I restart the CTI server
        When I start the XiVO Client
        When I log in the Xivo Client as "lord", pass "sanderson"
        When I search for "greatlord" in the directory xlet
        When I double-click on the phone number for "GreatLord MacDonnell"
        When I wait 10 seconds
        Then I see the called extension "1043" by "1042" in call logs page
