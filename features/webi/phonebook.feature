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
