Feature: Phonebook

    Scenario: Search for a contact in the phonebook
        Given "John" "Doe" is not in the phonebook "wazo"
        Given the directory definition "internal" is included in the default directory
        When I add the following entries to the phonebook "wazo"
          | first name | last name | phone |
          | John       | Doe       | 1234  |
        Then "John Doe" appears in the list

    Scenario: Phonebook search from a phone
        Given the phonebook is accessible by any hosts
        Given the internal directory exists
        Given the directory definition "internal" is included in the default directory
        Given I restart wazo-dird
        Given the latest plugin "xivo-aastra-3" is installed
        Given I have the following devices:
          | mac               | latest plugin of | vendor | model
          | 00:11:22:33:44:55 | xivo-aastra-3    | Aastra | 6731i
        Given there are users with infos:
          | firstname | lastname | number | context | protocol |            device |
          | Michaud   | Pascal   |   1001 | default | sip      | 00:11:22:33:44:55 |
        When I search the phonebook for "Mich" on my Aastra "00:11:22:33:44:55"
        Then I see the following results on the phone:
          | name           | number
          | Michaud Pascal | 1001

    Scenario: Phonebook search from a phone using compat URL
        Given the phonebook is accessible by any hosts
        Given the internal directory exists
        Given the directory definition "internal" is included in the default directory
        Given I restart wazo-dird
        Given there are users with infos:
          | firstname | lastname | number | context | protocol |
          | Michaud   | Pascal   |   1001 | default | sip      |
        When I search the phonebook for "Mich" on my Aastra "00:11:22:33:44:55" using the compatibility URL
        Then I see the following results on the phone:
          | name           | number
          | Michaud Pascal | 1001
