Feature: Directory

    Scenario: Create a directory from CSV file
        Given the directory "phonebook-x254" does not exist
        Given the CSV file "phonebook-x254.csv" is copied on the server into "/tmp"
        When I configure the following directories:
          | name           | type | URI                     |
          | phonebook-x254 | File | /tmp/phonebook-x254.csv |
        Then the directory "phonebook-x254" has the URI "file:///tmp/phonebook-x254.csv"
        When I edit and save the directory "phonebook-x254"
        Then the directory "phonebook-x254" has the URI "file:///tmp/phonebook-x254.csv"

    Scenario: Create a CTI directory definition from CSV file
        Given there are users with infos:
         | firstname | lastname   | number | context | cti_profile |
         | GreatLord | MacDonnell | 1043   | default | Client      |
        Given the CSV file "phonebook-x254.csv" is copied on the server into "/tmp"
        Given the following directories exist:
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
        Given the context "default" uses display "Display" with the following directories:
          | Directories |
          | xivodir     |
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

    Scenario: Search for a contact in a SSL LDAP directory
        Given there are users with infos:
         | firstname | lastname   | number | context | cti_profile |
         | GreatLord | MacDonnell | 1043   | default | Client      |
        Given the directory definition "openldap" does not exist
        Given the LDAP server is configured for SSL connections
        Given there are entries in the ldap server:
          | first name | last name | phone      |
          | Milan      | Gélinas   | 0133123456 |
        Given the display filter "Display" exists with the following fields:
          | Field title | Field type | Display format               |
          | Nom         |            | {db-firstname} {db-lastname} |
          | Numéro      |            | {db-phone}                   |
        When I add the following CTI directory definition:
          | name     | URI                       | direct match                 |
          | openldap | ldapfilter://openldap-dev | sn,givenName,telephoneNumber |
        When I map the following fields and save the directory definition:
          | field name | value           |
          | firstname  | givenName       |
          | lastname   | sn              |
          | phone      | telephoneNumber |
        When I include "openldap" in the default directory
        When I restart the CTI server
        When I start the XiVO Client
        When I log in the XiVO Client as "greatlord", pass "macdonnell"
        When I search for "gélinas" in the directory xlet
        Then "Milan Gélinas" shows up in the directory xlet

    Scenario: Search for a contact with special characters in his name
        Given there are users with infos:
         | firstname | lastname  | number | context | cti_profile |
         | Lord      | Sanderson | 1042   | default | Client      |
        Given the internal phonebook is configured
        Given there are users with infos:
          | firstname | lastname    |
          | Lôrdé     | Sànndéêrsòn |
          | Làârd     | Témèlêtë    |
          | Lûùrd     | Tûrècôt     |
        When I include "internal" in the default directory
        When I restart the CTI server
        When I start the XiVO Client
        When I log in the Xivo Client as "lord", pass "sanderson"
        When I search for "lord" in the directory xlet
        Then "Lord Sanderson" shows up in the directory xlet
        When I search for "ôrdé" in the directory xlet
        Then "Lôrdé Sànndéêrsòn" shows up in the directory xlet
        When I search for "asdfasdfasdfasdf" in the directory xlet
        Then nothing shows up in the directory xlet

    Scenario: Search for a contact in a LDAP server with a custom filter
        Given there are users with infos:
         | firstname | lastname   | number | context | cti_profile |
         | GreatLord | MacDonnell | 1043   | default | Client      |
        Given the directory definition "openldapexplicit" does not exist
        Given the LDAP server is configured
        Given there are entries in the ldap server:
          | first name | last name              | email             | city   | state  | phone      |
          | explicite  | mail avencall no state | user@avencall.com | Québec |        | 3698521478 |
          | explicite  | no mail state quebec   |                   |        | Québec | 123123123  |
          | explicite  | mail example no state  | qqch@example.com  |        |        | 4445556666 |
        Given there are the following ldap filters:
          | name              | server       | username                                  | password  | base dn                          | filter                                         | display name | phone number    |
          | openldap-explicit | openldap-dev | cn=admin,dc=lan-quebec,dc=avencall,dc=com | superpass | dc=lan-quebec,dc=avencall,dc=com | &(cn=*%Q*)(\|(mail=*@avencall.com)(st=Québec)) | cn           | telephoneNumber |
        Given the display filter "Display" exists with the following fields:
          | Field title | Field type | Display format               |
          | Nom         |            | {db-firstname} {db-lastname} |
          | Numéro      |            | {db-phone}                   |
        When I add the following CTI directory definition:
          | name             | URI                            | direct match                 |
          | openldapexplicit | ldapfilter://openldap-explicit | sn,givenName,telephoneNumber |
        When I map the following fields and save the directory definition:
          | field name | value           |
          | firstname  | givenName       |
          | lastname   | sn              |
          | phone      | telephoneNumber |
        When I include "openldapexplicit" in the default directory
        When I restart the CTI server
        When I start the XiVO Client
        When I log in the XiVO Client as "greatlord", pass "macdonnell"
        When I search for "explicite" in the directory xlet
        Then "explicite mail avencall no state" shows up in the directory xlet
        Then "explicite no mail state quebec" shows up in the directory xlet
        Then "explicite mail example no state" does not show up in the directory xlet

    Scenario: Search for a contact in a LDAP server with special characters
        Given there are users with infos:
         | firstname | lastname   | number | context | cti_profile |
         | GreatLord | MacDonnell | 1043   | default | Client      |
        Given the directory definition "openldapchars" does not exist
        Given the LDAP server is configured
        Given there are entries in the ldap server:
          | first name | last name | email               | city  | state | phone | mobile |
          | Vwé        | Xyzà      | vwexyza@example.org | phone | 987   | 987   | 987    |
        Given there are the following ldap filters:
          | name              | server       | username                                  | password  | base dn                          | display name | phone number    |
          | openldap-chars    | openldap-dev | cn=admin,dc=lan-quebec,dc=avencall,dc=com | superpass | dc=lan-quebec,dc=avencall,dc=com | cn           | telephoneNumber |
        Given the display filter "Display" exists with the following fields:
          | Field title | Field type | Display format               |
          | Nom         |            | {db-firstname} {db-lastname} |
          | Numéro      |            | {db-phone}                   |
        When I add the following CTI directory definition:
          | name          | URI                            | direct match                 |
          | openldapchars | ldapfilter://openldap-chars    | sn,givenName,telephoneNumber |
        When I map the following fields and save the directory definition:
          | field name | value           |
          | firstname  | givenName       |
          | lastname   | sn              |
          | phone      | telephoneNumber |
        When I include "openldapchars" in the default directory
        When I restart the CTI server
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
