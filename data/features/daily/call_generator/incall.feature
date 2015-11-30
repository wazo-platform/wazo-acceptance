Feature: Incoming calls

    Scenario: Incoming call without reverse lookup
        Given there are users with infos:
        | firstname | lastname   | number | context | protocol |
        | Oscar     | Latraverse |   1867 | default | sip      |
        | Will      | Hopkins    |   1868 | default | sip      |  # not necessary, workaround for linphone bug
        Given there is an incall "1867" in context "from-extern" to the "user" "Oscar Latraverse"
        Given I listen on the bus for messages:
        | queue       | routing_key   |
        | test_incall | ami.UserEvent |
        When chan_test calls "1867@from-extern" with id "callid" and calleridname "Caller" and calleridnum "666"
        When "Oscar Latraverse" answers
        When I wait 2 seconds
        When "Oscar Latraverse" hangs up
        Then I see an AMI message "UserEvent" on the queue "test_incall":
        | header    | value         |
        | UserEvent | ReverseLookup |
        | CHANNEL   | .*-callid     |

    Scenario: Incoming call with reverse lookup
        Given there are users with infos:
        | firstname | lastname | number | context | protocol |
        | Plume     | Wilde    |   1868 | default | sip      |
        | Anthony   | Smith    |   1869 | default | sip      |  # not necessary, workaround for linphone bug
        Given there is an incall "1868" in context "from-extern" to the "user" "Plume Wilde"
        Given there are entries in the phonebook:
        | first name | last name | phone | email           | company   | address1 |
        | El         | Diablo    |   666 | diablo@hell.org | Hell Inc. | 666 Hell |
        Given the directory definition "xivodirreverse" does not exist
        Given I add the following CTI directory definition:
        | name           | URI                                                                   | reverse match                 |
        | xivodirreverse | http://localhost/service/ipbx/json.php/private/pbx_services/phonebook | phonebooknumber.office.number |
        Given I map the following fields and save the directory definition:
        | field name | value                              |
        | firstname  | {phonebook.firstname}              |
        | lastname   | {phonebook.lastname}               |
        | fullname   | {phonebook.fullname}               |
        | phone      | {phonebooknumber.office.number}    |
        | mail       | {phonebook.email}                  |
        | reverse    | {phonebook.fullname}               |
        | address1   | {phonebookaddress.office.address1} |
        | company    | {phonebook.society}                |
        Given the following directories are used in reverse lookup:
        | directory       |
        | xivodirreverse  |
        Given I listen on the bus for messages:
        | queue                     | routing_key   |
        | test_incall_reverselookup | ami.UserEvent |
        When chan_test calls "1868@from-extern" with id "callid" and calleridname "666" and calleridnum "666"
        When "Plume Wilde" answers
        When I wait 2 seconds
        When "Plume Wilde" hangs up
        Then I see an AMI message "UserEvent" on the queue "test_incall_reverselookup":
        | header       | value           |
        | UserEvent    | ReverseLookup   |
        | CHANNEL      | .+-callid       |
        | db-reverse   | El Diablo       |
        | db-phone     | 666             |
        | db-lastname  | Diablo          |
        | db-firstname | El              |
        | db-fullname  | El Diablo       |
        | db-address1  | 666 Hell        |
        | db-mail      | diablo@hell.org |
        | db-company   | Hell Inc.       |
