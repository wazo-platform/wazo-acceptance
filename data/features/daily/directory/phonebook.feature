Feature: Phonebook

    Scenario: Search for a contact in the phonebook
        Given "John Doe" is not in the phonebook
        Given the directory definition "internal" is included in the default directory
        When I add the following entries to the phonebook:
          | first name | last name | phone |
          | John       | Doe       | 1234  |
        When I search for "John"
        Then "John Doe" appears in the list

    Scenario: Import phonebook entries from a CSV file
        Given there are users with infos:
         | firstname | lastname  | number | context | cti_profile |
         | Lord      | Sanderson | 1042   | default | Client      |
        Given the directory definition "xivodir" is included in the default directory
        Given "Marty McFly" is not in the phonebook
        When I import the CSV file "phonebook-x268.csv" into the phonebook
        When I start the XiVO Client
        When I log in the XiVO Client as "lord", pass "sanderson"
        When I search for "marty" in the directory xlet
        Then the following results show up in the directory xlet:
          | Nom         | Numéro |
          | Marty McFly | 1981   |

    Scenario: Phonebook is sorted by display name
        Given the phonebook is accessible by any hosts
        Given there are no LDAP filters configured in the phonebook
        Given "Abc Def" is not in the phonebook
        Given "Abc Aaa" is not in the phonebook
        When I add the following entries to the phonebook:
          | first name | last name | phone |
          | Abc        | Def       | 1234  |
          | Abc        | Aaa       | 6789  |
        When I search the phonebook for "Abc" on my Aastra
        Then I see the following results on the phone:
          | name             |
          | Abc Aaa (Office) |
          | Abc Def (Office) |

    Scenario: Phonebook searches using SSL LDAP connection
        Given the phonebook is accessible by any hosts
        Given there are no LDAP filters configured in the phonebook
        Given the LDAP server is configured for SSL connections
        Given there are entries in the ldap server:
          | first name  | last name   | phone      |
          | SupremeLord | Sanderson   | 4185551234 |
      When I search the phonebook for "sup" on my Aastra
      Then I see the following results on the phone:
          | name                           |
          | SupremeLord Sanderson (Office) |

    Scenario: Phonebook searches using multiple filters
        Given the phonebook is accessible by any hosts
        Given there are no LDAP filters configured in the phonebook
        Given the LDAP server is configured and active
        Given there are entries in the ldap server:
          | first name | last name | city   | state  | phone      |
          | Marie      | IPad      | Québec |        | 4181111111 |
          | Cédric     | SimCity   | Québec |        | 4182222222 |
          | Linus      | Torvalds  |        | Québec | 4183333333 |
          | Pape       | Francois  |        | Québec | 4184444444 |
        Given there are the following ldap filters:
          | name           | server       | username                                  | password  | base dn                          | filter  | display name | phone number    | phone number type |
          | openldap-city  | openldap-dev | cn=admin,dc=lan-quebec,dc=avencall,dc=com | superpass | dc=lan-quebec,dc=avencall,dc=com | l=*%Q*  | cn           | telephoneNumber | City              |
          | openldap-state | openldap-dev | cn=admin,dc=lan-quebec,dc=avencall,dc=com | superpass | dc=lan-quebec,dc=avencall,dc=com | st=*%Q* | cn           | telephoneNumber | State             |
        Given the ldap filter "openldap-city" has been added to the phonebook
        Given the ldap filter "openldap-state" has been added to the phonebook
        When I search the phonebook for "QU" on my Aastra
        Then I see the following results on the phone:
          | name                   |
          | Marie IPad (City)      |
          | Cédric SimCity (City)  |
          | Linus Torvalds (State) |
          | Pape Francois (State)  |

    Scenario: Phonebook searches LDAP using multiple attributes in display name
        Given the phonebook is accessible by any hosts
        Given there are no LDAP filters configured in the phonebook
        Given the LDAP server is configured and active
        Given there are entries in the ldap server:
          | first name | last name | city        | state        | phone  |
          | foobar     | city      | foobar city |              | 123789 |
          | foobar     | state     |             | foobar state | 123456 |
        Given there are the following ldap filters:
          | name                 | server       | username                                  | password  | base dn                          | display name | phone number    |
          | openldap-displayname | openldap-dev | cn=admin,dc=lan-quebec,dc=avencall,dc=com | superpass | dc=lan-quebec,dc=avencall,dc=com | l,st         | telephoneNumber |
        Given the ldap filter "openldap-displayname" has been added to the phonebook
        When I search the phonebook for "foobar" on my Aastra
        Then I see the following results on the phone:
          | name                  |
          | foobar city (Office)  |
          | foobar state (Office) |

    Scenario: Phonebook searches LDAP using multiple attriburtes in phone number
        Given the phonebook is accessible by any hosts
        Given there are no LDAP filters configured in the phonebook
        Given the LDAP server is configured and active
        Given there are entries in the ldap server:
          | first name  | last name   | mobile       | phone        |
          | utilisateur | mobile      | 654 456 9871 |              |
          | utilisateur | phoneNumber |              | 496 548 6512 |
        Given there are the following ldap filters:
          | name                 | server       | username                                  | password  | base dn                          | display name | phone number           |
          | openldap-phonenumber | openldap-dev | cn=admin,dc=lan-quebec,dc=avencall,dc=com | superpass | dc=lan-quebec,dc=avencall,dc=com | cn           | telephoneNumber,mobile |
        Given the ldap filter "openldap-phonenumber" has been added to the phonebook
        When I search the phonebook for "utilisateur" on my Aastra
        Then I see the following results on the phone:
          | name                             | number     |
          | utilisateur mobile (Office)      | 6544569871 |
          | utilisateur phoneNumber (Office) | 4965486512 |

    Scenario: Phonebook searches LDAP using a custom filter
        Given the phonebook is accessible by any hosts
        Given there are no LDAP filters configured in the phonebook
        Given the LDAP server is configured and active
        Given there are entries in the ldap server:
          | first name | last name              | email             | city   | state  | phone      |
          | explicite  | mail avencall no state | user@avencall.com | Québec |        | 3698521478 |
          | explicite  | no mail state quebec   |                   |        | Québec | 123123123  |
          | explicite  | mail example no state  | qqch@example.com  |        |        | 4445556666 |
        Given there are the following ldap filters:
          | name              | server       | username                                  | password  | base dn                          | filter                                         | display name | phone number    |
          | openldap-explicit | openldap-dev | cn=admin,dc=lan-quebec,dc=avencall,dc=com | superpass | dc=lan-quebec,dc=avencall,dc=com | &(cn=*%Q*)(\|(mail=*@avencall.com)(st=Québec)) | cn           | telephoneNumber |
        Given the ldap filter "openldap-explicit" has been added to the phonebook
        When I search the phonebook for "explicite" on my Aastra
        Then I see the following results on the phone:
          | name                                      | number     |
          | explicite mail avencall no state (Office) | 3698521478 |
          | explicite no mail state quebec (Office)   | 123123123  |
        Then I do not see the following results on the phone:
          | name                            | number     |
          | explicite mail example no state | 4445556666 |

    Scenario: Phonebook searches LDAP using special characters
        Given the phonebook is accessible by any hosts
        Given there are no LDAP filters configured in the phonebook
        Given the LDAP server is configured and active
        Given there are entries in the ldap server:
          | first name | last name | email               | phone |
          | Vwé        | Xyzà      | vwexyza@example.org | 987   |
        Given there are the following ldap filters:
          | name              | server       | username                                  | password  | base dn                          | display name | phone number    |
          | openldap-chars    | openldap-dev | cn=admin,dc=lan-quebec,dc=avencall,dc=com | superpass | dc=lan-quebec,dc=avencall,dc=com | cn           | telephoneNumber |
        Given the ldap filter "openldap-chars" has been added to the phonebook
        When I search the phonebook for "Vw" on my Aastra
        Then I see the following results on the phone:
          | name              | number |
          | Vwé Xyzà (Office) | 987    |
        When I search the phonebook for "é" on my Aastra
        Then I see the following results on the phone:
          | name              | number |
          | Vwé Xyzà (Office) | 987    |

    Scenario: Phonebook searches LDAP even when inactive
        Given there are users with infos:
         | firstname | lastname   | number | context | cti_profile |
         | GreatLord | MacDonnell | 1043   | default | Client      |
        Given the phonebook is accessible by any hosts
        Given there are no LDAP filters configured in the phonebook
        Given the LDAP server is configured and active
        Given there are entries in the ldap server:
          | first name | last name | email          | phone |
          | James      | Bond      | james@bond.com | 007   |
        Given there are the following ldap filters:
          | name              | server       | username                                  | password  | base dn                          | display name | phone number    |
          | openldap-inactive | openldap-dev | cn=admin,dc=lan-quebec,dc=avencall,dc=com | superpass | dc=lan-quebec,dc=avencall,dc=com | cn           | telephoneNumber |
        Given the ldap filter "openldap-inactive" has been added to the phonebook
        When the LDAP service is stopped
        When I search the phonebook for "james" on my Aastra
        Then I do not see the following results on the phone:
          | name                | number |
          | James Bond (Office) | 007    |
        When I search the phonebook for "greatlord" on my Aastra
        Then I see the following results on the phone:
          | name                 | number |
          | GreatLord MacDonnell | 1043   |

    Scenario: Phonebook searches LDAP even when shut down
        Given there are users with infos:
         | firstname | lastname   | number | context | cti_profile |
         | GreatLord | MacDonnell | 1043   | default | Client      |
        Given the phonebook is accessible by any hosts
        Given there are no LDAP filters configured in the phonebook
        Given the LDAP server is configured and active
        Given there are entries in the ldap server:
          | first name | last name | email          | phone |
          | James      | Bond      | james@bond.com | 007   |
        Given there are the following ldap filters:
          | name              | server       | username                                  | password  | base dn                          | display name | phone number    |
          | openldap-inactive | openldap-dev | cn=admin,dc=lan-quebec,dc=avencall,dc=com | superpass | dc=lan-quebec,dc=avencall,dc=com | cn           | telephoneNumber |
        Given the ldap filter "openldap-inactive" has been added to the phonebook
        When I shut down the LDAP server
        When I search the phonebook for "james" on my Aastra
        Then I do not see the following results on the phone:
          | name                | number |
          | James Bond (Office) | 007    |
        When I search the phonebook for "greatlord" on my Aastra
        Then I see the following results on the phone:
          | name                 | number |
          | GreatLord MacDonnell | 1043   |
