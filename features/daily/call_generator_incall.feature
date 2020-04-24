Feature: Incoming calls

  Scenario: Incoming call without reverse lookup
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone |
      | Oscar     | Latrail  | 1801  | default | yes        |
    Given there is an incall "1801@from-extern" to the user "Oscar Latrail"
    When incoming call received from "incall" to "1801@from-extern" with callerid ""incall" <666>"
    When "Oscar Latrail" answers
    Then "Oscar Latrail" is talking to "incall"

  Scenario: Incoming call with reverse lookup
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | mobile_phone_number | with_phone |
      | Oscar     | Latrail  | 1801  | default | 123                 | yes        |
      | El        | Diablo   |       |         | 666                 | no         |
    Given there is an incall "1801@from-extern" to the user "Oscar Latrail"
    When incoming call received from "incall" to "1801@from-extern" with callerid ""666" <666>"
    When "Oscar Latrail" answers
    Then "Oscar Latrail" is talking to "El Diablo"
