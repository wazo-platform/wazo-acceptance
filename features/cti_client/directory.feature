Feature: Directory

    Scenario: Import a directory from a CSV file
        Given there is a user "Lord" "Sanderson" with extension "1042@default" and CTI profile "Client"
        Given the directory "phonebook-x254" does not exist
        Given the directory definition "phonebook-csv" does not exist
        Given the CSV file "phonebook-x254.csv" is copied on the server into "/tmp"
        When I configure the following directories:
          | name           | type | URI                     |
          | phonebook-x254 | File | /tmp/phonebook-x254.csv |
        Then the directory "phonebook-x254" has the URI "file:///tmp/phonebook-x254.csv"
        When I edit and save the directory "phonebook-x254"
        Then the directory "phonebook-x254" has the URI "file:///tmp/phonebook-x254.csv"
        When I add the following CTI directory definition:
          | name         | URI                            | delimiter | direct match                    |
          | phonebookcsv | file:///tmp/phonebook-x254.csv | \|        | firstname,lastname,mobilenumber |
        When I map the following fields and save the directory definition:
          | field name | value        |
          | firstname  | firstname    |
          | lastname   | lastname     |
          | phone      | mobilenumber |
        When I include "phonebookcsv" in the default directory
        When I restart the CTI server
        When I start the XiVO Client
        When I log in the XiVO Client as "lord", pass "sanderson"
        Then "Emmett Brown" shows up in the directory xlet after searching for "emmet"
        Then "Emmett Brown" shows up in the directory xlet after searching for "0601"

