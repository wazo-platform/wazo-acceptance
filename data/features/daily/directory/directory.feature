Feature: Remote Directory in CTI Client

    Scenario: Create a directory from CSV file
        Given the CSV file "phonebook-x254.csv" is copied on the server into "/tmp"
        When I create the following directory configurations:
          | name           | type     | URI                     |
          | phonebook-x254 | CSV file | /tmp/phonebook-x254.csv |
        Then the directory configuration "phonebook-x254" has the URI "file:///tmp/phonebook-x254.csv"
        When I edit and save the directory configuration "phonebook-x254"
        Then the directory configuration "phonebook-x254" has the URI "file:///tmp/phonebook-x254.csv"

    Scenario: Reverse lookup in a directory definition from UTF-8 CSV file
        Given there are users with infos:
         | firstname | lastname   | number | context | cti_profile | protocol |
         | GreatLord | MacDonnell | 1043   | default | Client      | sip      |
        Given the CSV file "phonebook-unicode.csv" is copied on the server into "/tmp"
        Given the following directory configurations exist:
          | name              | type     | URI                        |
          | phonebook-unicode | CSV file | /tmp/phonebook-unicode.csv |
        Given the directory definition "phonebookunicode" does not exist
        When I add the following CTI directory definition:
          | name             | URI                               | delimiter | direct match   | reverse match |
          | phonebookunicode | file:///tmp/phonebook-unicode.csv | ;         | nom,prenom,tel | tel           |
        When I map the following fields and save the directory definition:
          | field name | value  |
          | firstname  | prenom |
          | lastname   | nom    |
          | phone      | tel    |
          | reverse    | nom    |
        When I include "phonebookunicode" in the default directory
        When I set the following directories for directory reverse lookup:
        | directory        |
        | phonebookunicode |
        When I restart the CTI server
        Given I have a sheet model named "testsheet" with the variables:
        | variable          |
        | xivo-calleridnum  |
        | xivo-calleridname |
        Given I assign the sheet "testsheet" to the "Link" event
        Given there is an incall "1043" in context "from-extern" to the "User" "GreatLord MacDonnell"

        When I start the XiVO Client
        When I enable screen pop-up
        When I log in the XiVO Client as "greatlord", pass "macdonnell"
        When chan_test calls "1043@from-extern" with id "1043-1" and calleridname "DÉSPROGES" and calleridnum "12345"
        When I wait 1 seconds for the call processing
        When "GreatLord MacDonnell" answers
        When I wait 1 seconds for the calls processing
        When chan_test hangs up "1043-1"
        When I wait 1 seconds for the call processing

        Then I see a sheet with the following values:
        | Variable          | Value     |
        | xivo-calleridname | DÉSPROGES |
        | xivo-calleridnum  | 12345     |
