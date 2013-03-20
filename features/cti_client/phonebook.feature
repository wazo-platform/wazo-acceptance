Feature: Phonebook

    Scenario: Search for a contact in the phonebook
        Given "John Doe" is not in the phonebook
        Given the directory definition "internal" is included in the default directory
        When I add the following entries to the phonebook:
          | first name | last name | phone |
          | John       | Doe       | 1234  |
        When I search for "John"
        Then "John Doe" appears in the list

    Scenario: Case insensitive search for a contact
        Given there is a user "Lord" "Sanderson" with extension "1042@default" and CTI profile "Client"
        Given the directory definition "internal" is included in the default directory
        When I start the XiVO Client
        When I log in the XiVO Client as "lord", pass "sanderson"
        When I search for "LORD" in the directory xlet
        Then "Lord Sanderson" shows up in the directory xlet
        When I search for "lord" in the directory xlet
        Then "Lord Sanderson" shows up in the directory xlet
