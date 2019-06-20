Feature: Incalls

    Scenario: Incall to destination user
        Given there are telephony users with infos:
          | firstname | lastname | exten | context | protocol |
          | Incall    | User     | 1801  | default | sip      |
        Given there is an incall "1801@from-extern" to the user "Incall User"
        When chan_test calls "1801@from-extern"
        Then "Incall User" is ringing
