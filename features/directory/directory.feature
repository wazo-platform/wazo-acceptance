Feature: Remote Directory in CTI Client

    Scenario: Create a directory from CSV file
        Given the CSV file "phonebook-x254.csv" is copied on the server into "/tmp"
        When I create the following directory configurations:
          | name           | type | URI                     |
          | phonebook-x254 | File | /tmp/phonebook-x254.csv |
        Then the directory configuration "phonebook-x254" has the URI "file:///tmp/phonebook-x254.csv"
        When I edit and save the directory configuration "phonebook-x254"
        Then the directory configuration "phonebook-x254" has the URI "file:///tmp/phonebook-x254.csv"

    Scenario: Create a CTI directory definition from CSV file
        Given there are users with infos:
         | firstname | lastname   | number | context | cti_profile |
         | GreatLord | MacDonnell | 1043   | default | Client      |
        Given the CSV file "phonebook-x254.csv" is copied on the server into "/tmp"
        Given the following directory configurations exist:
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
        When I log in the XiVO Client as "greatlord", pass "macdonnell"
        When I search for "emmet" in the directory xlet
        Then the following results show up in the directory xlet:
          | Nom          | Numéro     | Entreprise | E-mail | Mobile     | Source |
          | Emmett Brown | 0601020304 |            |        |            |        |
        When I search for "0601" in the directory xlet
        Then the following results show up in the directory xlet:
          | Nom          | Numéro     | Entreprise | E-mail | Mobile     | Source |
          | Emmett Brown | 0601020304 |            |        |            |        |

    Scenario: Create a CTI directory definition from UTF-8 CSV file
        Given there are users with infos:
         | firstname | lastname   | number | context | cti_profile |
         | GreatLord | MacDonnell | 1043   | default | Client      |
        Given the CSV file "phonebook-unicode.csv" is copied on the server into "/tmp"
        Given the following directory configurations exist:
          | name              | type | URI                        |
          | phonebook-unicode | File | /tmp/phonebook-unicode.csv |
        Given the directory definition "phonebookunicode" does not exist
        Given the display filter "Display" exists with the following fields:
          | Field title | Field type | Default value | Display format               |
          | Nom         |            |               | {db-firstname} {db-lastname} |
          | Numéro      | phone      |               | {db-phone}                   |
        When I add the following CTI directory definition:
          | name             | URI                               | delimiter | direct match   |
          | phonebookunicode | file:///tmp/phonebook-unicode.csv | ;         | nom,prenom,tel |
        When I map the following fields and save the directory definition:
          | field name | value  |
          | firstname  | prenom |
          | lastname   | nom    |
          | phone      | tel    |
        When I include "phonebookunicode" in the default directory
        When I restart the CTI server
        When I start the XiVO Client
        When I log in the XiVO Client as "greatlord", pass "macdonnell"
        When I search for "pier" in the directory xlet
        Then the following results show up in the directory xlet:
          | Nom              | Numéro |
          | Pierre DÉSPROGES | 12345  |
        When I search for "dés" in the directory xlet
        Then the following results show up in the directory xlet:
          | Nom              | Numéro |
          | Pierre DÉSPROGES | 12345  |

    Scenario: Reverse lookup in a directory definition from UTF-8 CSV file
        Given there are users with infos:
         | firstname | lastname   | number | context | cti_profile | protocol |
         | GreatLord | MacDonnell | 1043   | default | Client      | sip      |
        Given the CSV file "phonebook-unicode.csv" is copied on the server into "/tmp"
        Given the following directory configurations exist:
          | name              | type | URI                        |
          | phonebook-unicode | File | /tmp/phonebook-unicode.csv |
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
        When chan_test hangs up "1043-1"

        Then I see a sheet with the following values:
        | Variable          | Value     |
        | xivo-calleridname | DÉSPROGES |
        | xivo-calleridnum  | 12345     |

    Scenario: Search for a contact without a line
        Given there are users with infos:
         | firstname | lastname   | cti_profile |
         | GreatLord | MacDonnell | Client      |
        Given the CSV file "phonebook-x254.csv" is copied on the server into "/tmp"
        Given the directory definition "internal" is included in the default directory
        When I start the XiVO Client
        When I log in the Xivo Client as "greatlord", pass "macdonnell"
        When I search for "emmet" in the directory xlet
        Then nothing shows up in the directory xlet

    Scenario: Search for a contact with special characters in his name
        Given there are users with infos:
         | firstname | lastname    | number | context | cti_profile |
         | Lord      | Sanderson   | 1042   | default | Client      |
         | Lôrdé     | Sànndéêrsòn |        |         |             |
         | Làârd     | Témèlêtë    |        |         |             |
         | Lûùrd     | Tûrècôt     |        |         |             |
        Given the internal phonebook is configured
        When I restart the CTI server
        When I start the XiVO Client
        When I log in the Xivo Client as "lord", pass "sanderson"
        When I search for "lord" in the directory xlet
        Then the following results show up in the directory xlet:
          | Nom            |
          | Lord Sanderson |
        When I search for "ôrdé" in the directory xlet
        Then the following results show up in the directory xlet:
          | Nom               |
          | Lôrdé Sànndéêrsòn |
        When I search for "asdfasdfasdfasdf" in the directory xlet
        Then nothing shows up in the directory xlet

    Scenario: Case insensitive search for a contact
        Given there are users with infos:
         | firstname | lastname  | number | context | cti_profile |
         | Lord      | Sanderson | 1042   | default | Client      |
        Given the directory definition "internal" is included in the default directory
        When I start the XiVO Client
        When I log in the XiVO Client as "lord", pass "sanderson"
        When I search for "LORD" in the directory xlet
        Then the following results show up in the directory xlet:
          | Nom            | Numéro |
          | Lord Sanderson | 1042   |
        When I search for "lord" in the directory xlet
        Then the following results show up in the directory xlet:
          | Nom            | Numéro |
          | Lord Sanderson | 1042   |

    Scenario: Search for a contact when list is sorted
        Given there are users with infos:
            | firstname | lastname  | number | context | cti_profile |
            | Lord      | Sanderson | 1002   | default |             |
            | Greg      | Sanderson | 1012   | default | Client      |
            | Fodé      | Sanderson | 1022   | default |             |
        Given the directory definition "internal" is included in the default directory
        When I start the XiVO Client
        When I log in the XiVO Client as "greg", pass "sanderson"
        When I search for "san" in the directory xlet
        When I sort results by column "Nom" in ascending order
        Then the following sorted results show up in the directory xlet:
          | Nom            | Numéro |
          | Fodé Sanderson | 1022   |
          | Greg Sanderson | 1012   |
          | Lord Sanderson | 1002   |
        When I search for "der" in the directory xlet
        Then the following sorted results show up in the directory xlet:
          | Nom            | Numéro |
          | Fodé Sanderson | 1022   |
          | Greg Sanderson | 1012   |
          | Lord Sanderson | 1002   |

    Scenario: Closing or disconnecting the client preserves sorting order when searching
        Given there are users with infos:
            | firstname | lastname  | number | context | cti_profile |
            | Fodé      | Sanderson | 1421   | default |             |
            | Greg      | Sanderson | 1411   | default | Client      |
            | Lord      | Sanderson | 1401   | default |             |
        Given the directory definition "internal" is included in the default directory

        When I start the XiVO Client
        When I log in the XiVO Client as "greg", pass "sanderson"
        When I search for "sanderson" in the directory xlet
        When I sort results by column "Numéro" in ascending order
        Then the following sorted results show up in the directory xlet:
          | Nom            | Numéro |
          | Lord Sanderson | 1401   |
          | Greg Sanderson | 1411   |
          | Fodé Sanderson | 1421   |

        When I log out of the XiVO Client
        When I log in the XiVO Client as "greg", pass "sanderson"
        When I search for "sanderson" in the directory xlet
        Then the following sorted results show up in the directory xlet:
          | Nom            | Numéro |
          | Lord Sanderson | 1401   |
          | Greg Sanderson | 1411   |
          | Fodé Sanderson | 1421   |

        When I stop the XiVO Client
        When I start the XiVO Client
        When I log in the XiVO Client as "greg", pass "sanderson"
        When I search for "sanderson" in the directory xlet
        Then the following sorted results show up in the directory xlet:
          | Nom            | Numéro |
          | Lord Sanderson | 1401   |
          | Greg Sanderson | 1411   |
          | Fodé Sanderson | 1421   |

    Scenario: Call a contact in the directory
        Given there are users with infos:
          | firstname | lastname   | number | context | protocol | cti_profile |
          | Lord      | Sanderson  |   1042 | default | sip      | Client      |
          | GreatLord | MacDonnell |   1043 | default | sip      | Client      |
        Given the internal phonebook is configured
        When I include "internal" in the default directory
        When I restart the CTI server
        When I start the XiVO Client
        When I log in the Xivo Client as "lord", pass "sanderson"
        When I search for "greatlord" in the directory xlet
        When I double-click on the phone number for "GreatLord MacDonnell"
        When "Lord Sanderson" answers
        When "GreatLord MacDonnell" answers
        When "Lord Sanderson" and "GreatLord MacDonnell" talk for "5" seconds
        When "GreatLord MacDonnell" hangs up
        Then I have the last call log matching:
            | source_name    | source_exten | duration | answered |
            | Lord Sanderson | 1042         | 0:00:05  | True     |
