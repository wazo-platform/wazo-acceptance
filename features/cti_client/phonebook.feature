Feature: Phonebook

    Scenario: Search for a contact in the phonebook
        Given "John Doe" is not in the phonebook
        When I add the following entries to the phonebook:
          | first name | last name | phone |
          | John       | Doe       | 1234  |
        When I search for "John"
        Then "John Doe" appears in the list

    Scenario: Import phonebook entries from a CSV file
        Given there is a user "Lord" "Sanderson" with extension "1042@default" and CTI profile "Client"
        Given "Marty McFly" is not in the phonebook
        When I import the CSV file "phonebook-x268.csv" into the phonebook
        When I start the XiVO Client
        When I log in the XiVO Client as "lord", pass "sanderson"
        Then "Marty McFly" shows up in the directory xlet after searching for "marty"

