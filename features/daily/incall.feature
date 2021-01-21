Feature: Incalls

  Scenario: Incall to destination user
    Given there are telephony users with infos:
      | firstname | lastname | exten | context |
      | Incall    | User     | 1801  | default |
    Given there is an incall "1801@from-extern" to the user "Incall User"
    When chan_test calls "1801@from-extern"
    Then "Incall User" is ringing

  Scenario: Incall to destination DISA
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone |
      | User      | 01       | 1801  | default | yes        |
    Given there is an incall "1000@from-extern" to DISA redirected to "default" with pin "42"
    When incoming call received from "incall" to "1000@from-extern"
    When I wait 3 seconds for the call processing
    When "incall" sends DTMF "4"
    When "incall" sends DTMF "2"
    When "incall" sends DTMF "#"
    When I wait 2 seconds for the call processing
    When "incall" sends DTMF "1"
    When "incall" sends DTMF "8"
    When "incall" sends DTMF "0"
    When "incall" sends DTMF "1"
    When "incall" sends DTMF "#"
    When I wait 1 seconds for the call processing
    When "User 01" answers
    Then "User 01" is talking to "incall"
