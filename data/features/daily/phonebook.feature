Feature: Phonebook

    Scenario: Phonebook search from a phone
        Given the phonebook is accessible by any hosts
        Given the internal directory exists
        Given the directory definition "internal" is included in the default directory
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
