Feature: Directory

    Scenario: Create a directory from CSV file
        Given the directory "phonebook-x254" does not exist
        Given the CSV file "phonebook-x254.csv" is copied on the server into "/tmp"
        When I configure the following directories:
          | name           | type | URI                     |
          | phonebook-x254 | File | /tmp/phonebook-x254.csv |
        Then the directory "phonebook-x254" has the URI "file:///tmp/phonebook-x254.csv"
        When I edit and save the directory "phonebook-x254"
        Then the directory "phonebook-x254" has the URI "file:///tmp/phonebook-x254.csv"

    Scenario: Create a CTI directory definition from CSV file
        Given there is a user "Lord" "Sanderson" with extension "1042@default" and CTI profile "Client"
        Given the CSV file "phonebook-x254.csv" is copied on the server into "/tmp"
        Given the following directories exist:
          | name           | type | URI                     |
          | phonebook-x254 | File | /tmp/phonebook-x254.csv |
        Given the directory definition "phonebookcsv" does not exist
        Given the display filter "Display" exists with the following fields:
          | Field title | Field type | Default value | Display format               |
          | Nom         |            |               | {db-firstname} {db-lastname} |
          | Numéro      | phone      |               | {db-phone}                   |
          | Entreprise  |            | Inconnue      | {db-company}                 |
          | E-mail      |            |               | {db-mail}                    |
          | Mobile      | phone      |               | {db-mobile}                  |
          | Source      |            |               | {db-directory}               | 
	Given the context "default" uses display "Display" with the following directories:
          | Directories |
          | xivodir     |
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
        When I search for "emmet" in the directory xlet
        Then "Emmett Brown" shows up in the directory xlet
        When I search for "0601" in the directory xlet
        Then "Emmett Brown" shows up in the directory xlet

    Scenario: Search for a contact without a line
        Given there is a user "GreatLord" "MacDonnell" with CTI profile "Client"
        Given the CSV file "phonebook-x254.csv" is copied on the server into "/tmp"
        When I start the XiVO Client
        When I log in the Xivo Client as "greatlord", pass "macdonnell"
        When I search for "emmet" in the directory xlet
        Then nothing shows up in the directory xlet

    Scenario: Search for a contact with special characters in his name
        Given there is a user "Lord" "Sanderson" with extension "1042@default" and CTI profile "Client"
        Given the internal phonebook is configured
        Given there are users with infos:
          | firstname | lastname    |
          | Lôrdé     | Sànndéêrsòn |
          | Làârd     | Témèlêtë    |
          | Lûùrd     | Tûrècôt     |
        When I include "internal" in the default directory
        When I restart the CTI server
        When I start the XiVO Client
        When I log in the Xivo Client as "lord", pass "sanderson"
        When I search for "lord" in the directory xlet
        Then "Lord Sanderson" shows up in the directory xlet
        When I search for "ôrdé" in the directory xlet
        Then "Lôrdé Sànndéêrsòn" shows up in the directory xlet
        When I search for "asdfasdfasdfasdf" in the directory xlet
        Then nothing shows up in the directory xlet
