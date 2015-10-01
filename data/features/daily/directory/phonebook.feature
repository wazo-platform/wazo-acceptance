Feature: Phonebook

    Scenario: Search for a contact in the phonebook
        Given "John Doe" is not in the phonebook
        Given the directory definition "internal" is included in the default directory
        When I add the following entries to the phonebook:
          | first name | last name | phone |
          | John       | Doe       | 1234  |
        When I search for "John"
        Then "John Doe" appears in the list
