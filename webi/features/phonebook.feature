Feature: Phonebook

    Scenario: Search for a contact in the phonnebook
        Given "John Doe" is not in the phonebook
        When I add the following entries to the phonebook:
          | first name | last name | phone |
          | John       | Doe       | 1234  |
        When I search for "John"
        Then "John Doe" appears in the list
