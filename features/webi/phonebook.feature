Feature: Phonebook

    Scenario: Phonebook is sorted by display name
        Given the phonebook is accessible by any hosts
        Given "Abc Def" is not in the phonebook
        Given "Abc Aaa" is not in the phonebook
        When I add the following entries to the phonebook:
          | first name | last name | phone |
          | Abc        | Def       | 1234  |
          | Abc        | Aaa       | 6789  |
        When I search the phonebook for "Abc" on my Aastra
        Then I see the following results on the phone:
          | value            |
          | Abc Aaa (Office) |
          | Abc Def (Office) |

    Scenario: Phonebook searches using SSL LDAP connection
        Given the phonebook is accessible by any hosts
        Given the LDAP server is configured for SSL connections
        Given there are entries in the ldap server:
          | first name  | last name   | phone      |
          | SupremeLord | Sanderson   | 4185551234 |
      When I search the phonebook for "sup" on my Aastra
      Then I see the following results on the phone:
          | value                          |
          | SupremeLord Sanderson (Office) |

    Scenario: Phonebook searches using multiple filters
        Given the phonebook is accessible by any hosts
        Given the LDAP server is configured
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
          | value                  |
          | Marie IPad (City)      |
          | Cédric SimCity (City)  |
          | Linus Torvalds (State) |
          | Pape Francois (State)  |
