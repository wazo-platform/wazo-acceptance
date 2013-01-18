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
