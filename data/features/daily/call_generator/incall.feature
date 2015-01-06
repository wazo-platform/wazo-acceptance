Feature: Incoming calls

    Scenario: Incoming call without reverse lookup
        Given there are users with infos:
        | firstname | lastname    | number | context | protocol |
        | Oscar     | Latraverse  |   1867 | default | sip      |
        Given there is an incall "1867" in context "from-extern" to the "user" "Oscar Latraverse"
        Given I listen on the bus for messages:
        | exchange | routing_key |
        | xivo-ami | UserEvent   |
        When chan_test calls "1867@from-extern" with id "callid" and calleridname "Caller" and calleridnum "666"
        Then I see an AMI message "UserEvent" on the bus:
        | header    | value         |
        | UserEvent | ReverseLookup |
        | CHANNEL   | .*-callidpwet     |

    Scenario: Incoming call with reverse lookup
        Given there are users with infos:
        | firstname | lastname | number | context | protocol |
        | Plume     | Wilde    |   1868 | default | sip      |
        Given there is an incall "1868" in context "from-extern" to the "user" "Plume Wilde"
        Given there are entries in the phonebook:
        | first name | last name | phone |
        | El         | Diablo    |   666 |
        Given I listen on the bus for messages:
        | exchange | routing_key |
        | xivo-ami | UserEvent   |
        When chan_test calls "1868@from-extern" with id "callid" and calleridname "Caller" and calleridnum "666"
        Then I see an AMI message "UserEvent" on the bus:
        | header       | value           |
        | UserEvent    | ReverseLookup   |
        | CHANNEL      | .+-callid       |
        | db-reverse   | El Diablo       |
        | db-phone     | 666             |
        | db-lastname  | Diablo          |
        | db-firstname | El              |
        | db-fullname  | El Diablo       |
        | db-address1  | 666, Hell       |
        | db-mail      | diablo@hell.org |
        | db-company   | Hell Inc.       |
